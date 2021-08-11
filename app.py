import requests

data = requests.get('https://mapping-test.fra1.digitaloceanspaces.com/data/list.json')

for record in data.json():
    article = requests.get(f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{record["id"]}.json').json()
    media_list = requests.get(f'https://mapping-test.fra1.digitaloceanspaces.com/data/media/{record["id"]}.json')
    if media_list.status_code == 200:
        media_list = media_list.json()

    for section in article['sections']:
        if section.get('text', None):
            print(section['text'])

        if section['type'] == 'media':
            for media in media_list:
                if media['id'] == section['id']:
                    print(media['url'])
                    print(media['caption'])
