
import importlib.metadata as importlib_metadata

if not hasattr(importlib_metadata, "packages_distributions"):
    def _packages_distributions():
        return {}

    importlib_metadata.packages_distributions = _packages_distributions

from googleapiclient.discovery import build
import json

from secretKeys import youtube_keys

API_KEY = youtube_keys.API_KEY

class YoutubeApi:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=API_KEY)

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
        items = response.get('items', [])
        if not items:
            return None
        item = items[0]
        snippet = item['snippet']
        statistics=item['statistics']
        thumbnails = snippet['thumbnails']
        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'thumbnails':snippet['thumbnails'],
            'channelTitle':snippet['channelTitle'],
            'viewCount': statistics.get('viewCount', '0'),
            'likeCount': statistics.get('likeCount', '0'),
            'commentCount': statistics.get('commentCount', '0')
        }

if __name__ == '__main__':
    y=YoutubeApi()
    info=y.video_info('ji1eDH-WFQ0')
    print(info)
