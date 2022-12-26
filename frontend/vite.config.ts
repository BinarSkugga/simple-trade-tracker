import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {VitePWA} from "vite-plugin-pwa";

// @ts-ignore
import tailwindConfig from './tailwind.config.js'
import resolveConfig from 'tailwindcss/resolveConfig'
const twConfig = resolveConfig(tailwindConfig)

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        VitePWA({
            registerType: 'autoUpdate',
            workbox: {
                globPatterns: ['**/*.{js,css,html,ico,png,svg}']
            },
            manifest: {
                name: 'TradeTracker',
                short_name: 'TradeTracker',
                description: 'Personal tracker to manage portfolios and stocks on Wealthsimple.',
                theme_color: '#FFFFFF',
                icons: [
                    {
                        src: 'pwa-192x192.png',
                        sizes: '192x192',
                        type: 'image/png'
                    },
                    {
                        src: 'pwa-512x512.png',
                        sizes: '512x512',
                        type: 'image/png'
                    }
                ]
            }
        })
    ],
    define: {
        // @ts-ignore
        twPrimary: JSON.stringify(twConfig.theme.colors.primary.DEFAULT)
    },
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
            vue: 'vue/dist/vue.esm-bundler.js',
        }
    }
})
