import { resolve } from 'path'

import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'
import liveReload from 'vite-plugin-live-reload'

export default {
  build: {
    manifest: true,
    rollupOptions: {
      input: [
        resolve(__dirname, '/chat/assets/main.js'),
      ]
    },
    outDir:  'chat/static',
    assetsDir:  'chat',
  },
  plugins: [
    vue(),
    WindiCSS(),
    liveReload('./**/*.py')
  ],
  server: {
    port: 3001,
    open: false,
    cors: true
  }
};
