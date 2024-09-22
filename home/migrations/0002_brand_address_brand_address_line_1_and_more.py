# Generated by Django 5.1.1 on 2024-09-20 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="address_line_1",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="address_line_2",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="contact_person",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="status",
            field=models.CharField(default="Pending", max_length=10),
        ),
        migrations.AddField(
            model_name="brand",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="zip_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
