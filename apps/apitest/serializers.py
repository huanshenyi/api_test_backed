__author__ = "ハリネズミ"

from rest_framework import serializers
from apps.autoauth.serializers import UserSerializer
from .models import Project, Host, Api, ApiRunRecord, CaseArgument, Case, ApiArgument, CaseApiRunRecord, CaseRunRecord


class HostSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Host
        fields = ['id', 'name', 'description', 'project_id', 'host']


class ApiArgumentSerializer(serializers.ModelSerializer):
    """
    ケースAPIのパラメータ
    """

    class Meta:
        model = ApiArgument
        fields = "__all__"


class ApiSerializer(serializers.ModelSerializer):
    """
    API
    """
    project_id = serializers.IntegerField(write_only=True)
    host = HostSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)
    arguments = ApiArgumentSerializer(read_only=True, many=True)

    class Meta:
        model = Api
        fields = "__all__"


class ApiRunRecordSerializer(serializers.ModelSerializer):
    api = ApiSerializer()

    class Meta:
        model = ApiRunRecord
        fields = "__all__"


class CaseArgumentSerializer(serializers.ModelSerializer):
    """
    ケースパラメータ
    """

    class Meta:
        model = CaseArgument
        # 無限ループ回避のため
        exclude = ['case']


class CaseSerializer(serializers.ModelSerializer):
    """
    テストケース
    """
    project_id = serializers.IntegerField(write_only=True)
    api_list = ApiSerializer(many=True, read_only=True)
    arguments = CaseArgumentSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        # 排除
        exclude = ["user", "project"]


class ProjectSerializer(serializers.ModelSerializer):
    """
    プロジェクトserializers
    """
    id = serializers.IntegerField(read_only=True)
    last_update_time = serializers.DateTimeField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    host_list = HostSerializer(many=True, read_only=True)
    api_list = ApiSerializer(many=True, read_only=True)
    case_list = CaseSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "type", "description", "last_update_time", "create_time", "user", "host_list",
                  "api_list", "case_list"]


class CaseApiRunRecordSerializer(serializers.ModelSerializer):
    api = ApiSerializer()

    class Meta:
        model = CaseApiRunRecord
        fields = "__all__"


class CaseRunRecordSerializer(serializers.ModelSerializer):
    api_records = CaseApiRunRecordSerializer(many=True)
    case = CaseSerializer()

    class Meta:
        model = CaseRunRecord
        fields = "__all__"
