import base64
import json

import requests

# Authorization
client_id='3757c5b2008e42a2bf99ce18fa147d90'
client_secret='5fe13571df374ad5a5936fa7cf97ef6b'

# headers={"Authorization":'Bearer '+ClientID}
base_url = 'https://api.spotify.com'

def getToken():
    client_creds = f"{client_id}:{client_secret}"

    # Encode as Base64
    client_creds_b64=base64.b64encode(client_creds.encode())

    token_url='https://accounts.spotify.com/api/token'
    method='POST'
    token_data={
        'grant_type':'client_credentials',
    }
    token_headers={
        'Authorization':f'Basic {client_creds_b64.decode()}'#Basic <base64 encoded client_id:client_secret>
    }

    r=requests.post(token_url, data=token_data,headers=token_headers)

    # valid_request = r.status_code in range(200,299)
    token_response_data=r.json()
    access_token=token_response_data['access_token']

    return access_token

headers = {
        "Authorization": "Bearer " + getToken()
    }

def search(q,*types):
    search_endpoint = base_url + f"/v1/search"
    params={
        'q':q,
        'type': ','.join(type for type in types)
    }
    res = requests.get(search_endpoint, params=params, headers=headers)
    return res

def categories():
    search_endpoint=base_url+"/v1/browse/categories"
    res=requests.get(search_endpoint,headers=headers)
    items=res.json()['categories']['items']
    return items

def categories_playlist(category_id):
    search_endpoint = base_url + "/v1/browse/categories"
    params={
        'category_id':category_id
    }
    res = requests.get(search_endpoint,params=params, headers=headers)

def featuredPlaylist():
    playlistId = "22"
    search_endpoint = base_url + f"/v1/browse/featured-playlists"

    res = requests.get(search_endpoint, headers=headers)

    print(json.dumps(res.json(), indent=2))

def newReleases():
    search_endpoint = base_url + '/v1/browse/new-releases'

    res = requests.get(search_endpoint, headers=headers)

    albums=res.json()['albums']['items']
    # print(albums)
    albumsList=[]
    for index,song in enumerate(albums):
        d={
            'album':song['name'],
            'release_date':song['release_date'],
            'image_url':song['images'][2]['url'],
            'album_id':song['id'],
        }
        albumsList.append(d)
    # print(albumsList)
    return albumsList


if __name__=='__main__':
    # r=categories()[0]
    # print(json.dumps(r,indent=2))
    print(newReleases())