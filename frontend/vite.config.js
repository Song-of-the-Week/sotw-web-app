import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: false, // Keep console logs
        drop_debugger: false, // Keep debugger statements
      },
      mangle: false, // Prevent variable name mangling
    },
  },
  server: {
    host: '0.0.0.0',
    port: 8080,
    hmr: {
      clientPort: 0, // Matches `auto://0.0.0.0:0/ws`
    },
    allowedHosts: ['frontend', '0.0.0.0', 'localhost'],
    strictPort: true,
    watch: {
      usePolling: true, // important for Docker volume changes
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 8080,
    allowedHosts: ['frontend', '0.0.0.0', 'localhost']
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
