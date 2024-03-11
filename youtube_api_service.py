from googleapiclient.discovery import build
import time

class YoutubeApiService:

    def __init__(self, api_key):
        self._api_key = api_key
        self._connection = None
        self._video_ids = []


    def connect_to_youtube_public_service(self):
        self._connection = build(serviceName = 'youtube', version = 'v3', developerKey = self._api_key)
        return self._connection


    def get_video_ids_from_queris(self, queris):
        self._video_ids = []
        for i in range(len(queris)):
            request = self._connection.search().list(
                part="snippet",
                maxResults=2,
                q = queris[i]
            )
            response = request.execute()
            video_id = response['items'][0]['id']['videoId']

            self._video_ids.append(video_id)
            time.sleep(3)
        return self._video_ids
    

    def get_api_key(self):
        return self._api_key
    

    def set_api_key(self, api_key):
        self._api_key = api_key
    

    def get_connection(self):
        return self._connection
    

    def set_connection(self, connection):
        self._connection = connection
    

    def get_video_ids(self):
        return self._video_ids
    

    def set_video_ids(self, video_ids):
        self._video_ids = video_ids