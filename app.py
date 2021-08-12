from bs4 import BeautifulSoup

import requests

import models

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
            soup = BeautifulSoup(section['text'])
            section['text'] = soup.get_text()

            if section['type'] == 'title':
                title = models.TitleSection(**section)
                print(title)
            elif section['type'] == 'text':
                text = models.TextSection(**section)
                print(text)

        if section['type'] == 'media':
            for media in media_list:
                if media['id'] == section['id']:

                    if media['type'] == 'media':
                        date_split = media['pub_date'].split('-')
                        date = '-'.join(date_split[0:3])
                        time = ':'.join(date_split[-1].split(';'))
                        media['pub_date'] = f'{date}T{time}'
                        media_data = models.MediaSection(**media)
                        print(media_data)
                    elif media['type'] == 'image':
                        image = models.ImageSection(**media)
                        print(image)
