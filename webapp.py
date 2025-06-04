from flask import Flask, request, jsonify, render_template
from python.utils import (
    authenticate_spotify,
    get_user_id,
    create_or_update_playlist,
    add_tracks_to_playlist,
    generate_tracks_ai,
    generate_playlist_details_ai,
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    data = request.get_json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    redirect_uri = data.get('redirect_uri')
    playlist_name = data.get('playlist_name')
    playlist_description = data.get('playlist_description', '')
    playlist_public = data.get('playlist_public', False)
    tracks = data.get('tracks', [])

    # Write .env file temporarily
    with open('.env', 'w') as f:
        f.write(f"CLIENT_ID={client_id}\n")
        f.write(f"CLIENT_SECRET={client_secret}\n")
        f.write(f"REDIRECT_URI={redirect_uri}\n")

    sp = authenticate_spotify(client_id, client_secret, redirect_uri)
    user_id = get_user_id(sp)
    playlist_id = create_or_update_playlist(
        sp, user_id, playlist_name, playlist_description, playlist_public
    )
    add_tracks_to_playlist(sp, playlist_id, tracks, playlist_name)

    return jsonify({"status": "success"})


@app.route('/generate_tracks', methods=['POST'])
def generate_tracks():
    data = request.get_json()
    prompt = data.get('prompt', '')
    count = data.get('count', 10)
    tracks = generate_tracks_ai(prompt, count)
    name, description = generate_playlist_details_ai(prompt)
    return jsonify({'tracks': tracks, 'name': name, 'description': description})

if __name__ == '__main__':
    app.run(port=5000)
