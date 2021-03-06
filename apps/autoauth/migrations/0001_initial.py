# Generated by Django 3.0.6 on 2020-05-15 16:40

from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='AUTOUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False, verbose_name='ユーザーテーブル主キー')),
                ('telephone', models.CharField(max_length=11, null=True, unique=True, verbose_name='携帯番号')),
                ('email', models.EmailField(max_length=100, null=True, unique=True, verbose_name='アドレス')),
                ('username', models.CharField(max_length=100, verbose_name='ユーザーネーム')),
                ('avatar', models.CharField(max_length=200, verbose_name='アイコンリンク')),
                ('data_joined', models.DateTimeField(auto_now_add=True, verbose_name='新規時間')),
                ('is_active', models.BooleanField(default=True, verbose_name='アカウント状態')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
