from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response
from .models import Project, Host, Api, ApiRunRecord
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, HostSerializer, ApiSerializer, ApiRunRecordSerializer
from apps.autoauth.authorizations import JWTAuthentication

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
    def post(self, request, api_id):
        api = Api.objects.get(pk=api_id)
        resp = api_request(api)
        recode = ApiRunRecord.objects.create(
            url=resp.url,
            http_method=resp.request.http_method,
            return_code=resp.status_code,
            return_content=resp.text,
            data=resp.request.body,
            headers=api.headers,
            api=api,
            user=request.user
        )
        serializer = ApiRunRecordSerializer(recode)
        return Response(serializer.data)



