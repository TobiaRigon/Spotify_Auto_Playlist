<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ t('info_title') }}</h3>
      <p v-html="t('info_body')"></p>
      <button class="btn btn-secondary" @click="$emit('close')">{{ t('close') }}</button>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'
const t = inject('t')
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
