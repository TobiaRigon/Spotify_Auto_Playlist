markdown

# Spotify Auto Playlist

Questo progetto crea e aggiorna una playlist Spotify con una lista predefinita di tracce utilizzando l'API Web di Spotify, Flask per il backend e Vite con Vue.js per il frontend.

## Installazione

### Backend

1. Clona il repository:

   ```bash
   git clone https://github.com/TobiaRigon/Spotify_Auto_Playlist.git
   cd Spotify_Auto_Playlist

    Naviga nella directory Backend:

    bash

cd Backend

Crea un ambiente virtuale e attivalo (opzionale ma consigliato):

    Windows:

    bash

python -m venv venv
venv\Scripts\activate

Mac/Linux:

bash

    python3 -m venv venv
    source venv/bin/activate

Installa le librerie richieste:

bash

pip install -r requirements.txt

Crea un file .env nella directory Backend con le tue credenziali Spotify:

plaintext

CLIENT_ID=il_tuo_spotify_client_id
CLIENT_SECRET=il_tuo_spotify_client_secret
REDIRECT_URI=http://localhost:8888/callback

    Puoi ottenere le credenziali creando un'applicazione su Spotify Developer Dashboard.

Aggiorna il nome della playlist, la descrizione e la lista delle tracce nel file tracks.py:

python

    playlist_name = 'Nome della tua playlist'
    playlist_description = 'Descrizione della tua playlist'
    tracks_to_search = [
        'Nome Traccia Artista',
        'Nome Traccia Artista',
        # Aggiungi altre tracce qui
    ]

Frontend

    Naviga nella directory FrontEnd:

    bash

cd ../FrontEnd

Installa le dipendenze del progetto:

bash

    npm install

Uso
Avvio del Backend

    Assicurati di essere nella directory Backend e attiva l'ambiente virtuale se non lo è già:
        Windows:

        bash

venv\Scripts\activate

Mac/Linux:

bash

    source venv/bin/activate

Esegui il server Flask:

bash

    python app.py

    Il backend sarà in esecuzione su http://127.0.0.1:5000/.

Avvio del Frontend

    Naviga nella directory FrontEnd ed esegui il server di sviluppo Vite:

    bash

    cd ../FrontEnd
    npm run dev

    Il frontend sarà in esecuzione su http://localhost:3000/.

Verifica

    Apri il tuo browser e naviga a http://localhost:3000/. Dovresti vedere l'interfaccia della tua applicazione Vue.js con i dati della playlist caricati dal backend Flask.

Licenza

Questo progetto è licenziato sotto la Licenza MIT.