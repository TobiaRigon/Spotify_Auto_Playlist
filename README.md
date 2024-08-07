# Spotify Auto Playlist

Questo progetto crea e aggiorna una playlist Spotify con una lista predefinita di tracce utilizzando l'API Web di Spotify e la libreria spotipy per Python.

## Installazione

1. Clona il repository:

   ```bash
   git clone https://github.com/TobiaRigon/Spotify_Auto_Playlist.git
   cd Spotify_Auto_Playlist
   ```

2. Crea un ambiente virtuale e attivalo (opzionale ma consigliato):

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

3. Installa le librerie richieste:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea un file `.env` nella directory principale del progetto con le tue credenziali Spotify:

   ```plaintext
   CLIENT_ID=il_tuo_spotify_client_id
   CLIENT_SECRET=il_tuo_spotify_client_secret
   REDIRECT_URI=http://localhost:8888/callback
   ```

   - Puoi ottenere le credenziali creando un'applicazione su [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

5. Aggiorna il nome della playlist, la descrizione e la lista delle tracce nel file `tracks.py`:

   ```python
   playlist_name = 'Nome della tua playlist'
   playlist_description = 'Descrizione della tua playlist'
   tracks_to_search = [
       'Nome Traccia Artista',
       'Nome Traccia Artista',
       # Aggiungi altre tracce qui
   ]
   ```

## Uso

1. Esegui lo script:

   ```bash
   python auto_playlist.py
   ```

2. Lo script si autenticherà con Spotify e creerà o aggiornerà la playlist con le tracce specificate.

## Licenza

Questo progetto è licenziato sotto la Licenza MIT.
