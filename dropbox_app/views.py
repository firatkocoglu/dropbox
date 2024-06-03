from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.contrib.auth.models import User
from .models import File, Folder, Link
from .forms import RegistrationForm, LoginForm, FileUploadForm, GenerateLinkForm


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
    folders = Folder.objects.filter(user=request.user, linked_folder=None)
    context["folders"] = folders

    # RESET SESSION DATA
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
            extension = data.content_type
            file_size = data.size
            user = request.user
            folder_id = request.session.get("current")
            current_folder = get_object_or_404(Folder, pk=folder_id)
            new_file = File.objects.create(
                user=user,
                file_name=file_name,
                data=data,
                file_size=file_size,
                folder=current_folder,
                extension=extension,
            )
            new_file.save()
    return redirect(renderHome)


@login_required
def renderFolder(request, id):
    context = {}

    # GET CURRENTLY DISPLAYED FOLDER
    current_folder = get_object_or_404(Folder, pk=id)
    context["current"] = current_folder

    # SHARE CURRENT FOLDER ID WITH THE REST OF THE APPLICATION
    request.session["current"] = current_folder.id
    # FILTER FOLDERS INSIDE CURRENTLY DISPLAYED FOLDER - LINKED WITH CURRENT FOLDER
    folders = Folder.objects.filter(user=request.user, linked_folder=id)
    context["folders"] = folders

    # DISPLAY FILES INSIDE CURRENT FOLDER
    files = File.objects.filter(folder=current_folder)
    context["files"] = files

    # DISPLAY FILE UPLOAD FORM
    upload_form = FileUploadForm()
    context["upload_form"] = upload_form
    
    # DISPLAY GENERATE FILE FORM
    link_form = GenerateLinkForm()

    # CHECK IF A SHAREABLE LINK EXISTS FOR THE CURRENT FOLDER
    try:
        link = Link.objects.get(folder=current_folder)
    except Link.DoesNotExist:
        link = None
        

    if link is None:
        context["link_form"] = link_form
    else:
        context["link"] = link
    

    return render(request, "folders.html", context)


@login_required
def createFolder(request):
    if request.method == "POST":
        folder_name = request.POST.get("title")
        user = request.user
        linked_folder_id = request.session.get("current")
        if linked_folder_id:
            linked_folder = Folder.objects.get(pk=linked_folder_id)
            new_folder = Folder.objects.create(
                folder_name=folder_name, user=user, linked_folder=linked_folder
            )
            new_folder.save()
            return redirect("renderFolder", linked_folder_id)
        else:
            new_folder = Folder.objects.create(folder_name=folder_name, user=user)
            new_folder.save()
            return redirect(renderHome)


@login_required
def downloadFile(request, id):
    file = get_object_or_404(File, pk=id)
    file_type = "." + file.extension.split("/")[1]
    file_path = "storage/" + file.file_name + file_type
    response = FileResponse(open(file_path, "rb"), content_type=file.extension)
    return response


@login_required
def generateLink(request):
    if request.method == "POST":
        form = GenerateLinkForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            private = cleaned_data["private"]
            try:
                user = User.objects.get(username=cleaned_data["user"])
            except User.DoesNotExist:
                user = None
                        
            current_folder_id = request.session.get("current")
            current_folder = get_object_or_404(Folder, pk=current_folder_id)

            # GENERATE A UNIQUE SHORT LINK FOR CURRENT FOLDER
            unique_url = get_random_string(10)

            share_link = Link.objects.create(link=unique_url, private=private, folder_id=current_folder_id, allowed_users=user)
            share_link.save()

            return redirect("renderFolder", current_folder_id)


@login_required
def renderLink(request, url):
    try:
        link = Link.objects.get(link=url)
    except Link.DoesNotExist:
        link = None
    
    if link is None:
        raise Http404
    
    if link.allowed_users is not None and request.user != link.allowed_users:
        raise PermissionDenied()
    
    folder_id = link.folder.id
            
    return redirect('renderFolder', folder_id)
