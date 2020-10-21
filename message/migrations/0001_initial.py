# Generated by Django 2.2.14 on 2020-10-21 09:19

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_taggeduuiditem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('alert', 'alert'), ('recover', 'recover')], default='alert', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('id', models.CharField(default='0a47b4de815d4dba9ca2f538a41167d0', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('project', models.CharField(max_length=50, verbose_name='项目标识')),
                ('data_source', models.CharField(blank=True, max_length=50, null=True, verbose_name='数据源')),
                ('type', models.CharField(max_length=128, verbose_name='消息标识')),
                ('host', models.CharField(max_length=128, verbose_name='主机标识')),
                ('title', models.CharField(max_length=128, verbose_name='消息标题')),
                ('level', models.PositiveSmallIntegerField(choices=[(0, '警告'), (1, '危险'), (2, '灾难')], verbose_name='消息等级')),
                ('raw', models.TextField(blank=True, null=True, verbose_name='原始数据')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedUUIDItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': '- 消息管理',
                'verbose_name_plural': '- 消息管理',
                'ordering': ['-created'],
            },
        ),
    ]
