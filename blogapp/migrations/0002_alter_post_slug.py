# Generated by Django 4.1.8 on 2023-05-05 04:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=250, unique_for_date="publish"),
        ),
    ]
