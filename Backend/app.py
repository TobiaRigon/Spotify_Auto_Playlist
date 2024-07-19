from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
CORS(app)  # Abilita CORS per permettere al frontend di fare richieste al backend

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API")

@app.route('/update_playlist', methods=['POST'])
def update_playlist():
    data = request.json
    client_id = data['client_id']
    client_secret = data['client_secret']
    redirect_uri = data['redirect_uri']
    playlist_name = data['playlist_name']
    playlist_description = data['playlist_description']
    tracks_to_search = data['tracks']

    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

    # Autentica l'utente su Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope='playlist-modify-private playlist-modify-public'))
    
    user_id = sp.current_user()['id']

    # Cerca o crea la playlist
    playlists = sp.user_playlists(user_id)
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break

    if not playlist_id:
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

    # Cerca le tracce e aggiungile alla playlist
    track_uris = []
    for track in tracks_to_search:
        results = sp.search(q=track, type='track', limit=1)
        items = results['tracks']['items']
        if items:
            track_uris.append(items[0]['uri'])

    sp.user_playlist_replace_tracks(user_id, playlist_id, track_uris)

    return jsonify({"message": "Playlist updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
