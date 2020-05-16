__author__ = "ハリネズミ"
from rest_framework import serializers
from django.contrib.auth import get_user_model
AUTOUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AUTOUser
        fields = ["uid", "telephone", "username", "email", "avatar", "data_joined", "is_active"]
