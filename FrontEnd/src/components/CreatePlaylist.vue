<template>
    <div>
      <h2>Create or Update Playlist</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="client_id">Client ID:</label>
          <input type="text" v-model="client_id" required />
        </div>
        <div>
          <label for="client_secret">Client Secret:</label>
          <input type="text" v-model="client_secret" required />
        </div>
        <div>
          <label for="redirect_uri">Redirect URI:</label>
          <input type="text" v-model="redirect_uri" required />
        </div>
        <div>
          <label for="playlist_name">Playlist Name:</label>
          <input type="text" v-model="playlist_name" required />
        </div>
        <div>
          <label for="playlist_description">Playlist Description:</label>
          <input type="text" v-model="playlist_description" required />
        </div>
        <div>
          <label for="tracks">Tracks (comma separated):</label>
          <input type="text" v-model="tracks" required />
        </div>
        <button type="submit">Create/Update Playlist</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CreatePlaylist',
    data() {
      return {
        client_id: '',
        client_secret: '',
        redirect_uri: '',
        playlist_name: '',
        playlist_description: '',
        tracks: ''
      }
    },
    methods: {
      async submitForm() {
        const tracksArray = this.tracks.split(',').map(track => track.trim());
        const response = await fetch('http://127.0.0.1:5000/update_playlist', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            client_id: this.client_id,
            client_secret: this.client_secret,
            redirect_uri: this.redirect_uri,
            playlist_name: this.playlist_name,
            playlist_description: this.playlist_description,
            tracks: tracksArray
          })
        });
        const data = await response.json();
        console.log(data);
      }
    }
  }
  </script>
  
  <style scoped>
  /* Aggiungi i tuoi stili qui */
  </style>
  