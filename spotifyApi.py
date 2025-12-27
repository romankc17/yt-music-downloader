import base64
import re
import requests

from geniusApi import GeniusApi
from secretKeys import spotify_keys

geniusApi = GeniusApi()

"""
Extract the song info from the spotify Api
"""
class SpotifyApi:
    def __init__(self):
        # Authorization
        self.client_id = spotify_keys.CLIENT_ID
        self.client_secret = spotify_keys.CLIENT_SECRET

        self.base_url = 'https://api.spotify.com'
        self.headers = None

    def _ensure_headers(self):
        if self.headers is None:
            self.headers = {
                "Authorization": "Bearer " + self.getToken()
            }

    def getToken(self):
        client_creds = f"{self.client_id}:{self.client_secret}"

        # Encode as Base64
        client_creds_b64 = base64.b64encode(client_creds.encode())

        token_url = 'https://accounts.spotify.com/api/token'
        method = 'POST'
        token_data = {
            'grant_type': 'client_credentials',
        }
        token_headers = {
            # Basic <base64 encoded client_id:client_secret>
            'Authorization': f'Basic {client_creds_b64.decode()}'
        }

        r = requests.post(token_url, data=token_data, headers=token_headers)

        # valid_request = r.status_code in range(200,299)
        token_response_data = r.json()
        access_token = token_response_data['access_token']

        return access_token

    # to get a search keyword from youtube title
    def purify_ytTitle(self, ytTitle):
        keys = []
        exception_keys = ['official video', 'official music video', 'official audio', 'official mv', ' mv ']

        ytTitle = ytTitle.lower()

        # to see if it is remix
        pattern = re.compile(r'(\(|\[).*remix(\)|\])')
        m = pattern.search(ytTitle)
        if m:
            keys.append(m[0])
            ytTitle = ytTitle.replace(m[0], '')

        # pattern to get brackets
        pattern = re.compile(r'(\(|\[)[\w\s\.\?\!:\|-]*(\)|\])')
        match = pattern.finditer(ytTitle)
        if match:
            for m in match:
                print(m)
                ytTitle = ytTitle.replace(m.group(0), '')

        def foo(key):
            # pattern to get featured artist
            pattern = re.compile(r'\s(ft\.?|featuring|feature|feat\.?)\s.*')
            match = pattern.search(key)
            if match:
                key = key.replace(match[0], '')

            # remove exception keys
            for ek in exception_keys:
                if ek in key:
                    key = key.replace(ek, '')

            # to remove all words after '|'
            pattern = re.compile(r'\|.*')
            match = pattern.search(key)
            if match:
                key = key.replace(match[0], '')
            key = key.replace(' x ', ', ')
            key = key.replace(' & ', ', ')
            keys.append(key.strip())

        # partition of ytTitle
        pattern = re.compile(r'(^[\w\s$&\.\(\)\[\]!:+\?]*)\s(-|\||~)\s([\w\s$&\.\(\)\[\]\'\"\?]*)')
        match = pattern.findall(ytTitle)
        print(match)
        if match:
            for key in match[0][::2]:
                foo(key)
        else:
            foo(ytTitle)
        return keys

    def search(self, q):
        self._ensure_headers()
        search_endpoint = self.base_url + "/v1/search"
        params = {
            'q': q,
            'type': 'track,artist,album'
        }
        res = requests.get(search_endpoint, params=params, headers=self.headers).json()
        return res

    def get_first_search(self, q):
        items = self.search(q)['tracks']['items']
        if not items:
            return {
                'album_name': '',
                'album_artists': [],
                'images': {'high': {'url': ''}, 'low': {'url': ''}},
                'artists': [],
                'name': "",
                'album_type': '',
                'artist_url': '',
                'track_num': '',
                'duration': 0,
                'release_date': '',
                'lyrics': ''
            }
        result = items[0]
        album_artists = [artist['name'] for artist in result['album']['artists']]
        album_name = result['album']['name']
        info = self.get_lyrics(result['name'], album_artists)
        lyrics = ''
        if info:
            lyrics = info['lyrics']
            if info['album']:
                album_name = info['album']['name']
                album_artists = [info['album']['artist']]
        images = result['album']['images']
        return {
            'album_name': album_name,
            'album_artists': album_artists,
            'images': {
                "high": images[0],
                "low": images[2]
            },
            'artists': [artist['name'] for artist in result['artists']],
            'name': result['name'],
            'album_type': result['album']['album_type'],
            'artist_url': result['album']['artists'][0]['external_urls'],
            'track_num': result['track_number'],
            'duration': result['duration_ms'] / 1000,
            'release_date': result['album']['release_date'],
            'lyrics': lyrics
        }

    def get_lyrics(self, name, album_artists):
        pattern = re.compile(r"(\(|\[).*(\)|\])")
        match = pattern.search(name)
        if match:
            title = name.replace(match[0], '').strip()
        else:
            title = name.strip()

        if len(album_artists) <= 2:
            artist = ' and '.join(album_artists)
        elif len(album_artists) > 2:
            artist = ' '.join(album_artists[:-1]) + ' and ' + album_artists[-1]
        print('here in get lyrics')
        lyrics = geniusApi.get_lyrics(artist, title)

        return lyrics


if __name__ == '__main__':
    api = SpotifyApi()
    ytTitle = 'Nathan Dawe x Anne-Marie x MoStack - Way Too Long [Official Video]'
    q = api.purify_ytTitle(ytTitle)
    print(q)
    # print(json.dumps(api.search(q)['tracks']['items'][0],indent=4))
    print(api.get_first_search(q))
