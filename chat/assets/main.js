import 'virtual:windi.css'
import 'virtual:windi-devtools'

import App from './App.vue'
import { createApp, h } from 'vue'
import router from './router'

import axios from 'axios'

import { provideToast } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp({
  setup: _ => {
    provideToast({ timeout: 3000 })
  },
  render: _ => h(App)
})

// Devtools
if (process.env.NODE_ENV !== 'production' && '__VUE_DEVTOOLS_GLOBAL_HOOK__' in window) {
  app.config.devtools = true
  // window.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = app
}

// vue2-undraw color
app.config.globalProperties.$vueUndrawColor = '#db2777'

// axios
axios.defaults.headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value

app.use(router)
app.mount('#app')
