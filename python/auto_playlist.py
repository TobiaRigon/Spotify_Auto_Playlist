import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import logging
from fuzzywuzzy import fuzz
from tracks import tracks_to_search
from tracks import playlist_name
from tracks import playlist_description

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni le credenziali dal file .env
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Autenticazione
scope = 'playlist-modify-private playlist-read-private'
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
except spotipy.SpotifyException as e:
    logging.error(f"Errore durante l'autenticazione: {e}")
    raise

# ID dell'utente
try:
    user_id = sp.current_user()['id']
except spotipy.SpotifyException as e:
    logging.error(f"Errore durante il recupero dell'ID utente: {e}")
    raise

# Funzione per ottenere gli URI delle tracce
def get_track_uri(track_name):
    try:
        results = sp.search(q=track_name, type='track', limit=1)
        items = results['tracks']['items']
        if items:
            track = items[0]
            track_title = track['name'].lower()
            track_artists = [artist['name'].lower() for artist in track['artists']]
            
            # Separare il titolo della traccia dall'artista, se specificato
            if ' - ' in track_name:
                search_title, search_artist = track_name.lower().split(' - ', 1)
                artist_match = any(fuzz.partial_ratio(search_artist, artist) > 40 for artist in track_artists)
                if fuzz.partial_ratio(track_title, search_title) > 40 and artist_match:
                    return track['uri']
            else:
                search_title = track_name.lower()
                if fuzz.partial_ratio(track_title, search_title) > 40:
                    return track['uri']
                
            # Check for closest match
            if fuzz.partial_ratio(track_title, search_title) > 40:
                logging.warning("Track '%s' not found. Closest match: '%s' by %s", track_name, track_title, ', '.join(track_artists))
                return track['uri']
            else:
                logging.warning("Track '%s' not found. Closest match: '%s' by %s", track_name, track_title, ', '.join(track_artists))
                return None
        else:
            logging.warning("Track '%s' not found.", track_name)
            return None
    except spotipy.SpotifyException as e:
        logging.error("Errore durante la ricerca della traccia '%s': %s", track_name, e)
        return None

# Funzione per cercare una playlist esistente con gestione della paginazione
def find_playlist_by_name(playlist_name):
    try:
        logging.info("Checking existing playlists for a match...")
        playlists = sp.current_user_playlists(limit=50)
        while playlists:
            for playlist in playlists['items']:
                playlist_name_trimmed = playlist_name.strip().lower()
                existing_playlist_name_trimmed = playlist['name'].strip().lower()
                if existing_playlist_name_trimmed == playlist_name_trimmed:
                    logging.info("Found matching playlist by name: '%s' (ID: %s)", playlist['name'], playlist['id'])
                    return playlist['id']
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None
        logging.info("No matching playlist found for name: '%s'", playlist_name)
        return None
    except spotipy.SpotifyException as e:
        logging.error("Errore durante la ricerca della playlist '%s': %s", playlist_name, e)
        return None

# Cerca la playlist
playlist_id = find_playlist_by_name(playlist_name)

# Se la playlist non esiste, creala come privata
if playlist_id is None:
    try:
        playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=playlist_description)
        playlist_id = playlist['id']
        logging.info("Created new playlist '%s' with ID %s", playlist_name, playlist_id)
    except spotipy.SpotifyException as e:
        logging.error("Errore durante la creazione della playlist '%s': %s", playlist_name, e)
        raise
else:
    logging.info("Updating existing playlist '%s' with ID %s", playlist_name, playlist_id)
    try:
        # Aggiorna la descrizione della playlist esistente
        sp.user_playlist_change_details(user_id, playlist_id, description=playlist_description)
    except spotipy.SpotifyException as e:
        logging.error("Errore durante l'aggiornamento della descrizione della playlist '%s': %s", playlist_name, e)
        raise

# Raccogli gli URI delle tracce
track_uris = []
for track in tracks_to_search:
    track_uri = get_track_uri(track)
    if track_uri:
        track_uris.append(track_uri)

# Sostituisci le tracce nella playlist
try:
    sp.playlist_replace_items(playlist_id, track_uris)
    logging.info("Playlist '%s' updated successfully!", playlist_name)
except spotipy.SpotifyException as e:
    logging.error("Errore durante l'aggiornamento della playlist '%s': %s", playlist_name, e)
    raise
