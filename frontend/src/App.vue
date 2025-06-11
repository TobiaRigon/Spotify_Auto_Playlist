<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { inject } from 'vue'

const langState = inject('langState')
const t = inject('t')
</script>

<template>
  <div id="app" class="container py-3">
    <header class="mb-4">
      <nav class="navbar navbar-expand">
        <RouterLink class="nav-link" to="/" exact>{{ t('nav_home') }}</RouterLink>
        <RouterLink class="nav-link" to="/about">{{ t('nav_about') }}</RouterLink>
        <select v-model="langState.lang" class="form-select w-auto ms-auto">
          <option value="en">English</option>
          <option value="it">Italiano</option>
        </select>
      </nav>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
</style>
