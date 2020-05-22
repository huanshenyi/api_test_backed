__author__ = "ハリネズミ"
from rest_framework import serializers
from apps.autoauth.serializers import UserSerializer
from .models import Project, Host, Api


class HostSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Host
        fields = ['id', 'name', 'description', 'project_id', 'host']


class ProjectSerializer(serializers.ModelSerializer):
    """
    プロジェクトserializers
    """
    id = serializers.IntegerField(read_only=True)
    last_update_time = serializers.DateTimeField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    host_list = HostSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "type", "description", "last_update_time", "create_time", "user", "host_list"]


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
