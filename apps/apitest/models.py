from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

HTTP_METHOD_CHOICE = (
    ("POST", "POST"),
    ("GET", "GET"),
    ("PUT", "PUT"),
    ("DELETE", "DELETE"),
)


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


class Api(models.Model):
    """
    Apiデータ
    """
    STATUS_CODE_CHOICE = (
        ("200", "200"),
        ("201", "201"),
        ("202", "202"),
        ("203", "203"),
        ("204", "204"),
        ("301", "301"),
        ("302", "302"),
        ("400", "400"),
        ("401", "401"),
        ("403", "403"),
        ("404", "404"),
        ("405", "405"),
        ("406", "406"),
        ("407", "407"),
        ("408", "408"),
        ("500", "500"),
        ("502", "502")
    )
    name = models.CharField(max_length=50, verbose_name="api名称")
    http_method = models.CharField(max_length=50, verbose_name="Method", choices=HTTP_METHOD_CHOICE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name="host")
    path = models.CharField(max_length=1024, verbose_name="apiアドレス")
    headers = models.TextField(null=True, blank=True, verbose_name="リクエストヘット")
    data = models.TextField(null=True, blank=True, verbose_name="提出データ")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="詳細")
    expect_code = models.CharField(null=True, max_length=10, verbose_name="希望リスポンスcode", choices=STATUS_CODE_CHOICE)
    expect_content = models.CharField(null=True, max_length=200, verbose_name="希望リスポンスbody", blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="プロダクト", related_name="api_list",
                                null=True)


class ApiRunRecord(models.Model):
    """
    Api実行記録
    """
    url = models.CharField(max_length=200, verbose_name="リクエストurl")
    http_method = models.CharField(max_length=10, verbose_name="リクエストメソッド", choices=HTTP_METHOD_CHOICE)
    data = models.TextField(null=True, verbose_name="提出データ")
    headers = models.TextField(null=True, verbose_name="提出header")
    create_time = models.DateTimeField(auto_now=True, verbose_name="実行時間")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="実行者")
    return_code = models.CharField(max_length=10, verbose_name="レスポンスcode")
    return_content = models.TextField(null=True, verbose_name="レスポンス内容")
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name="関連API", null=True)

    class Meta:
        ordering = ["-create_time"]


class Case(models.Model):
    """
    テストケース
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="所属プロジェクト", related_name="case_list")
    name = models.CharField(max_length=50, verbose_name="ケース名")
    api_list = models.ManyToManyField(Api, related_name="case_list")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="制作者")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="詳細")
    create_time = models.DateTimeField(auto_now=True, verbose_name="更新時間")


class CaseArgument(models.Model):
    """
    ケースのパラメータ
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="テストケース", related_name="arguments")
    name = models.CharField(max_length=100, verbose_name="パラメータ名")
    value = models.CharField(max_length=100, verbose_name="パラメータ値")


class ApiArgument(models.Model):
    """
    ケースのAPIパラメータ
    """
    ARGUMENT_ORIGIN_CHOICE = (
        ("HEADER", "HEADER"),
        ("BODY", "BODY"),
        ("COOKIE", "COOKIE"),
    )
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name="ケースAPI", null=True, related_name="arguments")
    name = models.CharField(max_length=100, verbose_name="パラメータ名")
    origin = models.CharField(max_length=20, choices=ARGUMENT_ORIGIN_CHOICE, verbose_name="パラメータ出所")
    format = models.CharField(max_length=100, verbose_name="パラメータ取得形式")


class CaseRunRecord(models.Model):
    """
    ケースの実行記録
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="所属ケース")
    create_time = models.DateTimeField(auto_now=True, verbose_name="実行時間")

    class Meta:
        ordering = ['-create_time']


class CaseApiRunRecord(models.Model):
    """
     Case API実行記録
    """
    url = models.CharField(max_length=200, verbose_name="リクエストurl")
    http_method = models.CharField(max_length=10, verbose_name="メソッド", choices=HTTP_METHOD_CHOICE)
    headers = models.TextField(null=True, verbose_name="リクエストヘッド")
    data = models.TextField(null=True, verbose_name="提出データ")
    create_time = models.DateTimeField(auto_now=True, verbose_name="実行時間")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="実行者")
    return_code = models.CharField(max_length=10, verbose_name="リスポンスcode")
    return_content = models.TextField(null=True, verbose_name="リスポンス内容")
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name="関連API", null=True)
    case_record = models.ForeignKey(CaseRunRecord, on_delete=models.CASCADE, verbose_name="関連するケース実行記録",
                                    related_name="api_records")
