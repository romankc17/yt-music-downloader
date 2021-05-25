from pytube import YouTube
from pytube import Playlist
import ffmpeg
import os
import re
import subprocess
import eyed3
from requests.api import request
from replace import regexTitle
import requests
from geniusApi import *
import argparse

dPath="C:/Users/roman/Music/YtMusics"

def getPath(fileName):
    return dPath+'/'+fileName

def chooseMedia(choice,ytd):
    pass

def parseUrl(url):
    print('******Parsing*******')
    ytd=YouTube(url)
    print('*******Finished Parsing***********')
    return ytd

def _fileName(fName):
    _fname= fName.replace(' ','_')
    return _fname

def toMp3(oldFile,newFile):
    
    #exiting if old file doesn't exist
    if not fileExist(oldFile):
        print(f"Doesn't Exist File with filename '{oldFile}'")
        return 0
    
    #deleting new file if it already exist
    _newFile=_fileName(newFile)
    
    if fileExist(_newFile):
        os.remove(_newFile)
    print(oldFile,_newFile)
    
    subprocess.run(f"ffmpeg -i {oldFile} {_newFile}")
    
    if not fileExist(newFile):
        os.rename(_newFile,newFile)
    
    #Removing Old File
    os.remove(oldFile)
    print(newFile)
    return newFile
    
    
def concatVA(vFile,aFile,dFile):
    # print('*******Concating Audio and Video***********')
    # video = ffmpeg.input(videoFile)
    # audio = ffmpeg.input(audioFile)
     # ffmpeg.concat(video,audio,v=1,a=1).output(dFileName).run()
     
    subprocess.run(f"ffmpeg -i {vFile} -i {aFile} -c copy {dFile.replace(' ','-')}")
    os.rename(dFile.replace(' ','-'),dFile)
    
    '''*******Removing audio and video files***********'''
    os.remove(vFile)
    os.remove(aFile)

def fileExist(fileName):
    return os.path.exists(fileName)  

def setMeta(fileName,ytTitle):
    
    params=regexTitle(ytTitle)
    print(params)
    title=params['title']
    artist=params['artist']
    
    song_info=retrieve_song(title=title,artist=artist)
    lyrics=song_info['lyrics'],
    song_art_image_url=song_info['song_art_image_url'],
    artist=song_info['artist'],
    title=song_info['title'],
    release_date=song_info['release_date'],
    album_name=song_info['album_name'],
    featured_artists=song_info['featured_artists'],
    album_artist=song_info['album_artist']
    audioFile=eyed3.load(fileName)
    
    title=song_info['title']
    album_name=song_info['album_name']
    
    artist=song_info['artist']
    featured_artists=song_info['featured_artists']
    
    artist=artist.replace('&',',')
    artists=artist.split(',')
    [artists.append(x) for x in featured_artists]
    artists_name = '; '.join([str(elem).strip() for elem in artists])
    
    if album_name:
        audioFile.tag.album=album_name
        audioFile.tag.album_artist=song_info['album_artist']
    
    audioFile.tag.title=title
    audioFile.tag.artist=artists_name
    
    audioFile.tag.release_date=song_info['release_date']
    
    
    art_image=requests.get(song_info['song_art_image_url']).content
    audioFile.tag.images.set(3,art_image,'image/jpeg',song_info['title'])
    audioFile.tag.lyrics.set(song_info['lyrics'])
    print(song_info['lyrics'])
    audioFile.tag.save()
   

def downloadHighVideo(url):
    ytd=parseUrl(url)
        
    defaultFile=ytd.streams.first().default_filename
    default_name=ytd.title
    videoFile=default_name.replace(' ','_')+'-video.mp4'
    audioFile=default_name.replace(' ','_')+'-audio.mp4'    
    
    if fileExist(audioFile):
        os.remove(audioFile)
        
    if fileExist(videoFile):
        os.remove(videoFile)
    
    if fileExist(defaultFile):
        print("\nFile already exist")
        return 0
    
    print('*******Downloading Video***********')
    video=ytd.streams.filter(adaptive=True).filter(video_codec='vp9').first().download()
    os.rename(defaultFile,videoFile)
    
    print('*******Downloading Audio***********')
    audio=ytd.streams.filter(only_audio=True).first().download()
    os.rename(defaultFile,audioFile)
       
  
def downloadHighAudio(url,*args):
    try:
        for _ in range(3):
            yt=parseUrl(url)
            break
    except Exception as ec:
        print(ec)
        return 0


        
    if fileExist(getPath(yt.title+'.mp3')):
        print("File Already Exist")

        return 0

    
    print('*******Downloading Audio***********')    
    
    defaultFileName=yt.streams.first().default_filename
    
    audioFileName=defaultFileName.replace(' ','_')   
    audioFilePath=getPath(audioFileName)
    
    #getting streams of only audio with highest res
    audio=yt.streams.filter(only_audio=True).first().download(dPath)
    
    #Renaming and deleting if file with that name exist 
    if fileExist(audioFilePath):
        os.remove(audioFilePath)
    os.rename(audio,audioFilePath)
    
    # convert mp4 to mp3
    mp3File=getPath(yt.title+'.mp3')
    print('######Converting to mp3########')
    oldFile=audioFilePath
    newFile=mp3File
    toMp3(oldFile,newFile)
    print('######Converted########')
    
    
    
    print('######Setting Metadata########')
    setMeta(newFile,yt.title)
    print('######Done Setting########')
    
    # # increasing volume level
    # _fName=getPath(yt.title+".mp3").replace(' ','_')
    # subprocess.run(f'ffmpeg -i {mp3File} -filter:a "volume=2" {_fName}')
    # fName=yt.title+".mp3"
    # print(fName)
    # os.rename(_fName,fName)
 
def downloadAudioPlaylist(url):
     p=Playlist(url)
     return p.video_urls
     # for url in p.video_urls:
     #     downloadHighAudio(url)


def downloadUrl(url):
    url=str(url)
    print(url)
    if "playlist" in url:
        print("Downloading Playlist")
        downloadAudioPlaylist(url)
    elif "?list="  in url:
        # return url
        if not'radio' in url:
            print("""Downloading option:
                    1.Download only the song.
                    2.Download the whole Playlist""")
            choice=int(input("Enter the option: "))
            if choice==1:
                downloadHighAudio(url)
            elif choice==2:
                result=re.search(r"list=.*&",url).group(0)
                result=result[5:]
                m=''
                for r in result:
                    if r=='&':
                        break
                    m+=r
                url=m
        else:
            downloadHighAudio(url)
    else:
        print('hi')
        downloadHighAudio(url)
url = "https://youtu.be/3pIlOJrzDvs?list=RDCLAK5uy_nGZRi-an-ruqiZlNJSGhCDHucdp2FBNfI"

if __name__=='__main__':
    # try:
    #     parser=argparse.ArgumentParser()
        
    #     #adding postional parament
    #     parser.add_argument('url',help='Url of Youtube video')
        
    #     args=parser.parse_args()
    #     url=args.url
    # except :
    #     pass
    # downloadUrl(url)
    downloadHighVideo('https://www.youtube.com/watch?v=qCJJwlXv2LU')