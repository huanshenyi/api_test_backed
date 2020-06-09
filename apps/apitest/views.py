from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Project, Host, Api, ApiRunRecord, Case, CaseArgument, ApiArgument, CaseRunRecord, CaseApiRunRecord
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, HostSerializer, ApiSerializer, ApiRunRecordSerializer, \
    CaseArgumentSerializer, CaseSerializer, CaseRunRecordSerializer
from apps.autoauth.authorizations import JWTAuthentication
from utils import dictor

from .apirequest import request as api_request


class ProjectViewSets(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProjectSerializer


class HostViewSets(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = HostSerializer


class ApiViewSets(viewsets.ModelViewSet):
    queryset = Api.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ApiSerializer


class RunApiView(views.APIView):
    """
    APIを実行する
    """
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, api_id):
        api = Api.objects.get(pk=api_id)
        resp = api_request(api)
        recode = ApiRunRecord.objects.create(
            url=resp.url,
            http_method=resp.request.method,
            return_code=resp.status_code,
            return_content=resp.text,
            data=resp.request.body,
            headers=api.headers,
            api=api,
            user=request.user
        )
        serializer = ApiRunRecordSerializer(recode)
        return Response(serializer.data)


class CaseView(views.APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        """
        ケースの追加
        """
        serializer = CaseSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get("name")
            arguments = request.data.get("arguments")
            api_list = request.data.get("api_list")
            description = request.data.get("description")
            project_id = request.data.get("project_id")
            # ケースを新規追加
            case = Case.objects.create(
                name=name,
                description=description,
                user=request.user,
                project_id=project_id
            )
            # テストケースのパラメータ処理
            if arguments:
                for argument in arguments:
                    CaseArgument.objects.create(
                        name=argument["name"],
                        value=argument["value"],
                        case=case
                    )
            # APIリスト処理
            if api_list:
                api_list = sorted(api_list, key=lambda x: x["index"])
                for api in api_list:
                    api_model = Api.objects.get(pk=api["id"])
                    case.api_list.add(api_model)
                    api_arguments = api["arguments"]
                    print(api_arguments)
                    if api_arguments:
                        for api_argument in api_arguments:
                            ApiArgument.objects.create(
                                name=api_argument["name"],
                                origin=api_argument["origin"],
                                format=api_argument["format"],
                                api=api_model
                            )
            case.save()
            return Response(CaseSerializer(case).data)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, case_id):
        """
        ケース修正
        """
        serializer = CaseSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get("name")
            arguments = request.data.get("arguments")
            api_list = request.data.get("api_list")
            description = request.data.get("description")

            case = Case.objects.get(pk=case_id)
            case.name = name
            case.description = description

            # テストケースのパラメータ処理
            if arguments:
                argument_model_list = []
                for argument in arguments:
                    argument_id = argument["id"]
                    if argument_id:
                        argument_model = CaseArgument.objects.get(pk=argument_id)
                        argument_model.name = argument["name"]
                        argument_model.value = argument["value"]
                        argument_model.save()
                        argument_model_list.append(argument_model)
                    else:
                        print("koko")
                        argument_model = CaseArgument.objects.create(
                            name=argument["name"],
                            value=argument["value"],
                            case=case
                        )
                    argument_model_list.append(argument_model)
                # 改めて値を渡す
                case.arguments.set(argument_model_list)
            else:
                case.arguments.set([])
            # APIとAPIのパラメータ処理
            if api_list:
                api_model_list = []
                for api in api_list:
                    api_model = Api.objects.get(pk=api["id"])
                    api_arguments = api["arguments"]
                    # APIのパラメータ処理
                    if api_arguments:
                        argument_model_list = []
                        for api_argument in api_arguments:
                            argument_id = api_argument["id"]
                            if argument_id:
                                argument_model = ApiArgument.objects.get(pk=argument_id)
                                argument_model.name = api_argument["name"]
                                argument_model.origin = api_argument["origin"]
                                argument_model.format = api_argument["format"]
                                argument_model.save()
                            else:
                                argument_model = CaseArgument.objects.create(
                                    name=api_argument["name"],
                                    origin=api_argument["origin"],
                                    format=api_argument["format"],
                                    case=case
                                )
                            argument_model_list.append(argument_model)
                        api_model.arguments.set(argument_model_list)
                    else:
                        api_model.arguments.set([])
                    # apiのパラメータ処理後の再度保存
                    api_model.save()
                    api_model_list.append(api_model)
                case.api_list.set(api_model_list)
            else:
                case.api_list.set([])
            # 再度保存
            case.save()
            return Response(CaseSerializer(case).data)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RunCaseView(views.APIView):
    """
    テストケースの実行記録
    """
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, case_id):
        case = Case.objects.get(pk=case_id)
        case_arguments = CaseArgument.objects.filter(case=case)
        case_record = CaseRunRecord.objects.create(case=case)

        global_arguments = {}
        # テストケースのパラメータを追加
        for case_argument in case_arguments:
            global_arguments[case_argument.name] = case_argument.value

        # API実行&APIパラメータを追加
        api_model_list = case.api_list.all()
        for api_model in api_model_list:
            resp = api_request(api_model, global_arguments)
            CaseApiRunRecord.objects.create(
                url=resp.url,
                http_method=resp.request.method,
                data=resp.request.body,
                headers=resp.request.headers,
                user=request.user,
                return_code=resp.status_code,
                return_content=resp.text,
                api=api_model,
                case_record=case_record
            )
            # API実行後、必要なパラメータを取得
            api_arguments = api_model.arguments.all()
            if api_arguments:
                for api_argument in api_arguments:
                    dictor_data = {}
                    if api_argument.origin == "HEAD":
                        dictor_data = resp.headers
                    elif api_argument.origin == "COOKIE":
                        dictor_data = resp.cookies
                    elif api_argument.origin == "BODY":
                        dictor_data = resp.json()
                    argument_value = dictor.dictor(dictor_data, api_argument.format)
                    global_arguments[api_argument.name] = argument_value
                    # {"token":"xxx"} => token
        serializer = CaseRunRecordSerializer(case_record)
        return Response(serializer.data)



