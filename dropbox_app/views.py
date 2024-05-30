from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, FileUploadForm
from django.contrib.auth import authenticate, login, logout
from .models import File, Folder
from django.core.serializers import serialize



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data["username"]
            password = form_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session["username"] = username
                request.session.save()
                return redirect("home/")
            else:
                return render(request, "registration/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})


def logout(request):
    if request.user.is_authenticated:
        logout(request)


@login_required
def renderHome(request):
    # CREATE CONTEXT
    context = {}

    # RENDER TOP LEVEL FOLDERS
    folders = Folder.objects.filter(linked_folder=None)
    context["folders"] = folders
    
    #RESET SESSION DATA
    request.session["current"] = None

    return render(request, "home.html", context)


@login_required
def uploadFile(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            file_name = form_data["title"]
            data = form_data["file"]
            file_size = data.size
            user = request.user
            new_file = File.objects.create(
                user=user, file_name=file_name, data=data, file_size=file_size
            )
            new_file.save()
    return redirect(renderHome)


@login_required
def renderFolder(request, id):
    current_folder = get_object_or_404(Folder, pk=id)
    request.session['current'] = current_folder.id
    
    folders = Folder.objects.filter(linked_folder=id)
    context = {}
    context["folders"] = folders

    # DISPLAY FILE UPLOAD FORM
    upload_form = FileUploadForm()
    context["upload_form"] = upload_form
    

    return render(request, "folders.html", context)


@login_required
def createFolder(request):
    if request.method == "POST":
        folder_name = request.POST.get("title")
        user = request.user
        linked_folder_id = request.session.get("current")
        if linked_folder_id:
            linked_folder = Folder.objects.get(pk=linked_folder_id)
            new_folder = Folder.objects.create(folder_name=folder_name, user=user, linked_folder=linked_folder)
            new_folder.save()
            return redirect('renderFolder', linked_folder_id)
        else:
            new_folder = Folder.objects.create(folder_name=folder_name, user=user)
            new_folder.save()
            return redirect(renderHome)


