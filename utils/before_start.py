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
    'groups.json',
    'users.json',
    'blogs.json',
    'reviews.json',
    'quotes.json',
    'chats.json',
    'messages.json',
]

for fixture in FIXTURES:
    fixture_path = os.path.join(FIXTURE_DIR, fixture)
    os.system(f'python -Xutf8 manage.py loaddata {fixture_path}')