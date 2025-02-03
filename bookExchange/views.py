from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError


# Create your views here.

def index(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        mail = request.POST["mail"]

        #confirm password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords don't match"
            })
        
        #attempt creating a new user
        try: 
            user = User.objects.create_user(username, mail, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "User already exists"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

@login_required(login_url="/", redirect_field_name=None)
def shelf(request):
    return render(request, "shelf.html")

def browse(request):
    return render(request, "browse.html")
