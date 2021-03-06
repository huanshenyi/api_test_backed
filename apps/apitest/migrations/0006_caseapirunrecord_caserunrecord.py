# Generated by Django 3.0.6 on 2020-06-07 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apitest', '0005_apiargument_case_caseargument'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseRunRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='実行時間')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apitest.Case', verbose_name='所属ケース')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='CaseApiRunRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200, verbose_name='リクエストurl')),
                ('http_method', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], max_length=10, verbose_name='メソッド')),
                ('headers', models.TextField(null=True, verbose_name='リクエストヘッド')),
                ('data', models.TextField(null=True, verbose_name='提出データ')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='実行時間')),
                ('return_code', models.CharField(max_length=10, verbose_name='リスポンスcode')),
                ('return_content', models.TextField(null=True, verbose_name='リスポンス内容')),
                ('api', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.Api', verbose_name='関連API')),
                ('case_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_records', to='apitest.CaseRunRecord', verbose_name='関連するケース実行記録')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='実行者')),
            ],
        ),
    ]
