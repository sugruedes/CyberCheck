# Generated by Django 3.2.5 on 2023-06-26 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0004_auto_20230626_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_committee',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='surname',
        ),
    ]
