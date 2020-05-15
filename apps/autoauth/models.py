from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError("携帯番号入れて")
        if not username:
            raise ValueError("ユーザーネーム入れて")
        if not password:
            raise ValueError("パスワード入れて")
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)


class AUTOUser(AbstractBaseUser, PermissionsMixin):
    """
    UserModelの書き換え
    """
    uid = ShortUUIDField(primary_key=True, verbose_name="ユーザーテーブル主キー")
    telephone = models.CharField(unique=True,max_length=11, verbose_name="携帯番号", null=True)
    email = models.EmailField(unique=True, max_length=100, verbose_name="アドレス", null=True)
    username = models.CharField(max_length=100, verbose_name="ユーザーネーム", unique=False)
    avatar = models.CharField(max_length=200, verbose_name="アイコンリンク")
    data_joined = models.DateTimeField(auto_now_add=True, verbose_name="新規時間")
    is_active = models.BooleanField(default=True, verbose_name="アカウント状態")

    # default検証時に使用
    USERNAME_FIELD = "email"
    # createsuperuser時に使用
    REQUIRED_FIELDS = ["username"]

    EMAIL_FIELD = "email"

    objects = UserManager()

    def get_full_user(self):
        return self.username

    def get_short_name(self):
        return self.username

