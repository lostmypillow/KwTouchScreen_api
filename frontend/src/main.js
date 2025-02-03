import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material'
import ToastService from 'primevue/toastservice';
createApp(App).use(PrimeVue, {
    theme: {
        preset: Material,
        options: {
            darkModeSelector: '.my-app-dark',
        }
    }
}).use(ToastService).mount('#app')
