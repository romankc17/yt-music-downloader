import requests
import re
import webbrowser
import time
import json
from bs4 import BeautifulSoup


ClientAccesToken='CY7q7ubEoVaUdJXMmlAkRPYkB86sK4kK8S33H6cV5ATnrIrIN3TBZkM-e94h0fyW'
headers={"Authorization":'Bearer '+ClientAccesToken}
base_url = 'https://api.genius.com'

def req_content(url):
    headers={
        'content-type':'content-type: text/html; charset=utf-8',
    }
    page=requests.get(url,headers=headers)
    return page

def searchSong(song_title, artist_name):  
    #removing name of featured artist      
    wList=[' feat. ',' ft. ',' featuring ']
    for w in wList:
        if w in song_title.lower():
            rep=re.findall(f'{w}.*',song_title,re.IGNORECASE)[0]
            song_title=song_title.replace(rep,'')
    try:
        rep=re.findall(r'[(].*[)].*',song_title,)[0]
        song_title=song_title.replace(rep,'')
    except :
        pass
    
    for w in wList:
        if w in artist_name.lower():
            print(w)
            rep=re.findall(f'{w}.*',artist_name,re.IGNORECASE)[0]
            print(rep)
            artist_name=artist_name.replace(rep,'')
        
    if ' x ' in artist_name.lower():
        rep=re.findall(f'\sx\s.*',artist_name)[0]
        artist_name=artist_name.replace(rep,'')
        
    # Api end point for searching song
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    print(data)
    response = requests.get(search_url, data=data, headers=headers)

    return response

def songInfo(song_id):
    song_url=base_url+'/songs/'+str(song_id)
    response=requests.get(song_url,headers=headers)
    print(response)
    song_result=response.json()['response']['song']
    return song_result

def albumInfo(album_id):
    album_url=base_url+'/albums/'+str(album_id)
    response=requests.get(album_url,headers=headers)
    print(response)
    song_result=response.json()
    print(json.dumps(song_result, indent=2))
    

def retrieve_lyrics(lPath):
    print('here')
    headers={
        'content-type':'content-type: text/html; charset=utf-8',
    }    
    url='https://genius.com'+lPath
    
    for _ in range(5):
        time.sleep(1)
        page=req_content(url)
        print('Status Code:',page)
        soup=BeautifulSoup(page.text,'html.parser')
        try:
            print(page.url)
            print(page.history)
            for url in page.history:
                print(url)
            release_date=soup.find_all("span", class_="metadata_unit-info metadata_unit-info--text_only")
            release_date=release_date[0].text
            # lyrics=soup.find('div',class_='lyrics')
            lyrics=soup.find_all('div', {'class': 'lyrics'})[0].text
            return ({
                'lyrics':lyrics.strip(),
                'release_date':release_date
            })
        except Exception as ec :
            ec=ec
            print(ec)
    return ({
            'lyrics':'',
            'release_date':''
        })
    
        
   
def retrieve_fullTitle(full_title):
    found=re.findall(r'\sby.+',full_title)[0]
    found=found.replace('\xa0',' ')
    artist=found[4:]
    
    found=re.findall(r'.+\sby+',full_title)[0]
    title=found[:-2]
    
    return {'artist':artist,
            'title':title}
def retrieve_song(title=str,artist=str):
    result=searchSong(title,artist).json()['response']['hits'][0]['result']
    
    song_id=result['id']
    print(song_id)
    song_info=songInfo(song_id)
    
    release_date=song_info['release_date']
    primary_artist=song_info['primary_artist']['name']
    title=song_info['title']
    
    album=song_info['album']
    if album:
        album_name=album['name']
        album_artist=album['artist']['name']
    else:
        album_name=None
        album_artist=None
    
    _featured_artists=song_info['featured_artists']
    featured_artists=[]
    if _featured_artists:
        for artist in _featured_artists:
            featured_artists.append(artist['name'])
    
    
    
    
    song_art_image_url=result['song_art_image_url']

    lyrics_path=result['path']
       
    rl=retrieve_lyrics(lyrics_path)
    lyrics=rl['lyrics']
    
    return{
           'lyrics':lyrics,
           'song_art_image_url':song_art_image_url,
           'artist':primary_artist,
           'title':title,
           'release_date':release_date,
           'album_name':album_name,
           'featured_artists':featured_artists,
           'album_artist':album_artist,
           }

if __name__=='__main__':
    artist="Bitter Feat. Mulatto"
    title="Queen Naija"
    t=retrieve_song(title=title,artist=artist)
    for i in t:
        print(f'{i}: {t[i]}')
    # res=searchSong(title,artist)
    # res=albumInfo(104614)
    # print(json.dumps(res.json()['response']['hits'][0]['result'],indent=4))
    # print(res.json())

    
    
    
    
    
    
    