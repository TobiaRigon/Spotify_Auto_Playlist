import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from tracks import tracks_to_search

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni le credenziali dal file .env
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Autenticazione
scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# ID dell'utente
user_id = sp.current_user()['id']


# Funzione per ottenere gli URI delle tracce
def get_track_uri(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    items = results['tracks']['items']
    return items[0]['uri'] if items else None

# Funzione per cercare una playlist esistente
def find_playlist_by_name(playlist_name):
    playlists = sp.user_playlists(user_id)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']
    return None

# Cerca la playlist
playlist_id = find_playlist_by_name(playlist_name)

# Se la playlist non esiste, creala
if playlist_id is None:
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=playlist_description)
    playlist_id = playlist['id']
    print(f"Created new playlist '{playlist_name}' with ID {playlist_id}")
else:
    print(f"Found existing playlist '{playlist_name}' with ID {playlist_id}")

# Raccogli gli URI delle tracce
track_uris = [get_track_uri(track) for track in tracks_to_search if get_track_uri(track)]

# Aggiungi le tracce alla playlist (puoi rimuovere le tracce esistenti se desideri)
sp.user_playlist_replace_tracks(user_id, playlist_id, track_uris)

print(f"Playlist '{playlist_name}' updated successfully!")
