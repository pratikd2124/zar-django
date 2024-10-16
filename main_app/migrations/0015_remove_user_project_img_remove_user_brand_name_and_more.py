# Generated by Django 5.1.1 on 2024-09-21 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_projectimages_brand_project_img'),
        ('main_app', '0014_user_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='project_img',
        ),
        migrations.RemoveField(
            model_name='user',
            name='brand_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contact_person',
        ),
        migrations.AddField(
            model_name='user',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.brand'),
        ),
        migrations.DeleteModel(
            name='ProjectImages',
        ),
    ]
