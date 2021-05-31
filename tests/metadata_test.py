from spotifyApi import SpotifyApi
from yt import MusicDownloader
import os
m=MusicDownloader('afd')
s = SpotifyApi()
q="dj-khaled let it go"
song = s.get_first_search(q)
m.set_metadata(
    os.path.join(
        'C:\\Users\\roman\\Music\\YtMusics','DJ Khaled - LET IT GO (Official Audio) ft. Justin Bieber, 21 Savage.mp3'),song)
