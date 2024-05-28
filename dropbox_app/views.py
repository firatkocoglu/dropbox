from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


@login_required
def renderHome(request):
    return render(request, "home.html")


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

# @login_required
def logout(request):
    if request.user.is_authenticated:
        logout(request)
