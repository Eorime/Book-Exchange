from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.models import LogEntry
from .models import User, CanLend, WillBorrow
from django.db import transaction

class CustomUserAdmin(BaseUserAdmin):
    @transaction.atomic
    def delete_model(self, request, obj):
        # delete admin log entries first
        LogEntry.objects.filter(user_id=obj.id).delete()
        
        # delete related objects
        CanLend.objects.filter(user=obj).delete()
        WillBorrow.objects.filter(user=obj).delete()
        
        # clear many-to-many relationships
        obj.groups.clear()
        obj.user_permissions.clear()
        
        # delete the user
        obj.delete()

    @transaction.atomic
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

admin.site.register(User, CustomUserAdmin)
admin.site.register(CanLend)
admin.site.register(WillBorrow)