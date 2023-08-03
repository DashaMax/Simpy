import os


# Make migrations
os.system('python manage.py makemigrations')

# Migrate
os.system('python manage.py migrate')

# Load fixtures (superuser created on this step)
FIXTURE_DIR = os.path.normpath('fixtures')

FIXTURES = [
    'author.json',
    'category.json',
    'publish.json',
    'book.json',
    'cities.json',
    'users.json',
    'blogs.json',
    'reviews.json',
    'quotes.json',
]

for fixture in FIXTURES:
    fixture_path = os.path.join(FIXTURE_DIR, fixture)
    os.system(f'python -Xutf8 manage.py loaddata {fixture_path}')

# Run server
os.system('python manage.py runserver')
