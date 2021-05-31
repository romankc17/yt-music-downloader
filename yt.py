import requests
from pytube import YouTube, Playlist
import re
import eyed3
from moviepy.editor import *

from youtubeApi import YoutubeApi

youtube = YoutubeApi()

class MusicDownloader:
    def __init__(self, url):
        self.url = url

        homedir = os.path.expanduser('~')
        self.path = os.path.join(homedir, "Music\\YtMusics")

        self.title = ''

    def link_type(self):
        video_id_pattern = re.compile(r"(v=|/)([a-zA-Z0-9-_]{11})")
        playlist_id_pattern = re.compile(r"list=([a-zA-Z0-9-_]{3,10})")

        video_match = video_id_pattern.findall(self.url)
        playlist_match = playlist_id_pattern.findall(self.url)

        if video_match and playlist_match:
            return {
                'type': 1,
                'video_id': video_match[0][1],
                'playlist_id': playlist_match[0]
            }
        elif video_match:
            return {'type': 2, 'video_id': video_match[0][1]}
        elif playlist_match:
            return {'type': 3, 'playlist_id': playlist_match[0]}
        else:
            return {'type': 0}

    def get_title(self, video_id):
        self.title = youtube.video_info(video_id)['title']
        return self.title

    def mp4_to_mp3(self, video_file, audio_file):
        mp4 = AudioFileClip(os.path.join(self.path, video_file))
        mp3 = mp4.write_audiofile(audio_file)

        # deleting mp4
        os.remove(os.path.join(self.path, video_file))

        return mp3

    def downlod(self, title):
        print('******Parsing*******')
        yt = YouTube(self.url)
        print('*******Finished Parsing***********')

        audio_mp4 = yt.streams.filter(only_audio=True).first().download(self.path)
        mp3_filename = os.path.join(self.path, "music-" + len(title) + ".mp3")
        audio = self.mp4_to_mp3(audio_mp4, mp3_filename)
        os.rename(mp3_filename, os.path.join(self.path, title + ".mp3"))
        return mp3_filename

    # return all the video urls from playlist
    def downloadAudioPlaylist(self):
        p = Playlist(self.url)
        return p.video_urls

    def set_metadata(self, fileName, song_info):
        audioFile = eyed3.load(fileName)

        title = song_info['name']
        album_name = song_info['album_name']
        image_url = song_info['images'][0]['url']

        artists_name = '; '.join(song_info['artists'])

        audioFile.tag.album = album_name
        audioFile.tag.album_artist = "; ".join(song_info['album_artists'])

        audioFile.tag.title = title
        audioFile.tag.artist = artists_name

        audioFile.tag.release_date = song_info['release_date']

        art_image = requests.get(image_url).content
        audioFile.tag.images.set(3, art_image, 'image/jpeg', title)
        audioFile.tag.lyrics.set(song_info['lyrics'])
        audioFile.info.time_secs = song_info['duration']

        audioFile.tag.save()


if __name__ == '__main__':
    url = 'https://youtu.be/9n42tHMWqo'
    obj = MusicDownloader(url)
