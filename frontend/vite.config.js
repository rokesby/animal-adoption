import { defineConfig } from 'vitest/config'
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  optimizeDeps: {
    include: ['@mui/material', '@mui/icons-material','@emotion/react', '@emotion/styled', '@mui/material/Tooltip'],
  },
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), 
      }
    }
  },
  test: {
    globals: true,
    environment: "jsdom",
  },
});
