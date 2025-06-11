<template>
  <div>
    <h1>{{ t('about_title') }}</h1>
    <p>{{ t('about_desc') }}</p>
    <ol>
      <li v-html="t('about_step1')"></li>
      <li>{{ t('about_step2') }}</li>
      <li v-html="t('about_step3')"></li>
    </ol>
    <p>{{ t('about_hint') }}</p>
    <p><strong>{{ t('disclaimer_title') }}</strong></p>
    <p>{{ t('disclaimer_body') }}</p>
    <p><RouterLink to="/">{{ t('back_home') }}</RouterLink></p>
  </div>
</template>

<script setup>
import { inject } from 'vue'
import { RouterLink } from 'vue-router'

const t = inject('t')
</script>

<style scoped></style>
