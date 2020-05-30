__author__ = "ハリネズミ"

from rest_framework import serializers
from apps.autoauth.serializers import UserSerializer
from .models import Project, Host, Api, ApiRunRecord


class HostSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Host
        fields = ['id', 'name', 'description', 'project_id', 'host']


class ApiSerializer(serializers.ModelSerializer):
    """
    API
    """
    project_id = serializers.IntegerField(write_only=True)
    host = HostSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Api
        fields = "__all__"


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

    class Meta:
        model = Project
        fields = ["id", "name", "type", "description", "last_update_time", "create_time", "user", "host_list",
                  "api_list"]


class ApiRunRecordSerializer(serializers.ModelSerializer):
    api = ApiSerializer()

    class Meta:
        model = ApiRunRecord
        fields = "__all__"
