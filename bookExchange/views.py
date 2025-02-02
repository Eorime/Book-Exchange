from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def index(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def register_view(request):
    return render(request, "register.html")

@login_required(login_url="/", redirect_field_name=None)
def shelf(request):
    return render(request, "shelf.html")
