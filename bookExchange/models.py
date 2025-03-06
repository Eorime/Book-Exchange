from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class User(AbstractUser):
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

    image = models.ImageField(
        upload_to='profile_images',
        blank=True,
        null=True,
    )


    def __str__(self):
        return f"{self.username}"
    
class CanLend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lent_books")
    book_id = models.CharField(max_length=13)
    lent_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book_id}"
    
class WillBorrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book_id = models.CharField(max_length=13)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()

    def __str__(self):
        return f"{self.book_id}"
    
    