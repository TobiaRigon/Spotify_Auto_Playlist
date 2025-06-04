<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <header>
      <nav>
        <RouterLink to="/" exact>Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
</style>
