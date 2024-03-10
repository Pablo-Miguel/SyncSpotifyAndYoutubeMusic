import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from googleapiclient.discovery import build


def makeService():
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

            # Save the credentials for the next run
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)

    service = build(serviceName="youtube", version="v3", credentials=credentials)

    return service


def makePlaylist(service, name):
    request = service.playlists().list(part="snippet", mine=True)
    response = request.execute()
    for item in response['items']:
        if item['snippet']['title'] == name:
            print("Playlist already exists - Id: ", item['id'])
            return item['id']

    request = service.playlists().insert(
        part="snippet", body={"snippet": {"title":str(name)}}
    )
    response = request.execute()
    return response['id']


def addItemToPlaylist(service, playlistId, videoIds):
    res = []
    skipTrack = False
    for videoId in videoIds:
        request = service.playlistItems().list(part="snippet",playlistId=playlistId)
        response = request.execute()
        for item in response['items']:
            if item['snippet']['resourceId']['videoId'] == videoId:
                print("Video ", videoId, " already in playlist ", playlistId)
                skipTrack = True
                break

        if not skipTrack:
            request = service.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": str(playlistId),
                        "resourceId": {"kind": "youtube#video", "videoId": videoId},
                    }
                },
            )
            try:
                response = request.execute()
            except HttpError as e:
                print(e.reason)
            print("Video ", videoId, " added to playlist ", playlistId)

        res.append(response)

    return res