<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <ul>
      <li v-for="track in playlist.tracks" :key="track">{{ track }}</li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const message = ref('Cooling Vibes Playlist')
    const playlist = ref({ tracks: [] })

    onMounted(async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/playlist')
        const data = await response.json()
        playlist.value = data
      } catch (error) {
        console.error('Error fetching playlist:', error)
      }
    })

    return { message, playlist }
  }
}
</script>

<style>
/* Aggiungi i tuoi stili qui */
</style>
