<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>Come ottenere le credenziali Spotify</h3>
      <p>
        1. Vai al
        <a
          href="https://developer.spotify.com/dashboard/applications"
          target="_blank"
          >Spotify Developer Dashboard</a
        >.<br />
        2. Accedi con il tuo account Spotify e clicca su “Create an App”.<br />
        3. Inserisci nome e descrizione dell’app (puoi mettere qualsiasi
        cosa).<br />
        4. Durante la creazione, nella sezione <strong>Redirect URI</strong>,
        inserisci: <code>http://localhost:8888/callback/</code><br />
        5. Una volta creata l’app, accedi ai suoi dettagli e copia
        <strong>Client ID</strong> e <strong>Client Secret</strong>.
      </p>
      <button @click="$emit('close')">Chiudi</button>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
}
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
}
</style>
