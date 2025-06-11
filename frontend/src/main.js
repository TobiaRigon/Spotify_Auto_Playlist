import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { state, t } from './i18n'

const app = createApp(App)
app.use(router)
app.provide('langState', state)
app.provide('t', t)
app.mount('#app')
