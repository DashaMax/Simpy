from bs4 import BeautifulSoup
import os
from datetime import datetime, date
import requests
import json
from random import choice, randint


YEAR_TODAY = date.today().year
MONTH_TODAY = date.today().month if len(str(date.today().month)) == 2 else f'0{date.today().month}'
DAY_TODAY = date.today().day if len(str(date.today().day)) == 2 else f'0{date.today().day}'
TIME_NOW = datetime.now()

FIXTURE_DIR = os.path.normpath('fixtures')
IMAGE_DIR = os.path.normpath(f'books/{YEAR_TODAY}/{MONTH_TODAY}/{DAY_TODAY}')
MEDIA_DIR = os.path.join('media', IMAGE_DIR)

URL_SITE = 'https://www.chitai-gorod.ru'

CATEGORY_MODEL = 'books.categorymodel'
AUTHOR_MODEL = 'books.authormodel'
PUBLISH_MODEL = 'books.publishingmodel'
BOOK_MODEL = 'books.bookmodel'

FILENAME_JSON = [
    'author.json',
    'category.json',
    'publish.json',
    'book.json'
]

LANGUAGE = [
    'ru',
    'en'
]

BINDING = [
    'solid',
    'soft'
]


def get_html(url: str):
    page = requests.get(url)
    print('Status code:', page.status_code)

    if str(page.status_code).startswith('2'):
        return page.text


def get_data_from_html(html: str, tag_name: str, class_name: str):
    soup = BeautifulSoup(html, 'html.parser')
    data_list = soup.findAll(tag_name, class_=class_name)
    return data_list


def write_to_json(filename: str, data: list):
    json_dir = os.path.join(FIXTURE_DIR, filename)
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    with open(json_dir, 'w', encoding='utf-8') as file:
        file.write(json_data)


def save_image(src: str):
    image = requests.get(src).content
    image_name = os.path.basename(src)
    image_dir = os.path.join(MEDIA_DIR, image_name)

    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)

    with open(image_dir, 'wb') as file:
        file.write(image)


def get_data(categories: list):
    category_list = []
    author_list = []
    publishing_list = []
    book_list = []

    for i, category in enumerate(categories):
        # if i > 2:
        #     break

        title_category = category.text.strip()
        url_category = category['href']
        slug_category = '-'.join(url_category.split('/')[-1].split('-')[:-1])
        category_data = {
            'model': CATEGORY_MODEL,
            'pk': i + 1,
            'fields': {
                'title': title_category,
                'slug': slug_category
            }
        }
        category_list.append(category_data)

        html_books_category = get_html(f'{URL_SITE}{url_category}')

        if not html_books_category:
            continue

        data_books = get_data_from_html(html_books_category, 'a', 'product-card__picture')

        for book in data_books:
            url = book['href']
            html_book = get_html(f'{URL_SITE}{url}')

            if not html_book:
                continue

            title = get_data_from_html(html_book, 'h1', 'app-title')
            slug = '-'.join(os.path.basename(url).split('-')[:-1])
            authors = get_data_from_html(html_book, 'a', 'product-detail-title__author')
            description = get_data_from_html(html_book, 'div', 'product-detail-additional__description')
            language = choice(LANGUAGE)
            binding = choice(BINDING)
            pages = randint(300, 700)
            year = randint(2018, 2023)
            publishing_house = get_data_from_html(html_book, 'a', 'product-detail-characteristics__item-value')
            image = get_data_from_html(html_book, 'img', 'product-gallery__image')[0]['src']
            save_image(image)

            if title and authors and publishing_house:
                title = title[0].text.strip()
                authors_list = []
                publishing_house = publishing_house[0].text.strip()
            else:
                continue

            if description:
                description = description[0].text.strip()
            else:
                description = ''

            if title in [t['fields']['title'] for t in book_list]:
                continue

            for author in authors:
                author = author.text.strip()

                if author not in [d_author['fields']['name'] for d_author in author_list] or not author_list:
                    author_id = len(author_list) + 1
                    author_data = {
                        'model': AUTHOR_MODEL,
                        'pk': author_id,
                        'fields': {
                            'name': author.replace(',', '')
                        }
                    }
                    authors_list.append(author_id)
                    author_list.append(author_data)

                else:
                    authors_list.append(
                        [d_author['fields']['name'] for d_author in author_list].index(author) + 1
                    )

            if publishing_house not in [d_publish['fields']['title'] for d_publish in publishing_list] or not publishing_list:
                publish_id = len(publishing_list) + 1
                publish_data = {
                    'model': PUBLISH_MODEL,
                    'pk': publish_id,
                    'fields': {
                        'title': publishing_house
                    }
                }
                publishing_list.append(publish_data)

            else:
                publish_id = [d_publish['fields']['title'] for d_publish in publishing_list].index(publishing_house) + 1

            book_data = {
                'model': BOOK_MODEL,
                'pk': len(book_list) + 1,
                'fields': {
                    'title': title,
                    'slug': slug,
                    'description': description,
                    'language': language,
                    'binding': binding,
                    'pages': pages,
                    'year': year,
                    'image': os.path.join(IMAGE_DIR, os.path.basename(image)),
                    'date_created': str(TIME_NOW).replace(' ', 'T'),
                    'author': authors_list,
                    'category': [
                        i + 1
                    ],
                    'publishing': [
                        publish_id
                    ]
                }
            }
            book_list.append(book_data)

    return author_list, category_list, publishing_list, book_list


def main():
    url = f'{URL_SITE}/catalog/books'
    html = get_html(url)

    if not html:
        return

    data = get_data_from_html(html, 'a', 'catalog-menu__parent--children')
    list_data = get_data(data)

    for i, l in enumerate(list_data):
        write_to_json(FILENAME_JSON[i], l)
    
    
if __name__ == '__main__':
    main()