import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medRoster.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@medroster.com')
admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@1234!')

if not User.objects.filter(username=admin_username).exists():
    print(f"Creating default admin user: {admin_username}")
    User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
    print("Admin user created successfully!")
else:
    print("Admin user already exists. Skipping creation.")
