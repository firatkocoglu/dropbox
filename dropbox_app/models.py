from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    file_name = models.CharField(verbose_name="file name", max_length=255, unique=True)
    extension = models.CharField(verbose_name="file extension", max_length=75)
    data = models.FileField(verbose_name="file", upload_to="storage/")
    file_size = models.CharField(max_length=75)
    folder = models.ForeignKey(
        "Folder", related_name="files", blank=True, null=True, on_delete=models.CASCADE
    )
    link = models.URLField(verbose_name="file share link", blank=True, null=True)
    icon = models.ImageField(
        verbose_name="file icon", default="/static/icons/document.png"
    )
    uploaded_at = models.DateTimeField(auto_now=True)


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # files = models.ForeignKey(File, on_delete=models.CASCADE, related_name="files")
    folder_name = models.CharField(
        verbose_name="folder name", max_length=255, unique=True
    )
    folder_size = models.CharField(max_length=75, default=0)
    linked_folder = models.ForeignKey(
        "self",
        related_name="linked_folders",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    link = models.URLField(verbose_name="file share link", blank=True, null=True)
    icon = models.ImageField(
        verbose_name="folder icon", default="/static/icons/folder.png"
    )
    created_at = models.DateTimeField(auto_now=True)
