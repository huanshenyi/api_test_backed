__author__ = "ハリネズミ"
from rest_framework import serializers
from apps.autoauth.serializers import UserSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    プロジェクトserializers
    """
    id = serializers.IntegerField(read_only=True)
    last_update_time = serializers.DateTimeField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        mode = Project
        fields = ["id", "name", "type", "description", "last_update_time", "create_time", "user"]
