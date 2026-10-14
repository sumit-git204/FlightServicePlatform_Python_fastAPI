import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({plugins:[react()],server:{proxy:{'/flights':'http://127.0.0.1:8000','/users':'http://127.0.0.1:8000','/bookings':'http://127.0.0.1:8000','/service-info':{target:'http://127.0.0.1:8000',rewrite:()=> '/'}}}})
