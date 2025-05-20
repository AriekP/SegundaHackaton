import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Importación global de componentes UI (opcional, si los usas frecuentemente)
import AppAlert from '@/components/ui/AppAlert.vue'
import AppButton from '@/components/ui/AppButton.vue'

// Estilos globales
import '@/assets/main.css'

const app = createApp(App)

// Plugins
app.use(createPinia())
app.use(router)

// Componentes globales (si son usados en múltiples vistas)
app.component('AppAlert', AppAlert)
app.component('AppButton', AppButton)

app.mount('#app')