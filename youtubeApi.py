API_KEY = 'AIzaSyDPGSStUEhoGIuhylVuK28rZk2c4QntIwU'
from googleapiclient.discovery import build
import json


class YoutubeApi:
    def __init__(self):
        self.youtube = build('Youtube', 'v3', developerKey=API_KEY)

    # method to search youtube videos
    def search(self, q, maxResutls=10):
        request = self.youtube.search().list(
            part='snippet',
            channelType='any',
            maxResults=maxResutls,
            q=q
        )
        response = request.execute()
        items = response['items']
        return items

    def video_info(self, video_id):
        request = self.youtube.videos().list(
            part='snippet,statistics',
            id=video_id,
        )
        response = request.execute()
        item = response['items'][0]
        snippet = item['snippet']
        statistics=item['statistics']
        thumbnails = snippet['thumbnails']
        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'thumbnails':snippet['thumbnails'],
            'channelTitle':snippet['channelTitle'],
            'viewCount':statistics['viewCount'],
            'likeCount':statistics['likeCount'],
            'dislikeCount':statistics['dislikeCount'],
            'commentCount':statistics['commentCount']
        }

if __name__ == '__main__':
    y=YoutubeApi()
    info=y.video_info('ji1eDH-WFQ0')
    print(info)
