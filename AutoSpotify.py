import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime


def show_tracks(results):
    saved_tracks_uris = []
    for item in results['items']:
        track = item['track']
        saved_tracks_uris.append(track['uri'])
        print("%32.32s %s" % (track['artists'][0]['name'], track['name']))

    return saved_tracks_uris


scopes = ["user-library-read", "playlist-modify-public", "playlist-modify-public"]
REDIRECT_URI = 'http://localhost:8888/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes, redirect_uri=REDIRECT_URI))
user_id = sp.me()['id']

now_time = datetime.datetime.now()
playlist = f"Liked Songs {now_time.year}-{now_time.month}-{now_time.day} {now_time.hour}:{now_time.minute}"
playlist_id = sp.user_playlist_create(user_id, playlist)['id']

results = sp.current_user_saved_tracks()
uri_list = show_tracks(results)

while results['next']:
    results = sp.next(results)
    uri_list = show_tracks(results)
    sp.playlist_add_items(playlist_id, uri_list)
