import json


with open('russian-cities.json', encoding='utf-8') as file:
    json_data = json.load(file)


cities = []

for i, data in enumerate(json_data):
    title_city = data['name']

    if title_city in [city['fields']['title'] for city in cities]:
        continue

    new_data = {
        "model": "users.citymodel",
        "pk": len(cities) + 1,
        "fields": {
            "title": title_city
        }
    }
    cities.append(new_data)

cities_json = json.dumps(cities, indent=4, ensure_ascii=False)


with open('cities.json', 'w', encoding='utf-8') as file:
    file.write(cities_json)

