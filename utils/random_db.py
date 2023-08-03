import os
import randominfo
import json

from random import choice, randint


FIXTURE_DIR = os.path.normpath('fixtures')
IMAGE_USER_DIR = os.path.normpath(f'users/2023/08/01')
IMAGE_BLOG_DIR = os.path.normpath(f'blogs/2023/08/01')

USER_MODEL = 'users.usermodel'
REVIEW_MODEL = 'books.reviewmodel'
BLOG_MODEL = 'blogs.blogmodel'

FILENAME_JSON = [
    'users.json',
    'reviews.json',
    'blogs.json'
]

PASSWORD = 'pbkdf2_sha256$390000$yKZvEahKDI5v28Xds8GN8m$zkjt3ve5f0OoqEP3m2IrrWCkid4b/ZCJCM9cXkr9r+c='
LAST_LOGIN = '2023-08-01T21:52:09.148'
DATE_JOINED = '2023-08-01T21:51:30.460'
SEX = [
    'female',
    'male'
]
IMAGES_USER = ['profile-default.png'] + [os.path.join(IMAGE_USER_DIR, f'{i}.jpg') for i in range(13)]
IMAGES_BLOG = ['blog-default.jpg'] + [os.path.join(IMAGE_BLOG_DIR, f'{i}.jpg') for i in range(13)]

TEXT = '''
    "Луна жёстко стелет" - научно-фантастический роман, в
    котором исследуется борьба за свободу и независимость
    группы людей, живущих на Луне, которые десятилетиями
    эксплуатировались и угнетались Землей. Действие романа
    разворачивается в 2075 году, когда Луна стала тюремной
    колонией для Земли и используется для добычи ресурсов.
    История рассказана с точки зрения компьютерного техника
    по имени Мануэль Гарсия "Манни" О'Келли-Дэвис, который
    живет на Луне и участвует в подпольном движении за
    независимость Луны. Мэнни - неотразимый и общительный
    главный герой, который не является типичным героем, а
    скорее обычным человеком, оказавшимся втянутым в
    революцию.Роман хорошо написан и заставляет задуматься,
    со сложным и увлекательным сюжетом, который держит читателя
    в напряжении на протяжении всего. Одним из наиболее интересных
    аспектов книги является изображение Луны как персонажа самой по себе,
    со своей собственной уникальной культурой и обществом, которые отличаются
    от земных.Персонажи в романе хорошо развиты и запоминаются, каждый со своей
    особой индивидуальностью и мотивациями. Отношения между персонажами также
    хорошо прописаны и придают истории глубину.В целом, "Луна - суровая хозяйка"
    - обязательный к прочтению для любителей научной фантастики классический роман,
    исследующий темы свободы, бунта и революции. Творчество Роберта А. Хайнлайна
    увлекательно и заставляет задуматься, а его изображение Луны и ее обитателей
    одновременно уникально и реалистично.
'''

REVIEW = '''
    Этот роман - одно из самых спорных произведений русской литературы. Кто-то назовёт его шедевром, другие скажут, что невозможно читать, ничего не понятно. Для меня эта книга стала одним из любимых произведений. Несколько сюжетных линий, герои, живущие в разные времена в разных городах, но по сути, по одним и тем же законам. И конечно, бессмертная история любви мастера и Маргариты. Все это не оставит равнодушным любителей вдумчивого чтения.
'''


def write_to_json(json_name: str, data: list):
    json_dir = os.path.join(FIXTURE_DIR, json_name)
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    with open(json_dir, 'w', encoding='utf-8') as file:
        file.write(json_data)


def main():
    users_data = []
    reviews_data = []
    blogs_data = []

    for i in range(20):
        sex = choice(SEX)
        username = randominfo.get_first_name(gender=sex)
        user_data = {
            "model": USER_MODEL,
            "pk": i + 1,
            "fields": {
                "password": PASSWORD,
                "last_login": LAST_LOGIN,
                "is_superuser": choice([True, False]),
                "username": username,
                "first_name": username,
                "last_name": randominfo.get_last_name(),
                "email": f'{username}@mail.ru',
                "is_staff": choice([True, False]),
                "is_active": True,
                "date_joined": DATE_JOINED,
                "slug": username,
                "sex": sex,
                "city": randint(1, 500),
                "image": choice(IMAGES_USER),
                "date_of_birth": randominfo.get_birthdate(_format='%Y-%m-%d'),
                "about": randominfo.get_hobbies(),
                "groups": [],
                "user_permissions": [],
                "book": list(set(randint(1, 50) for _ in range(randint(1, 20))))
            }
        }
        users_data.append(user_data)

        review_data = {
            "model": REVIEW_MODEL,
            "pk": i + 1,
            "fields": {
                "book": randint(1, 500),
                "user": randint(1, 20),
                "review": REVIEW,
                "create_date": "2023-08-01T21:54:23.901"
            }
        }
        reviews_data.append(review_data)

        blog_data = {
            "model": BLOG_MODEL,
            "pk": i + 1,
            "fields": {
                "title": f'Луна жёстко стелет {i + 1}',
                "slug": f'article{i + 1}',
                "user": randint(1, 20),
                "image": choice(IMAGES_BLOG),
                "blog": TEXT,
                "create_date": "2023-08-01T21:52:51.155"
            }
        }
        blogs_data.append(blog_data)

    # write_to_json(FILENAME_JSON[0], users_data)
    write_to_json(FILENAME_JSON[1], reviews_data)
    write_to_json(FILENAME_JSON[2], blogs_data)


if __name__ == '__main__':
    main()