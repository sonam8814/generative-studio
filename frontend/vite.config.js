import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/generate-2d': 'http://localhost:8000',
      '/generate-3d': 'http://localhost:8000',
      '/models': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    }
  }
})