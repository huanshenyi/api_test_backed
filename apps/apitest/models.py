from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Project(models.Model):
    """
    APIテストプロジェクト
    """
    ProjectType = (
        ("web", "web"),
        ("app", "app")
    )
    name = models.CharField(max_length=50, verbose_name="プロジェクトネーム")
    type = models.CharField(max_length=50, verbose_name="プロジェクトタイプ", choices=ProjectType)
    description = models.CharField(max_length=1024, blank=True, verbose_name="詳細")
    last_update_time = models.DateTimeField(auto_now_add=True, verbose_name="最近の修正時間")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="作った時間")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="作った人")
