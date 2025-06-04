<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>Come ottenere le credenziali Spotify</h3>
      <p>
        Crea un'applicazione sul
        <a href="https://developer.spotify.com/dashboard/applications" target="_blank">Spotify Developer Dashboard</a>
        e copia CLIENT_ID e CLIENT_SECRET.
      </p>
      <button @click="$emit('close')">Chiudi</button>
    </div>
  </div>
</template>

<script>
export default {}
</script>

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

