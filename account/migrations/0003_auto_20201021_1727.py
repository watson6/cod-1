# Generated by Django 2.2.14 on 2020-10-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201021_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default='7bb07340a5ab4b93a828ce99204acf3d', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
    ]
