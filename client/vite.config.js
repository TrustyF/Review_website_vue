import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import compression from 'vite-plugin-compression';
import pluginPurgeCss from "@mojojoejo/vite-plugin-purgecss";
import {visualizer } from 'rollup-plugin-visualizer'
import fs from 'fs';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        compression(),
        pluginPurgeCss({
            variables: true}),
        visualizer({
            filename: `dist_stats/stats_${Date.now()}.html`,
            open: false,
            template: 'flamegraph',
        })
    ],
    build: {
        target: "ES2022",
    },
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    }
})
