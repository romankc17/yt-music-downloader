import requests
import re
import webbrowser
import time
import json
from bs4 import BeautifulSoup
from secretKeys import genius_keys


class GeniusApi():
    def __init__(self):
        ClientAccesToken = genius_keys.ClientAccesToken
        self.headers = {"Authorization": 'Bearer ' + ClientAccesToken}
        self.base_url = 'https://api.genius.com'

    def response(self, endpoint,**kwargs):
        response = requests.get(self.base_url + endpoint, headers=headers)
        return response

    def search(self,q):
        endpoint='/search'
        url=self.base_url+endpoint
        data = {'q': q}
        response = requests.get(url, data=data, headers=self.headers)
        return response.json()

    def get_lyrics(self, artist_name, song_name):
        endpoint = f"/{artist_name.replace(' ', '-')}-{song_name.replace(' ', '-')}-lyrics"
        lyrics = self.retrieve_lyrics(endpoint)
        print(type(lyrics))
        return lyrics

    def retrieve_lyrics(self, lPath):
        print(lPath)
        url = 'https://genius.com' + lPath
        headers = {
            'content-type': 'content-type: text/html; charset=utf-8',
        }
        for i in range(5):
            page = requests.get(url, headers=headers)
            if not page.ok:
                print("Invalid Url")
                return 0
            soup = BeautifulSoup(page.text, 'html.parser')
            try:
                lyrics = soup.find_all('div', {'class': 'lyrics'})[0].text
                album = soup.find_all('div', {'class': 'song_album'})
                if album:
                    # extract album name and artist
                    print(album)
                    album_name = album[0].find_all("a", {'class': 'song_album-info-title'})[0].text.strip()
                    album_artist = album[0].find_all("a", {'class': 'song_album-info-artist'})[0].text.strip()
                    album = {'name': album_name, 'artist': album_artist}
                return {'lyrics': lyrics.strip(), 'album': album}
            except Exception as ec:
                pass


if __name__ == '__main__':
    artist = "laure "
    title = "sabai ho laure "
    g = GeniusApi()
    q=artist+title
    r=g.search(q)['response']['hits'][0]
    print(json.dumps(r,indent=4))
