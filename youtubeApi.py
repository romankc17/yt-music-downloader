API_KEY='AIzaSyC4suq1pA5XS7YluydsmRXpnB8R83JTwTM'
from googleapiclient.discovery import build

youtube = build('youtube','v3',developerKey=API_KEY)

request = youtube.channels().list()