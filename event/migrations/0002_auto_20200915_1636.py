# Generated by Django 2.2.14 on 2020-09-15 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('taggit', '0004_taggeduuiditem'),
        ('message', '0001_initial'),
        ('event', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='grade',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade_events', to='project.Project', verbose_name='通知级别'),
        ),
        migrations.AddField(
            model_name='event',
            name='messages',
            field=models.ManyToManyField(to='message.Message', verbose_name='关联消息'),
        ),
        migrations.AddField(
            model_name='event',
            name='operators',
            field=models.ManyToManyField(blank=True, related_name='operate_events', to=settings.AUTH_USER_MODEL, verbose_name='处理人员'),
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='event',
            name='receivers',
            field=models.ManyToManyField(blank=True, related_name='receive_events', to=settings.AUTH_USER_MODEL, verbose_name='消息接收人'),
        ),
        migrations.AddField(
            model_name='event',
            name='responder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='respond_event', to=settings.AUTH_USER_MODEL, verbose_name='响应人员'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedUUIDItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]