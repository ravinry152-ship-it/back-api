set -o errexit

# ដំឡើងបណ្ណាល័យ
pip install -r requirements.txt

# ប្រមូល Static files
python manage.py collectstatic --no-input

# រត់ Migration បង្កើតតារាង (សំខាន់សម្រាប់បាត់ Error 500)
python manage.py migrate

# រត់ Script បង្កើត User ស្វ័យប្រវត្តិ
python create_admin.py