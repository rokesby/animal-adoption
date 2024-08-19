import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  test:{
  plugins: [react()],
  globals: true,
  environment: 'jsdom',
  }
})
