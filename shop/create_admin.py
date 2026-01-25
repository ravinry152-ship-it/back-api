import os
import django
from django.contrib.auth import get_user_model

# ប្តូរពី 'your_project_name' ទៅជា 'api' តាមឈ្មោះ project របស់អ្នក
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings') 
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'your_password_123' 

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")