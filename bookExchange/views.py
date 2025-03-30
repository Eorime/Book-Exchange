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
from django.shortcuts import redirect


def fetch_books(page=1, per_page=100):
    """
    Fetch books with pagination
    page: Which page to fetch (starting from 1)
    per_page: How many books per page (default 100)
    """
    cache_key = f"books_page_{page}"
    cached_page = cache.get(cache_key)
    
    if cached_page:
        print(f"CACHE HIT: Found page {page} in cache with {len(cached_page['books'])} books")
        return cached_page
    
    print(f"CACHE MISS: Fetching page {page} from API")
    
    API_KEY = "20ce11f3bdfd4e24ae5a07bc3311bb8e"
    base_url = "https://api.bigbookapi.com/search-books"
    
    offset = (page - 1) * per_page + 1
    
    try:
        params = {
            'api-key': API_KEY,
            'query': 'all',
            'number': per_page,
            'offset': offset
        }
        
        response = requests.get(base_url, params=params, timeout=50)
        if response.status_code == 200:
            data = response.json()
            books = [book[0] for book in data.get('books', [])]
            
            result = {
                'books': books,
                'total': data.get('available', 0),
                'page': page,
                'per_page': per_page,
                'total_pages': (data.get('available', 0) + per_page - 1) // per_page
            }
            
            # cache this page for 24 hours
            cache.set(cache_key, result, 86400)
            return result
        else:
            print(f"Error fetching books: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    # return empty result if something went wrong
    return {'books': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 0}

def fetch_book_details(book_id):
    cached_book = cache.get(f"book_{book_id}")
    if cached_book:
        return cached_book

    API_KEY = "20ce11f3bdfd4e24ae5a07bc3311bb8e"
    base_url = f"https://api.bigbookapi.com/{book_id}"

    try:
        params = {
            'api-key': API_KEY
        }

        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            book_data = response.json()
            print(f"Received book data: {book_data}")
            
            # cache the book data for 24 hours
            cache.set(f"book_{book_id}", book_data, 86400)
            return book_data
        else:
            print(f"Error fetching book details: {response.status_code}")

    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    return None

# create your views here.

def index(request):
    # fetch the first page with 100 books but only show the first 8
    books_data = fetch_books(page=1, per_page=100)
    firstEight = books_data['books'][:8]
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
            return redirect("browse")
        else:
            print("it wont work")
            return render(request, "login.html", {
                "message": "Invalid username or password", "hide_loader": True
            })
    return render(request, "login.html", {"hide_loader": True})

def logout_view(request):
    logout(request)
    return redirect('index') 

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        mail = request.POST["mail"]

        #confirm password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not mail or not password or not confirmation:
            return render(request, "register.html", {
                "message": "All fields required",
                "hide_loader": True})
        
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords don't match",
                "hide_loader": True
            })
        
        #attempt creating a new user
        try: 
            user = User.objects.create_user(username, mail, password)
            # user.save()

            if "profile_image" in request.FILES:
                user.image = request.FILES["profile_image"]
                user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "User already exists"
            , "hide_loader": True})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html", {"hide_loader": True})

@login_required(login_url="/login", redirect_field_name=None)
def shelf(request):
    user = request.user

    if request.method == "POST":
        # check if an image file was uploaded
        if "profile_image" in request.FILES:
            user.image = request.FILES["profile_image"]
            user.save()

        if "username"in request.POST:
            new_username = request.POST["username"]
            
            if new_username:
                if User.objects.filter(username = new_username).exclude(id = user.id).exists():
                    return render(request, "shelf.html", {
                        "user": user,
                        "message": "Username taken"
                    })
                
                user.username = new_username
                user.save()

        if "delete_image" in request.POST:
            user.image.delete()
            user.save()

        return render(request, "shelf.html", {
            "user": user
        })
    
    return render(request, "shelf.html", {
        "user": user, 

    }) 

def browse(request):
    # Get the requested page number from query parameters
    page = int(request.GET.get('page', 1))
    per_page = 100  # Show 100 books per page
    
    books_data = fetch_books(page=page, per_page=per_page)
    
    return render(request, "browse.html", {
        "books": books_data['books'],
        "current_page": books_data['page'],
        "total_pages": books_data['total_pages'],
        "total_books": books_data['total'],
    })

def book(request, book_id):
    book_details = fetch_book_details(book_id)
    rating = float(book_details['rating']['average']) * 10
    
    if book_details is None:
        # Handle the case where the response is None, maybe return a 404 or a message
        return HttpResponse("Book not found or error occurred", status=404)

    description = book_details['description']
    words = description.split()
    mid = len(words) // 2
    top_half = ' '.join(words[:mid])
    bottom_half = ' '.join(words[mid:])
    
    return render(request, 'book.html', {
        'book': book_details,
        'rating': rating,
        'description_top': top_half,
        'description_bottom': bottom_half
    })