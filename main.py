from credentials import spotify_client_id, spotify_client_secret, spotify_playlist_to_sync_id, youtube_api
from spotify_service import SpotifyService
from youtube_api_service import YoutubeApiService
from youtube_oauth_service import YoutubeOauthService


spotify_playlist_id_to_migrate = spotify_playlist_to_sync_id


def main():
    print("Starting migration from Spotify to Youtube")
    print("Spotify playlist id: ", spotify_playlist_id_to_migrate)
    youtube_playlist_id = syncSpotifyToYoutube(spotify_playlist_id_to_migrate)
    print("Youtube playlist id: ", youtube_playlist_id)
    print("Finished migrating")


def syncSpotifyToYoutube(playlist_id):
    spotify_service = SpotifyService(spotify_client_id, spotify_client_secret)
    youtube_api_service = YoutubeApiService(youtube_api)
    youtube_oauth_service = YoutubeOauthService()

    spotify_service.connect()
    spotify_service.fetch_playlist_by_id(playlist_id)
    queries_for_youtube = spotify_service.queries_for_youtube_builder()

    youtube_api_service.connect_to_youtube_public_service()
    video_ids = youtube_api_service.get_video_ids_from_queris(queries_for_youtube)

    youtube_oauth_service.connect_via_oauth_to_youtube()
    youtube_oauth_service.upsert_playlist_by_name(spotify_service.get_playlist_name())
    youtube_oauth_service.add_track_to_playlist(video_ids)

    return youtube_oauth_service.get_playlist_id()


main()