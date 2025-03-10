# Spotify Auto Playlist

This project creates and updates a Spotify playlist with a predefined list of tracks using the Spotify Web API and the Spotipy library for Python.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TobiaRigon/Spotify_Auto_Playlist.git
   cd Spotify_Auto_Playlist
   ```

2. Create and activate a virtual environment (optional but recommended):

   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project's root directory with your Spotify credentials:

   ```plaintext
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   REDIRECT_URI=http://localhost:8888/callback
   ```

   - You can obtain your credentials by creating an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

5. Update the playlist name, description, and track list in the `playlist.py` file:

   ```python
   playlist_name = 'Your Playlist Name'
   playlist_description = 'Your Playlist Description'
   tracks_to_search = [
       'Track Name Artist',
       'Track Name Artist',
       # Add more tracks here
   ]
   ```

## Usage

1. Run the script:

   ```bash
   python auto_playlist.py
   ```

2. The script will authenticate with Spotify and create or update the playlist with the specified tracks.

## License

This project is licensed under the MIT License.
