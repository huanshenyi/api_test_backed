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


class Host(models.Model):
    """
    Host管理する
    """
    name = models.CharField(max_length=50, verbose_name="名称")
    host = models.CharField(max_length=1024, verbose_name="hostアドレス")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="詳細")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="所属プロジェクト", related_name="host_list")
