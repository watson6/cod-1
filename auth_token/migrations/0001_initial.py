# Generated by Django 2.2.14 on 2020-09-15 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='end')),
                ('status', model_utils.fields.StatusField(choices=[('草稿', '草稿'), ('发布', '发布'), ('下架', '下架')], default='草稿', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.CharField(default='af1ab0d077ad4317b8d859fa5d214868', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=50, verbose_name='秘钥名称')),
                ('token', models.CharField(default='a953452234f844e6b0955d7db7716d36', max_length=32, verbose_name='认证秘钥')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '- 密钥认证',
                'verbose_name_plural': '- 密钥认证',
                'ordering': ['owner__username'],
            },
        ),
    ]
