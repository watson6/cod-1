# Generated by Django 2.2.14 on 2020-10-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converge', '0002_auto_20201021_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burrconverge',
            name='id',
            field=models.CharField(default='6c75a11dc6144db18dbc4e56e8b4708e', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='datetimeconverge',
            name='id',
            field=models.CharField(default='6c75a11dc6144db18dbc4e56e8b4708e', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='timeconverge',
            name='id',
            field=models.CharField(default='6c75a11dc6144db18dbc4e56e8b4708e', max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='id'),
        ),
    ]