<template>
  <div>
    <h1>Spotify Auto Playlist</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>
          CLIENT_ID <span class="help" @click="showModal=true">?</span>
        </label>
        <input type="text" v-model="client_id" required>
      </div>
      <div class="form-group">
        <label>
          CLIENT_SECRET <span class="help" @click="showModal=true">?</span>
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
    <info-modal v-if="showModal" @close="showModal=false"></info-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      client_id: '',
      client_secret: '',
      redirect_uri: 'http://localhost:8888/callback/',
      custom_redirect: false,
      playlist_name: '',
      playlist_description: '',
      playlist_public: true,
      tracks_text: '',
      ai_prompt: '',
      message: '',
      loading: false,
      showModal: false
    };
  },
  methods: {
    submitForm() {
      const tracks = this.tracks_text.split('\n').map(t => t.trim()).filter(t => t);
      fetch('/create_playlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: this.client_id,
          client_secret: this.client_secret,
          redirect_uri: this.redirect_uri,
          playlist_name: this.playlist_name,
          playlist_description: this.playlist_description,
          playlist_public: this.playlist_public,
          tracks: tracks
        })
      })
      .then(r => r.json())
      .then(data => {
        this.message = data.status === 'success' ? 'Playlist aggiornata!' : 'Errore';
      })
      .catch(() => {
        this.message = 'Errore di rete';
      });
    },
    generateTracks() {
      this.loading = true;
      this.message = '';
      fetch('/generate_tracks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: this.ai_prompt, count: 10 })
      })
      .then(r => r.json())
      .then(data => {
        this.tracks_text = data.tracks.join('\n');
        this.playlist_name = data.name;
        this.playlist_description = data.description;
        this.loading = false;
      })
      .catch(() => {
        this.message = 'Errore generazione AI';
        this.loading = false;
      });
    }
  }
};
</script>

<style scoped>
.help {
  cursor: pointer;
  margin-left: 4px;
  color: #1DB954;
  font-weight: bold;
}
</style>

