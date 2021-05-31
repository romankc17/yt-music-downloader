import base64
import re
import requests

from geniusApi import GeniusApi

geniusApi = GeniusApi()


class SpotifyApi:
    def __init__(self):
        # Authorization
        self.client_id = '3757c5b2008e42a2bf99ce18fa147d90'
        self.client_secret = '5fe13571df374ad5a5936fa7cf97ef6b'

        self.base_url = 'https://api.spotify.com'
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
            'Authorization': f'Basic {client_creds_b64.decode()}'  # Basic <base64 encoded client_id:client_secret>
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
        pattern = re.compile(r'(\(|\[).*[remix](\)|\])')
        m = pattern.search(ytTitle)
        if m:
            keys.append(m[0])

        def foo(key):
            # pattern to get featured artist
            pattern = re.compile(r'\s(ft\.?|featuring)\s.*')
            match = pattern.search(key)
            if match:
                key = key.replace(match[0], '')

            # pattern to get brackets
            pattern = re.compile(r'(\(|\[).*(\)|\])')
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
        pattern = re.compile(r'(.*)(-|\||~)(.*)')
        match = pattern.findall(ytTitle)
        if match:
            for key in match[0][::2]:
                foo(key)
        else:
            foo(ytTitle)
        print(keys)
        q = ' '.join(keys)
        return q

    def search(self, q):
        search_endpoint = self.base_url + f"/v1/search"
        params = {
            'q': q,
            'type': 'track,artist,album'
        }
        res = requests.get(search_endpoint, params=params, headers=self.headers).json()
        return res
        result = res['tracks']

    def get_first_search(self, q):
        print(f'Searching: {q}')
        result = self.search(q)['tracks']['items'][0]
        album_artists = [artist['name'] for artist in result['album']['artists']]
        album_name = result['album']['name']
        info = self.get_lyrics(result['name'], album_artists)
        lyrics = ''
        if info:
            album_name = info['album_name']
            lyrics = info['lyrics']
        return {
            'album_name': album_name,
            'album_artists': album_artists,
            'images': result['album']['images'],
            'artists': [artist['name'] for artist in result['artists']],
            'name': result['name'],
            'album_type': result['album']['album_type'],
            'artist_url': result['album']['artists'][0]['external_urls'],
            'track_num': result['track_number'],
            'duration': result['duration_ms'] / 60,
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

        lyrics = geniusApi.get_lyrics(artist, title)

        return lyrics


if __name__ == '__main__':
    api = SpotifyApi()
    ytTitle = 'BTS (방탄소년단) \'Butter\' Official MV (Hotter Remix)'
    q = api.purify_ytTitle(ytTitle)
    print(q)
    # print(json.dumps(api.search(q)['tracks']['items'][0],indent=4))
    # print(api.get_first_search(q))

    title = "BTS (방탄소년단) 'Butter' Official MV (Hotter Remix)"
