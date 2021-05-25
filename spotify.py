import requests
import base64
import datetime
import json

base_url='https://api.spotify.com'

# Step 1 - Authorization
client_id='3757c5b2008e42a2bf99ce18fa147d90'
client_secret='5fe13571df374ad5a5936fa7cf97ef6b'

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
print(r.json())
valid_request = r.status_code in range(200,299)
token_response_data=r.json()

if valid_request:
    now=datetime.datetime.now()
    access_token=token_response_data['access_token']
    expires_in=token_response_data['expires_in']
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires<now


    # Step 2 - Use Access Token to call playlist endpoint

    playlistId = "22"
    search_endpoint = base_url+f"/v1/tracks/1vvNmPOiUuyCbgWmtc6yfm"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    params={
        'q':'My way Calvin Harris',
        'type':'track',
    }
    
    res = requests.get(search_endpoint, headers=headers)

    print(json.dumps(res.json(), indent=2))

