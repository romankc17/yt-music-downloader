import youtube_dl
import json
import pygame
import requests
import time
ydl_opts={
    'format':'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    # 'outtmpl': '%(id)s',
    'noplaylist' : True,
}
url='https://www.youtube.com/watch?v=zBLrKBaiIkc'
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # ydl.download(['https://www.youtube.com/watch?v=Uk1hv6h7O1Y'])
    song_info = ydl.extract_info(
        url,
        download=False
    )

# # print(json.dumps(meta, indent=3))
# print(meta['artist'])

print(song_info["formats"][0]["url"])



