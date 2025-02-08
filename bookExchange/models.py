from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='bookexchange_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='bookexchange_user_permissions_set',
        blank=True
    )


    def __str__(self):
        return f"{self.name}"
    
class LentBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lent_books")
    book_id = models.CharField(max_length=13)
    lent_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book_id}"
    
class BorrowedBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book_id = models.CharField(max_length=13)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()

    def __str__(self):
        return f"{self.book_id}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    book_id = models.CharField(max_length=13)
    
    def __str__(self):
        return f"{self.book_id}"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite")
    book_id = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.book_id}"