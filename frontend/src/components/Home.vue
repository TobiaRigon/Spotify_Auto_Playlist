<template>
  <div>
    <h1 class="mb-4">{{ t('home_title') }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label class="form-label">
          {{ t('client_id') }} <span class="help" @click="showModal = true">?</span>
        </label>
        <input type="text" class="form-control" v-model="client_id" required>
      </div>
      <div class="mb-3">
        <label class="form-label">
          {{ t('client_secret') }} <span class="help" @click="showModal = true">?</span>
        </label>
        <input type="password" class="form-control" v-model="client_secret" required>
      </div>
      <div class="form-check mb-3">
        <input class="form-check-input" type="checkbox" id="redirect" v-model="custom_redirect">
        <label class="form-check-label" for="redirect">{{ t('custom_redirect') }}</label>
      </div>
      <div class="mb-3" v-if="custom_redirect">
        <input type="text" class="form-control" v-model="redirect_uri">
      </div>
      <div class="mb-3">
        <label class="form-label">{{ t('playlist_name') }}</label>
        <input type="text" class="form-control" v-model="playlist_name" required>
        <div class="form-text">{{ t('update_note') }}</div>
      </div>
      <div class="mb-3">
        <label class="form-label">{{ t('playlist_description') }}</label>
        <input type="text" class="form-control" v-model="playlist_description">
      </div>
      <div class="form-check mb-3">
        <input class="form-check-input" type="checkbox" id="public" v-model="playlist_public">
        <label class="form-check-label" for="public">{{ t('public') }}</label>
      </div>
      <div class="mb-3">
        <label class="form-label">{{ t('tracks') }}</label>
        <textarea class="form-control" v-model="tracks_text" rows="10"></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">{{ t('ai_prompt') }}</label>
        <div class="input-group">
          <input type="text" class="form-control" v-model="ai_prompt" :placeholder="t('placeholder_prompt')">
          <button type="button" class="btn btn-secondary" @click="generateTracks" :disabled="loading">{{ t('generate_ai') }}</button>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">{{ t('create_playlist') }}</button>
    </form>
    <p class="loading" v-if="loading">{{ t('generating') }}</p>
    <p v-if="message">{{ message }}</p>
    <InfoModal v-if="showModal" @close="showModal = false" />
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import InfoModal from './InfoModal.vue'
const t = inject('t')

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
      message.value = data.status === 'success' ? t('success') : t('error')
    })
    .catch(() => {
      message.value = t('network_error')
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
      message.value = t('ai_error')
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
