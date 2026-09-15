import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// Caminho base do site: "/" no computador e na Vercel. Só muda se o site for
// servido dentro de uma subpasta, definindo VITE_BASE_PATH no build.
export default defineConfig({
  plugins: [react()],
  base: process.env.VITE_BASE_PATH || '/',
})
