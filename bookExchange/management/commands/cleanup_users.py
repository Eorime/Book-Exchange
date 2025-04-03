# Create a file called cleanup_users.py in one of your management/commands directories
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Clean up auth_user table data'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # First delete any foreign keys to auth_user
            cursor.execute("DELETE FROM django_admin_log WHERE user_id IN (SELECT id FROM auth_user)")
            cursor.execute("DELETE FROM auth_user_groups WHERE user_id IN (SELECT id FROM auth_user)")
            cursor.execute("DELETE FROM auth_user_user_permissions WHERE user_id IN (SELECT id FROM auth_user)")
            
            # Then delete the auth_user records
            cursor.execute("DELETE FROM auth_user")
            
            self.stdout.write(self.style.SUCCESS('Successfully cleaned up auth_user table'))