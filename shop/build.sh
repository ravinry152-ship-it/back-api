set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate  # បញ្ជានេះនឹងរត់ដោយខ្លួនវាលើ Render