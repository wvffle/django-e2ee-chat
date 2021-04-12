import 'virtual:windi.css'
import 'virtual:windi-devtools'

import App from './App.vue'
import { createApp, h } from 'vue'
import router from './router'


const app = createApp({
  setup: _ => {

  },
  render: _ => h(App)
})

// Devtools
if (process.env.NODE_ENV !== 'production' && '__VUE_DEVTOOLS_GLOBAL_HOOK__' in window) {
  app.config.devtools = true
  // window.__VUE_DEVTOOLS_GLOBAL_HOOK__.Vue = app
}

app.use(router)
app.mount('#app')
