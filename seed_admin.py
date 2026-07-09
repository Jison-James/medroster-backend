import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medRoster.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# 1. Create standard admin
admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@medroster.com')
admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@1234!')

if not User.objects.filter(username=admin_username).exists():
    print(f"Creating default admin user: {admin_username}")
    admin_user = User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
    admin_user.role = 'manager'
    admin_user.save()
    print("Admin user created successfully!")
else:
    print("Admin user already exists. Skipping creation.")

# 2. Create specific manager account requested by user
manager_email = 'manager@gmail.com'
manager_password = 'medroster123'

if not User.objects.filter(email=manager_email).exists():
    print(f"Creating manager user: {manager_email}")
    manager = User.objects.create_user(
        username=manager_email.split('@')[0],
        email=manager_email,
        password=manager_password,
    )
    manager.role = 'manager'
    manager.save()
    print("Manager user created successfully!")
else:
    # If they already created it in the admin but it's broken, fix it!
    manager = User.objects.get(email=manager_email)
    manager.set_password(manager_password)
    manager.role = 'manager'
    manager.save()
    print("Manager user already existed - fixed password and role!")
