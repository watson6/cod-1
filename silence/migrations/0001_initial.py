# Generated by Django 2.2.14 on 2020-09-15 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Silence',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.CharField(default='af1ab0d077ad4317b8d859fa5d214868', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('filter_kwargs', models.TextField(blank=True, null=True, verbose_name='沉默规则')),
                ('ignore_type', models.BooleanField(default=False, verbose_name='忽略类型')),
                ('duration', models.PositiveSmallIntegerField(default=60, verbose_name='沉默时间')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='项目名称')),
            ],
            options={
                'verbose_name': '- 沉默规则',
                'verbose_name_plural': '- 沉默规则',
            },
        ),
    ]
