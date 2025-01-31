from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def lent(request):
    return render(request, "lent.html")

def borrowed(request):
    return render(request, "borrowed.html")

def shelf(request):
    return render(request, "shelf.html")