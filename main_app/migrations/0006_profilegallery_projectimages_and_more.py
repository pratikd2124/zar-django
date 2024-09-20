# Generated by Django 5.1.1 on 2024-09-20 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0005_remove_materialprovider_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="profile_gallery")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProjectImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="project_images")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="user",
            name="profile_gallery",
        ),
        migrations.RemoveField(
            model_name="user",
            name="project_img",
        ),
        migrations.AlterField(
            model_name="user",
            name="type",
            field=models.CharField(
                choices=[
                    ("Home Ownerr", "Home Owner"),
                    ("Service Provider", "Service Provider"),
                    ("Material Provider", "Material Provider"),
                    ("Community User", "Community User"),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_gallery",
            field=models.ManyToManyField(
                blank=True, null=True, to="main_app.profilegallery"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="project_img",
            field=models.ManyToManyField(
                blank=True, null=True, to="main_app.projectimages"
            ),
        ),
    ]
