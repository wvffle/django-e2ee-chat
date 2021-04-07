import WindiCSS from 'vite-plugin-windicss'
import { resolve } from 'path'

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
        WindiCSS()
    ],
    server: {
        port: 3001,
        open: false,
        cors: true
    }
};