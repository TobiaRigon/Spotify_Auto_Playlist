import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import os

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env_variables():
    """Carica le variabili d'ambiente dal file .env e verifica la loro presenza."""
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    
    if not client_id:
        logging.error("CLIENT_ID non è impostato nel file .env")
        raise ValueError("CLIENT_ID non è impostato nel file .env")
    if not client_secret:
        logging.error("CLIENT_SECRET non è impostato nel file .env")
        raise ValueError("CLIENT_SECRET non è impostato nel file .env")
    if not redirect_uri:
        logging.error("REDIRECT_URI non è impostato nel file .env")
        raise ValueError("REDIRECT_URI non è impostato nel file .env")

    return client_id, client_secret, redirect_uri

def authenticate_spotify(client_id, client_secret, redirect_uri):
    """Autentica l'utente su Spotify utilizzando le credenziali fornite."""
    scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri=redirect_uri,
                                                       scope=scope))
        return sp
    except spotipy.SpotifyException as e:
        logging.error(f"Errore durante l'autenticazione: {e}")
        raise

def get_user_id(sp):
    """Ottiene l'ID dell'utente autenticato su Spotify."""
    try:
        user_id = sp.current_user()['id']
        return user_id
    except spotipy.SpotifyException as e:
        logging.error(f"Errore durante il recupero dell'ID utente: {e}")
        raise

def get_track_uri(sp, track_name):
    """Ottiene l'URI di una traccia su Spotify data una stringa di ricerca."""
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
                artist_match = any(fuzz.partial_ratio(search_artist, artist) > 30 for artist in track_artists)
                if fuzz.partial_ratio(track_title, search_title) > 30 and artist_match:
                    return track['uri']
            else:
                search_title = track_name.lower()
                if fuzz.partial_ratio(track_title, search_title) > 30:
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

def find_playlist_by_name(sp, playlist_name):
    """Cerca una playlist esistente per nome e ritorna il suo ID e visibilità."""
    try:
        logging.info("Checking existing playlists for a match...")
        playlists = sp.current_user_playlists(limit=50)
        while playlists:
            for playlist in playlists['items']:
                playlist_name_trimmed = playlist_name.strip().lower()
                existing_playlist_name_trimmed = playlist['name'].strip().lower()
                if existing_playlist_name_trimmed == playlist_name_trimmed:
                    logging.info("Found matching playlist by name: '%s' (ID: %s)", playlist['name'], playlist['id'])
                    return playlist['id'], playlist['public']
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None
        logging.info("No matching playlist found for name: '%s'", playlist_name)
        return None, None
    except spotipy.SpotifyException as e:
        logging.error("Errore durante la ricerca della playlist '%s': %s", playlist_name, e)
        return None, None

def create_or_update_playlist(sp, user_id, playlist_name, playlist_description, playlist_public):
    """Crea o aggiorna una playlist su Spotify."""
    playlist_id, is_public = find_playlist_by_name(sp, playlist_name)

    # Se la playlist non esiste, creala con la visibilità corretta
    if playlist_id is None:
        try:
            playlist = sp.user_playlist_create(user_id, playlist_name, public=playlist_public, description=playlist_description)
            playlist_id = playlist['id']
            logging.info("Created new playlist '%s' with ID %s", playlist_name, playlist_id)
        except spotipy.SpotifyException as e:
            logging.error("Errore durante la creazione della playlist '%s': %s", playlist_name, e)
            raise
    else:
        logging.info("Updating existing playlist '%s' with ID %s", playlist_name, playlist_id)
        try:
            # Aggiorna la descrizione e la visibilità della playlist esistente
            sp.user_playlist_change_details(user_id, playlist_id, description=playlist_description, public=playlist_public)
        except spotipy.SpotifyException as e:
            logging.error("Errore durante l'aggiornamento della descrizione della playlist '%s': %s", playlist_name, e)
            raise

    return playlist_id

def add_tracks_to_playlist(sp, playlist_id, tracks_to_search, playlist_name):
    """Aggiunge tracce alla playlist su Spotify."""
    track_uris = []
    for track in tracks_to_search:
        track_uri = get_track_uri(sp, track)
        if track_uri:
            track_uris.append(track_uri)
    
    try:
        sp.playlist_replace_items(playlist_id, track_uris)
        logging.info("Playlist '%s' updated successfully!", playlist_name)
    except spotipy.SpotifyException as e:
        logging.error("Errore durante l'aggiornamento della playlist '%s': %s", playlist_name, e)
        raise
