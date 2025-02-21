from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
import requests
import json
from django.core.cache import cache



def fetch_books():
    cached_books = cache.get("all_books")
    if cached_books:
        print(f"CACHE HIT: Found {len(cached_books)} books in cache")
        return cached_books
    
    print("CACHE MISS: Fetching from API")
    
    books = []
    API_KEY = "20ce11f3bdfd4e24ae5a07bc3311bb8e"
    base_url = "https://api.bigbookapi.com/search-books"
    
    try:
        params = {
            'api-key': API_KEY,
            'query': 'all',
            'number': 100,
            'offset': 1
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Parsed JSON data: {data}")
            # return just the books list with flattened structure, easy to run over
            books = [book[0] for book in data.get('books', [])]
            if books:
                cache.set('all_books', books, 86400)
            return books
        else:
            print(f"Error fetching books: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    return books

# Create your views here.

def index(request):
    books = fetch_books()
    firstEight = books[:8]
    return render(request, "index.html", {
        "books": firstEight
    })

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