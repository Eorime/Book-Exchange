from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
import requests

def fetch_books():
    books = []
    start_index = 0
    max_results = 20
    total_limit = 50
    query = "book OR novel OR literature OR fiction"
    lang = "en"

    while start_index < total_limit:
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict={lang}&startIndex={start_index}&maxResults={max_results}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                books.extend(data["items"])
            else:
                break
        else:
            break  

        start_index += max_results

    print(books)
    return books


# Create your views here.

def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index.html"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username or password"
            })
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
    books = fetch_books()  
    return render(request, "browse.html", {
        "books": books
    })