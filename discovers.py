import concurrent.futures
import json
import time

import grequests
import requests
from bs4 import BeautifulSoup
import re


urls={'A-ListPop':'https://music.apple.com/us/playlist/a-list-pop/pl.5ee8333dbe944d9f9151e97d92d1ead9',
      'HotTracks':'https://music.apple.com/us/room/1457265758',
      'NewMusicDaily':'https://music.apple.com/us/playlist/new-music-daily/pl.2b0e6e332fdf4b7a91164da3162127b5',
      'PureCalm':'https://music.apple.com/us/playlist/pure-calm/pl.ffc344338c3d4ff394ddcf94d766c143',
      'A-ListPop':'https://music.apple.com/us/playlist/a-list-pop/pl.5ee8333dbe944d9f9151e97d92d1ead9',
      'HotTracks':'https://music.apple.com/us/room/1457265758',
      'NewMusicDaily':'https://music.apple.com/us/playlist/new-music-daily/pl.2b0e6e332fdf4b7a91164da3162127b5',
      'PureCalm':'https://music.apple.com/us/playlist/pure-calm/pl.ffc344338c3d4ff394ddcf94d766c143',
      }

def getSongs(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    m = soup.find_all('div', class_='song-name-wrapper')
    songs = [re.sub('[(]f.*[)]', '', re.sub(' +', ' ', a.text.replace('\n', ''))) for a in m]
    # [print(p) for p in popSongs]
    return songs

def foo(url):
    page=requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    m = soup.find_all('div', class_='song-name-wrapper')
    songs = [re.sub('[(]f.*[)]', '', re.sub(' +', ' ', a.text.replace('\n', ''))) for a in m]
    # [print(p) for p in popSongs]
    return songs

if __name__=='__main__':
    start=time.perf_counter()
    # rs = (grequests.get(u) for u in list(urls.values()))
    # r = grequests.map(rs)

    # songsDict = {}
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     results = executor.map(getSongs, r)
    #
    #     for cate, result in zip(list(urls.keys()), results):
    #         songsDict[cate] = result

    songsDict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(foo, list(urls.values()))

        for cate, result in zip(list(urls.keys()), results):
            songsDict[cate] = result
    stop=time.perf_counter()
    print(json.dumps(songsDict,indent=2))
    print(stop-start)