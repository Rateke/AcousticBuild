import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// Caminho base do site: "/" no computador e na Vercel. Só muda se o site for
// servido dentro de uma subpasta, definindo VITE_BASE_PATH no build.
export default defineConfig({
  plugins: [react()],
  base: process.env.VITE_BASE_PATH || '/',
  // host: true faz o servidor escutar em IPv4 e IPv6. Sem isso o Vite liga só
  // em [::1] no Windows e http://127.0.0.1:5173 responde "não foi possível
  // conectar", mesmo com o servidor no ar.
  server: {
    host: true,
    port: 5173,
  },
})
