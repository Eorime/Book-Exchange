from django.contrib import admin
from .models import User, LentBooks, BorrowedBooks, Wishlist, Favorite

# Register your models here.

admin.site.register(User)
admin.site.register(LentBooks)
admin.site.register(BorrowedBooks)
admin.site.register(Wishlist)
admin.site.register(Favorite)
