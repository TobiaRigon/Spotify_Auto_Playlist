import { reactive } from 'vue'

export const state = reactive({
  lang: 'en'
})

export const messages = {
  en: {
    nav_home: 'Home',
    nav_about: 'About',
    home_title: 'Spotify Auto Playlist',
    client_id: 'CLIENT_ID',
    client_secret: 'CLIENT_SECRET',
    custom_redirect: 'Custom REDIRECT_URI',
    playlist_name: 'Playlist Name:',
    playlist_description: 'Playlist Description:',
    public: 'Public',
    tracks: 'Tracks (one per line):',
    ai_prompt: 'AI Prompt:',
    placeholder_prompt: 'e.g. 90s Italian rock',
    generate_ai: 'Generate with AI',
    create_playlist: 'Create Playlist',
    generating: 'Generating...',
    success: 'Playlist updated!',
    error: 'Error',
    network_error: 'Network error',
    ai_error: 'AI generation error',
    about_title: 'Application Info',
    about_desc: 'This webapp allows you to create or update a Spotify playlist using the tracks you provide.',
    about_step1: 'Fill in the required fields on the main page with your credentials and playlist name.',
    about_step2: 'List the songs you want to add, one per line.',
    about_step3: 'Press <em>Run</em> to start the process.',
    about_hint: 'If the AI only fills in some fields or the operation fails, it might be due to g4f overload. Try again with the same prompt.',
    disclaimer_title: 'Disclaimer',
    disclaimer_body: '⚠️ This project uses libraries that interact with third-party services in unofficial ways. Using them may violate the terms of service of OpenAI, Google or other providers. This software is provided for educational purposes only and the author takes no responsibility for any misuse.',
    back_home: 'Back to home',
    info_title: 'How to obtain Spotify credentials',
    info_body: '1. Go to <a href="https://developer.spotify.com/dashboard/applications" target="_blank">Spotify Developer Dashboard</a>.<br>2. Log in with your Spotify account and click "Create an App".<br>3. Enter any name and description.<br>4. In the <strong>Redirect URI</strong> section, add: <code>http://localhost:8888/callback/</code><br>5. Open the app details and copy your <strong>Client ID</strong> and <strong>Client Secret</strong>.',
    close: 'Close',
    language: 'Language'
  },
  it: {
    nav_home: 'Home',
    nav_about: 'Info',
    home_title: 'Spotify Auto Playlist',
    client_id: 'CLIENT_ID',
    client_secret: 'CLIENT_SECRET',
    custom_redirect: 'Redirect personalizzato',
    playlist_name: 'Nome Playlist:',
    playlist_description: 'Descrizione Playlist:',
    public: 'Pubblica',
    tracks: 'Tracce (una per riga):',
    ai_prompt: 'Prompt AI:',
    placeholder_prompt: 'es. rock italiano anni 90',
    generate_ai: 'Genera con AI',
    create_playlist: 'Crea Playlist',
    generating: 'Generazione in corso...',
    success: 'Playlist aggiornata!',
    error: 'Errore',
    network_error: 'Errore di rete',
    ai_error: 'Errore generazione AI',
    about_title: "Informazioni sull'applicazione",
    about_desc: 'Questa webapp consente di creare o aggiornare una playlist Spotify in base alle tracce fornite.',
    about_step1: 'Compila i campi richiesti nella pagina principale inserendo le tue credenziali e il nome della playlist.',
    about_step2: 'Elenca le canzoni che desideri aggiungere, una per riga.',
    about_step3: 'Premi <em>Esegui</em> per avviare il processo.',
    about_hint: "Se l'IA compila solo alcuni campi o l'operazione sembra non andare a buon fine, potrebbe dipendere da un sovraccarico di g4f. In tal caso ripeti la richiesta con lo stesso prompt.",
    disclaimer_title: 'Disclaimer',
    disclaimer_body: '⚠️ Questo progetto utilizza librerie che interagiscono con servizi di terze parti in modi non ufficiali. Il loro utilizzo potrebbe violare i termini di servizio di OpenAI, Google o altri provider. Questo software è fornito a scopo educativo e l\'autore non si assume responsabilità per eventuali usi impropri.',
    back_home: 'Torna alla home',
    info_title: 'Come ottenere le credenziali Spotify',
    info_body: '1. Vai al <a href="https://developer.spotify.com/dashboard/applications" target="_blank">Spotify Developer Dashboard</a>.<br>2. Accedi con il tuo account Spotify e clicca su “Create an App”.<br>3. Inserisci nome e descrizione dell\'app (puoi mettere qualsiasi cosa).<br>4. Durante la creazione, nella sezione <strong>Redirect URI</strong>, inserisci: <code>http://localhost:8888/callback/</code><br>5. Una volta creata l\'app, accedi ai suoi dettagli e copia <strong>Client ID</strong> e <strong>Client Secret</strong>.',
    close: 'Chiudi',
    language: 'Lingua'
  }
}

export function t(key) {
  return messages[state.lang][key] || key
}
