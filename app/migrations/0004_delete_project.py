# Generated by Django 4.2.7 on 2024-01-18 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_project_delete_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Project',
        ),
    ]