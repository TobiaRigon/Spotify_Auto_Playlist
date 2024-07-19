<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <CreatePlaylist />
  </div>
</template>

<script>
import { ref } from 'vue'
import CreatePlaylist from './components/CreatePlaylist.vue'

export default {
  name: 'App',
  components: {
    CreatePlaylist
  },
  setup() {
    const message = ref('Create or Update Spotify Playlist')

    return { message }
  }
}
</script>

<style>
/* Aggiungi i tuoi stili qui */
</style>
