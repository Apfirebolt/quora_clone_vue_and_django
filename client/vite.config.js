import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/', 
  server: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: ['src/main.js', './index.html']
    }
  }
})