# Generated by Django 5.0.6 on 2024-05-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dropbox_app", "0002_alter_file_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="data",
            field=models.FileField(upload_to="storage/", verbose_name="file"),
        ),
    ]
