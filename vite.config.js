import { defineConfig } from 'vite'
import { resolve } from 'path'

import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'
import liveReload from 'vite-plugin-live-reload'
import ViteIcons, { ViteIconsResolver } from 'vite-plugin-icons'
import ViteComponents from 'vite-plugin-components'

export default defineConfig(({ command, mode }) => {
  return {
    publicDir: 'chat/public',
    base: command === 'serve'
      ? 'https://3001.local.dev/'
      : undefined,

    plugins: [
      vue(),
      {
        name: 'vue2-undraw-compat',
        transform (code, id) {
          if (id.includes('vue2-undraw')) {
            return code.replace(/(import .+?)"vue"$/gm, '$1"../../../vue"')
          }
        }
      },
      ViteComponents({
        dirs: [
          'chat/assets/components',
          'chat/public',
        ],

        extensions: ['vue'],
        customComponentResolvers: [
          ViteIconsResolver(),
          name => {
            if (name.startsWith('Undraw')) return { path: `vue2-undraw/src/components/${name}.vue` }
          }
        ]
      }),
      WindiCSS({
        scan: {
          dirs: ['chat']
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
      cors: true,

      hmr: {
        port: 443,
        host: '3001.local.dev'
      }
    }
  }
})
