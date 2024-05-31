from django.urls import path
from .views import register, uploadFile, createFolder, renderFolder, downloadFile

urlpatterns = [
    path("register/", register, name="register"),
    path("upload-file/", uploadFile, name="uploadFile"),
    path("create-folder/", createFolder, name="createFolder"),
    path("render-folder/<str:id>/", renderFolder, name="renderFolder"),
    path("download/<str:id>/", downloadFile, name='downloadFile')
]
