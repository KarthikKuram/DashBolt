# Generated by Django 3.2.4 on 2021-07-11 19:04

from django.db import migrations
from django.contrib.postgres.operations import CITextExtension


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
    ]

    operations = [
        CITextExtension()
    ]
