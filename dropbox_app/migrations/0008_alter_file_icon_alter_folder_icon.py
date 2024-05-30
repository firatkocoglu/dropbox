# Generated by Django 5.0.6 on 2024-05-30 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dropbox_app", "0007_folder_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="icon",
            field=models.ImageField(
                default="/static/icons/document.png",
                upload_to="",
                verbose_name="file icon",
            ),
        ),
        migrations.AlterField(
            model_name="folder",
            name="icon",
            field=models.ImageField(
                default="/static/icons/folder.png",
                upload_to="",
                verbose_name="folder icon",
            ),
        ),
    ]
