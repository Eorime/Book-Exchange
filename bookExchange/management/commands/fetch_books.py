from django.core.management.base import BaseCommand
from django.core.cache import cache
import requests
import json

class Command(BaseCommand):
    help = 'Fetch books from API and store in cache'

    def handle(self, *args, **options):
        books = []
        API_KEY = "20ce11f3bdfd4e24ae5a07bc3311bb8e"
        base_url = "https://api.bigbookapi.com/search-books"
        
        try:
            params = {
                'api-key': API_KEY, 
                'query': 'all',
                'number': 1000,
                'offset': 1
            }
            
            response = requests.get(base_url, params=params, timeout=20)
            if response.status_code == 200:
                data = response.json()
                books = [book[0] for book in data.get('books', [])]
                
                cache.set('all_books', books, 86400 * 7)  # Cache for a week
                self.stdout.write(self.style.SUCCESS(f'Successfully fetched {len(books)} books'))
            else:
                self.stdout.write(self.style.ERROR(f'Error fetching books: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Request error: {str(e)}'))