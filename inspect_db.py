from django.db import connection
from django.apps import apps
from django.db.models import ForeignKey
from django.conf import settings

def get_all_foreign_keys_to_user():
    """Find all foreign keys pointing to the User model"""
    user_model = apps.get_model('bookExchange', 'User')
    user_table = user_model._meta.db_table
    results = []

    # Option 1: Using Django's model introspection
    print("=== Foreign keys from Django model introspection ===")
    for model in apps.get_models():
        for field in model._meta.fields:
            if isinstance(field, ForeignKey) and field.related_model == user_model:
                print(f"Model: {model.__name__}, Field: {field.name}, DB Column: {field.column}")
                results.append((model.__name__, field.name, field.column))

    # Option 2: Using SQL (works better for SQLite)
    print("\n=== Foreign keys from SQL introspection ===")
    with connection.cursor() as cursor:
        if connection.vendor == 'sqlite':
            # SQLite - query sqlite_master table
            cursor.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='table' AND sql LIKE '%REFERENCES%'
            """)
            
            for table_name, table_sql in cursor.fetchall():
                if user_table in table_sql:
                    print(f"Table: {table_name}, SQL: {table_sql}")
                    
                    # Get foreign key info
                    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                    for fk_info in cursor.fetchall():
                        if fk_info[2] == user_table:  # Referenced table
                            print(f"  FK from {table_name}.{fk_info[3]} to {fk_info[2]}.{fk_info[4]}")
        
        elif connection.vendor == 'postgresql':
            # PostgreSQL - query information_schema
            cursor.execute("""
                SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, 
                       ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu 
                  ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                  AND ccu.table_name = %s
            """, [user_table])
            
            for row in cursor.fetchall():
                print(f"Table: {row[0]}, Column: {row[1]} references {row[2]}.{row[3]}")
        
        elif connection.vendor == 'mysql':
            # MySQL - query information_schema
            cursor.execute("""
                SELECT table_name, column_name, referenced_table_name, referenced_column_name
                FROM information_schema.key_column_usage
                WHERE referenced_table_schema = %s
                  AND referenced_table_name = %s
            """, [connection.settings_dict['NAME'], user_table])
            
            for row in cursor.fetchall():
                print(f"Table: {row[0]}, Column: {row[1]} references {row[2]}.{row[3]}")

    return results

# Find all tables containing user_id and analyze them
def analyze_tables_with_user_id():
    user_model = apps.get_model('bookExchange', 'User')
    user_table = user_model._meta.db_table
    
    print("\n=== Tables with user_id column ===")
    with connection.cursor() as cursor:
        if connection.vendor == 'sqlite':
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Check each table for user_id column
            for table in tables:
                try:
                    cursor.execute(f"PRAGMA table_info({table});")
                    columns = [row[1] for row in cursor.fetchall()]
                    if 'user_id' in columns:
                        print(f"Table: {table} has user_id column")
                        
                        # Get sample data
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        print(f"  Record count: {count}")
                        
                        if count > 0:
                            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
                            sample = cursor.fetchone()
                            print(f"  Sample data: {sample}")
                except Exception as e:
                    print(f"Error analyzing table {table}: {e}")

# Run the analysis
print("=== Database Structure Analysis ===")
print(f"Django connection: {connection.vendor}")
foreign_keys = get_all_foreign_keys_to_user()
analyze_tables_with_user_id()

# Check for Django-specific tables that may reference users
print("\n=== Django system tables check ===")
from django.contrib.auth.models import User as AuthUser
print(f"Default auth_user table: {AuthUser._meta.db_table}")
print(f"Your custom User table: {apps.get_model('bookExchange', 'User')._meta.db_table}")

# Attempt to check auth_user relationships
try:
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM auth_user")
    count = cursor.fetchone()[0]
    print(f"auth_user table has {count} records")
    if count > 0:
        print("WARNING: You have data in auth_user table even though you're using custom User model")
except Exception as e:
    print(f"auth_user table check error: {e}")

print("\nAnalysis complete. Look for foreign key relationships above.")