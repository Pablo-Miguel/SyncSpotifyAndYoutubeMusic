from credentials import my_client_secret, my_client_id, yt_api, spotify_playlist_to_sync_id
from spotify_extract import connect, fetch_playlist_by_id, extract_data, query_builder
from ytOauth import makePlaylist, addItemToPlaylist, makeService
from ytapi import getVideoIds


playlist_id = spotify_playlist_to_sync_id


def main():
    print("Starting migration from Spotify to Youtube")
    new_play_id = syncSpotifyToYoutube(playlist_id)
    print("New playlist id: ",new_play_id)
    print("Finished migrating")


def syncSpotifyToYoutube(pl_id):
    api = connect(my_client_id,my_client_secret)
    items_name = fetch_playlist_by_id(api,pl_id)
    name = items_name[1]
    queries = query_builder(extract_data(api,items_name[0]))
    videoIds = getVideoIds(queries,yt_api)
   
    service = makeService()
    new_play_id = makePlaylist(service,name)
    addItemToPlaylist(service,new_play_id,videoIds)
    return new_play_id



main()