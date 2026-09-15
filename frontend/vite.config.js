import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// No GitHub Pages o site fica em https://rateke.github.io/AcousticBuild/, então
// todo caminho precisa desse prefixo. O workflow de publicação define
// VITE_BASE_PATH; em desenvolvimento continua "/".
export default defineConfig({
  plugins: [react()],
  base: process.env.VITE_BASE_PATH || '/',
})
