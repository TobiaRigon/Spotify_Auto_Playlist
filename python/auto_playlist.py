import logging
from utils import load_env_variables, authenticate_spotify, get_user_id, create_or_update_playlist, add_tracks_to_playlist
from playlist import tracks_to_search, playlist_name, playlist_description, playlist_public

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function that coordinates all operations."""
    # Load environment variables
    client_id, client_secret, redirect_uri = load_env_variables()
    
    # Authenticate user on Spotify
    sp = authenticate_spotify(client_id, client_secret, redirect_uri)
    
    # Get user ID
    user_id = get_user_id(sp)
    
    # Create or update the playlist
    playlist_id = create_or_update_playlist(sp, user_id, playlist_name, playlist_description, playlist_public)
    
    # Add tracks to the playlist
    add_tracks_to_playlist(sp, playlist_id, tracks_to_search, playlist_name)

if __name__ == "__main__":
    main()