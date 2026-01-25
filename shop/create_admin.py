import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # ប្តូរ your_project_name ជាឈ្មោះ folder settings របស់អ្នក
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'your_password_123' # ដាក់ password ដែលអ្នកចង់ប្រើ

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")