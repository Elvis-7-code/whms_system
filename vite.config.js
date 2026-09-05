import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});

// export default {
//   server: {
//     proxy: {
//       '/api': {
//         target: 'http://localhost:5000', // wherever your backend runs
//         changeOrigin: true,
//       },
//     },
//   },
// }