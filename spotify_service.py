from spotipy import Spotify

from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyService:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._connection = None
        self._playlist_name = ""
        self._playlist_tracks = []
        self._playlist_data = []
        self._queries = []


    def connect(self):
        self._connection = Spotify(
            auth_manager = SpotifyClientCredentials(
                client_id = self.client_id, client_secret = self.client_secret
            )
        )

        return self._connection


    def fetch_playlist_by_id(self, id):
        playlist_response = self._connection.playlist(playlist_id = id)
        self._playlist_name = playlist_response['name']
        self._playlist_tracks = playlist_response['tracks']['items']
        
        return self.extract_data_from_tracks()


    def extract_data_from_tracks(self):
        for track in self._playlist_tracks:
            data = dict.fromkeys(['track_name','artist_name','album_name'])
            data['track_name'] = track['track']['name']
            data['artist_name'] = track['track']['artists'][0]['name']
            data['album_name'] = track['track']['album']['name']
            self._playlist_data.append(data)

        return self._playlist_data


    def queries_for_youtube_builder(self):
        self._queries = []
        for track in self._playlist_data:
            query = "{} {} {}".format(track['track_name'],track['album_name'],track['artist_name'])
            self._queries.append(query)
        
        return self._queries


    def get_client_id(self):
        return self.client_id
    
    def set_client_id(self, client_id):
        self.client_id = client_id


    def get_client_secret(self):
        return self.client_secret
    

    def set_client_secret(self, client_secret):
        self.client_secret = client_secret


    def get_connection(self):
        return self._connection


    def set_connection(self, connection):
        self._connection = connection


    def get_playlist_name(self):
        return self._playlist_name


    def set_playlist_name(self, name):
        self._playlist_name = name


    def get_playlist_tracks(self):
        return self._playlist_tracks
    

    def set_playlist_tracks(self, tracks):
        self._playlist_tracks = tracks

    
    def get_playlist_data(self):
        return self._playlist_data

    def set_playlist_data(self, data):
        self._playlist_data = data


    def get_queries(self):
        return self._queries
    

    def set_queries(self, queries):
        self._queries = queries