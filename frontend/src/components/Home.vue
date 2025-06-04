<template>
  <div>
    <h1>Spotify Auto Playlist</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>
          CLIENT_ID <span class="help" @click="showModal = true">?</span>
        </label>
        <input type="text" v-model="client_id" required>
      </div>
      <div class="form-group">
        <label>
          CLIENT_SECRET <span class="help" @click="showModal = true">?</span>
        </label>
        <input type="password" v-model="client_secret" required>
      </div>
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="custom_redirect"> Custom REDIRECT_URI
        </label>
        <input type="text" v-model="redirect_uri" v-if="custom_redirect">
      </div>
      <div class="form-group">
        <label>Nome Playlist:</label>
        <input type="text" v-model="playlist_name" required>
      </div>
      <div class="form-group">
        <label>Descrizione Playlist:</label>
        <input type="text" v-model="playlist_description">
      </div>
      <div class="form-group">
        <label><input type="checkbox" v-model="playlist_public"> Pubblica</label>
      </div>
      <div class="form-group">
        <label>Tracce (una per riga):</label>
        <textarea v-model="tracks_text" rows="10"></textarea>
      </div>
      <div class="form-group">
        <label>Prompt AI:</label>
        <input type="text" v-model="ai_prompt" placeholder="es. rock italiano anni 90">
        <button type="button" @click="generateTracks" :disabled="loading">Genera con AI</button>
      </div>
      <button type="submit">Crea Playlist</button>
    </form>
    <p class="loading" v-if="loading">Generazione in corso...</p>
    <p v-if="message">{{ message }}</p>
    <InfoModal v-if="showModal" @close="showModal = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import InfoModal from './InfoModal.vue'

const client_id = ref('')
const client_secret = ref('')
const redirect_uri = ref('http://localhost:8888/callback/')
const custom_redirect = ref(false)
const playlist_name = ref('')
const playlist_description = ref('')
const playlist_public = ref(true)
const tracks_text = ref('')
const ai_prompt = ref('')
const message = ref('')
const loading = ref(false)
const showModal = ref(false)

function submitForm() {
  const tracks = tracks_text.value.split('\n').map(t => t.trim()).filter(Boolean)
  fetch('/create_playlist', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: client_id.value,
      client_secret: client_secret.value,
      redirect_uri: redirect_uri.value,
      playlist_name: playlist_name.value,
      playlist_description: playlist_description.value,
      playlist_public: playlist_public.value,
      tracks
    })
  })
    .then(r => r.json())
    .then(data => {
      message.value = data.status === 'success' ? 'Playlist aggiornata!' : 'Errore'
    })
    .catch(() => {
      message.value = 'Errore di rete'
    })
}

function generateTracks() {
  loading.value = true
  message.value = ''
  fetch('/generate_tracks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: ai_prompt.value, count: 10 })
  })
    .then(r => r.json())
    .then(data => {
      tracks_text.value = data.tracks.join('\n')
      playlist_name.value = data.name
      playlist_description.value = data.description
      loading.value = false
    })
    .catch(() => {
      message.value = 'Errore generazione AI'
      loading.value = false
    })
}
</script>

<style scoped>
.help {
  cursor: pointer;
  margin-left: 4px;
  color: #1DB954;
  font-weight: bold;
}
</style>
