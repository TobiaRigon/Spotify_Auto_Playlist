from flask import Flask, request, render_template_string
import os
from utils import authenticate_spotify, get_user_id, create_or_update_playlist, add_tracks_to_playlist

app = Flask(__name__)

FORM_HTML = '''
<!doctype html>
<title>Spotify Auto Playlist</title>
<h1>Imposta le credenziali e la playlist</h1>
<form method=post>
  CLIENT_ID: <input type=text name=client_id required><br>
  CLIENT_SECRET: <input type=text name=client_secret required><br>
  REDIRECT_URI: <input type=text name=redirect_uri value="http://localhost:8888/callback/" required><br>
  Nome Playlist: <input type=text name=playlist_name required><br>
  Descrizione Playlist: <input type=text name=playlist_description><br>
  Pubblica: <input type=checkbox name=playlist_public checked><br>
  Tracce (una per riga):<br>
  <textarea name=tracks rows=10 cols=40></textarea><br>
  <input type=submit value="Crea Playlist">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        redirect_uri = request.form['redirect_uri']
        playlist_name = request.form['playlist_name']
        playlist_description = request.form.get('playlist_description', '')
        playlist_public = 'playlist_public' in request.form
        tracks = [line.strip() for line in request.form.get('tracks', '').splitlines() if line.strip()]

        # Write .env file temporarily
        with open('.env', 'w') as f:
            f.write(f"CLIENT_ID={client_id}\n")
            f.write(f"CLIENT_SECRET={client_secret}\n")
            f.write(f"REDIRECT_URI={redirect_uri}\n")

        sp = authenticate_spotify(client_id, client_secret, redirect_uri)
        user_id = get_user_id(sp)
        playlist_id = create_or_update_playlist(sp, user_id, playlist_name, playlist_description, playlist_public)
        add_tracks_to_playlist(sp, playlist_id, tracks, playlist_name)

        return 'Playlist aggiornata!'
    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(port=5000)
