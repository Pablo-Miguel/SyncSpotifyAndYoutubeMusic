import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from googleapiclient.discovery import build

class YoutubeOauthService:

    def __init__(self):
        self._connection = None
        self._playlist_id = ""
        self._playlist_name = ""

    def connect_via_oauth_to_youtube(self):
        credentials = None

        if os.path.exists("token.pickle"):
            print("Loading Credentials From File...")
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Refreshing Access Token...")
                credentials.refresh(Request())
            else:
                print("Fetching New Tokens...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secrets.json",
                    scopes=["https://www.googleapis.com/auth/youtube"],
                )

                flow.run_local_server(
                    port=8080, prompt="consent", authorization_prompt_message=""
                )
                credentials = flow.credentials

                with open("token.pickle", "wb") as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(credentials, f)

        self._connection = build(serviceName="youtube", version="v3", credentials=credentials)

        return self._connection
    

    def upsert_playlist_by_name(self, name):
        request = self._connection.playlists().list(part = "snippet", mine = True)
        response = request.execute()
        for playlist in response['items']:
            if playlist['snippet']['title'] == name:
                self._playlist_id = playlist['id']
                self._playlist_name = name
                print("Playlist already exists - Id: ", self._playlist_id, " Name: ", self._playlist_name)
                return self._playlist_id

        request = self._connection.playlists().insert(
            part = "snippet", body = {"snippet": {"title": str(name)}}
        )
        response = request.execute()
        self._playlist_id = response['id']
        self._playlist_name = name
        print("Playlist created - Id: ", self._playlist_id, " Name: ", self._playlist_name)
        return self._playlist_id


    def add_track_to_playlist(self, video_ids):
        res = []
        skipTrack = False
        for video_id in video_ids:
            request = self._connection.playlistItems().list(part="snippet", playlistId = self._playlist_id)
            response = request.execute()
            for item in response['items']:
                if item['snippet']['resourceId']['videoId'] == video_id:
                    print("Video ", video_id, " already in playlist ", self._playlist_id)
                    skipTrack = True
                    break

            if not skipTrack:
                request = self._connection.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": str(self._playlist_id),
                            "resourceId": {"kind": "youtube#video", "videoId": video_id},
                        }
                    },
                )
                try:
                    response = request.execute()
                except HttpError as e:
                    print("HttpError: ", e.reason)
                print("Video ", video_id, " added to playlist ", self._playlist_id)

            res.append(response)

        return res
    

    def get_connection(self):
        return self._connection
    

    def set_connection(self, connection):
        self._connection = connection


    def get_playlist_id(self):
        return self._playlist_id
    

    def set_playlist_id(self, playlist_id):
        self._playlist_id = playlist_id

    
    def get_playlist_name(self):
        return self._playlist_name
    

    def set_playlist_name(self, playlist_name):
        self._playlist_name = playlist_name
