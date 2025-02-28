from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CanLend, WillBorrow 

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(CanLend)
admin.site.register(WillBorrow)
