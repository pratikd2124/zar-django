# Generated by Django 5.1.1 on 2024-09-21 06:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_user_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
