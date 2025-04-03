from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.models import LogEntry
from .models import User, CanLend, WillBorrow
from django.db import transaction

class CustomUserAdmin(BaseUserAdmin):
    @transaction.atomic
    def delete_model(self, request, obj):
    # Delete admin log entries related to this user
        from django.contrib.admin.models import LogEntry
        LogEntry.objects.filter(user_id=obj.id).delete()
    
    # Clear permissions and groups
        obj.groups.clear()
        obj.user_permissions.clear()
    
    # Delete related book records
        from .models import CanLend, WillBorrow
        CanLend.objects.filter(user=obj).delete()
        WillBorrow.objects.filter(user=obj).delete()
    
    # Finally delete the user
        obj.delete()

    @transaction.atomic
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

admin.site.register(User, CustomUserAdmin)
admin.site.register(CanLend)
admin.site.register(WillBorrow)