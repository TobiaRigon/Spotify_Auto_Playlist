import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env_variables():
    """Loads environment variables from the .env file and checks their presence."""
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    
    if not client_id:
        logging.error("CLIENT_ID is not set in the .env file")
        raise ValueError("CLIENT_ID is not set in the .env file")
    if not client_secret:
        logging.error("CLIENT_SECRET is not set in the .env file")
        raise ValueError("CLIENT_SECRET is not set in the .env file")
    if not redirect_uri:
        logging.error("REDIRECT_URI is not set in the .env file")
        raise ValueError("REDIRECT_URI is not set in the .env file")

    return client_id, client_secret, redirect_uri

def authenticate_spotify(client_id, client_secret, redirect_uri):
    """Authenticates the user on Spotify using the provided credentials."""
    scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri=redirect_uri,
                                                       scope=scope))
        return sp
    except spotipy.SpotifyException as e:
        logging.error(f"Error during authentication: {e}")
        raise

def get_user_id(sp):
    """Retrieves the authenticated Spotify user's ID."""
    try:
        user_id = sp.current_user()['id']
        return user_id
    except spotipy.SpotifyException as e:
        logging.error(f"Error retrieving user ID: {e}")
        raise

def get_track_uri(sp, track_name):
    """Retrieves the URI of a track on Spotify given a search string."""
    try:
        results = sp.search(q=track_name, type='track', limit=1)
        items = results['tracks']['items']
        if items:
            track = items[0]
            track_title = track['name'].lower()
            track_artists = [artist['name'].lower() for artist in track['artists']]
            
            # Separate track title from artist if specified
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
        logging.error("Error searching for track '%s': %s", track_name, e)
        return None

def find_playlist_by_name(sp, playlist_name):
    """Searches for an existing playlist by name and returns its ID and visibility."""
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
        logging.error("Error searching for playlist '%s': %s", playlist_name, e)
        return None, None

def create_or_update_playlist(sp, user_id, playlist_name, playlist_description, playlist_public):
    """Creates or updates a playlist on Spotify."""
    playlist_id, is_public = find_playlist_by_name(sp, playlist_name)

    # If the playlist does not exist, create it with the correct visibility
    if playlist_id is None:
        try:
            playlist = sp.user_playlist_create(user_id, playlist_name, public=playlist_public, description=playlist_description)
            playlist_id = playlist['id']
            logging.info("Created new playlist '%s' with ID %s", playlist_name, playlist_id)
        except spotipy.SpotifyException as e:
            logging.error("Error creating playlist '%s': %s", playlist_name, e)
            raise
    else:
        logging.info("Updating existing playlist '%s' with ID %s", playlist_name, playlist_id)
        try:
            # Update the description and visibility of the existing playlist
            sp.user_playlist_change_details(user_id, playlist_id, description=playlist_description, public=playlist_public)
        except spotipy.SpotifyException as e:
            logging.error("Error updating playlist description '%s': %s", playlist_name, e)
            raise

    return playlist_id

def add_tracks_to_playlist(sp, playlist_id, tracks_to_search, playlist_name):
    """Adds tracks to the playlist on Spotify."""
    track_uris = []
    for track in tracks_to_search:
        track_uri = get_track_uri(sp, track)
        if track_uri:
            track_uris.append(track_uri)
    
    try:
        sp.playlist_replace_items(playlist_id, track_uris)
        logging.info("Playlist '%s' updated successfully!", playlist_name)
    except spotipy.SpotifyException as e:
        logging.error("Error updating playlist '%s': %s", playlist_name, e)
        raise
