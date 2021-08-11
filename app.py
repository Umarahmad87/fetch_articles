import requests

# get all the articles list from api
data = requests.get('https://mapping-test.fra1.digitaloceanspaces.com/data/list.json')

# iterating over the list all articles
for record in data.json():
    # get article
    article = requests.get(f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{record["id"]}.json').json()
    # get all media for specific article
    media_list = requests.get(f'https://mapping-test.fra1.digitaloceanspaces.com/data/media/{record["id"]}.json')
    if media_list.status_code == 200:
        media_list = media_list.json()

    # get all sections of particular article
    for section in article['sections']:
        if section.get('text', None):
            print(section['text'])

        if section['type'] == 'media':
            for media in media_list:
                if media['id'] == section['id']:
                    print(media['url'])
                    print(media['caption'])
