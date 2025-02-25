from django.contrib import admin
from .models import User, CanLend, WillBorrow 

# Register your models here.

admin.site.register(User)
admin.site.register(CanLend)
admin.site.register(WillBorrow)
