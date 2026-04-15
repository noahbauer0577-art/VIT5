import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendUrl = env.VITE_BACKEND_URL || 'http://localhost:8000'
  const port = parseInt(process.env.PORT || env.PORT || '5000', 10)

  return {
    plugins: [react()],
    build: {
      cssMinify: false,
    },
    server: {
      port,
      host: '0.0.0.0',
      allowedHosts: true,
      proxy: {
        '/predict': backendUrl,
        '/history': backendUrl,
        '/health':  backendUrl,
        '/fetch':   backendUrl,
        '/odds':    backendUrl,
        '/analytics': backendUrl,
        '/training': backendUrl,
        '/admin':   backendUrl,
        '/results': backendUrl,
        '/system':  backendUrl,
        '/ai':      backendUrl,
      },
    },
  }
})
