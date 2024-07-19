import logging
from utils import load_env_variables, authenticate_spotify, get_user_id, create_or_update_playlist, add_tracks_to_playlist
from playlist import tracks_to_search, playlist_name, playlist_description, playlist_public

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    client_id, client_secret, redirect_uri = load_env_variables()
    sp = authenticate_spotify(client_id, client_secret, redirect_uri)
    user_id = get_user_id(sp)
    playlist_id = create_or_update_playlist(sp, user_id, playlist_name, playlist_description, playlist_public)
    add_tracks_to_playlist(sp, playlist_id, tracks_to_search, playlist_name)

if __name__ == "__main__":
    main()
