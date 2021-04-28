import { defineConfig } from 'vite'
import { resolve } from 'path'

import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'
import liveReload from 'vite-plugin-live-reload'
import svgLoader from 'vite-svg-loader'
import ViteIcons, { ViteIconsResolver } from 'vite-plugin-icons'
import ViteComponents from 'vite-plugin-components'

export default defineConfig(({
  base: 'http://localhost:3001/',
  publicDir: 'chat/public',

  plugins: [
    vue(),
    svgLoader(),
    ViteComponents({
      dirs: [
        'chat/assets/components',
        'chat/public',
      ],

      extensions: ['vue', 'svg'],
      customComponentResolvers: [
        ViteIconsResolver(),
        name => {
          if (name.startsWith('Undraw')) return { path: `vue2-undraw/src/components/${name}.vue` }
        }
      ]
    }),
    WindiCSS({
      scan: {
        dirs: ['chat/assets', 'chat/templates', 'chat/public']
      }
    }),
    liveReload('./**/*.py'),
    ViteIcons(),
  ],

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

  server: {
    port: 3001,
    open: false,
    cors: true
  }
}))
