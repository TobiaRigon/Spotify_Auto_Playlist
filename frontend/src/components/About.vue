<template>
  <h1>Informazioni sull'applicazione</h1>
  <p>
    Questa webapp consente di creare o aggiornare una playlist Spotify in base
    alle tracce fornite.
  </p>
  <ol>
    <li>
      Compila i campi richiesti nella pagina principale inserendo le tue
      credenziali e il nome della playlist.
    </li>
    <li>Elenca le canzoni che desideri aggiungere, una per riga.</li>
    <li>Premi <em>Esegui</em> per avviare il processo.</li>
  </ol>
  <p>
    Se l'IA compila solo alcuni campi o l'operazione sembra non andare a buon
    fine, potrebbe dipendere da un sovraccarico di g4f. In tal caso ripeti la
    richiesta con lo stesso prompt.
  </p>
  <p><strong>Disclaimer</strong></p>
  <p>
    ⚠️ This project uses libraries that interact with third-party services in
    unofficial ways. Using them may violate the terms of service of OpenAI,
    Google or other providers. This software is provided for educational
    purposes only and the author takes no responsibility for any misuse.
  </p>
  <p><a href="{{ url_for('index') }}">Torna alla home</a></p>
</template>

<script setup></script>

<style scoped></style>
