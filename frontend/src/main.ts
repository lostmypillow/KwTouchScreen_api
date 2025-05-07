import "./style.css";
import 'primeicons/primeicons.css'
import { createApp } from "vue";
import router from "./router";
import { definePreset } from "@primevue/themes";
import PrimeVue from "primevue/config";
import Material from "@primevue/themes/material";
import { autoAnimatePlugin } from "@formkit/auto-animate/vue";
import App from "./App.vue";

const MyPreset = definePreset(Material, {
  semantic: {
    primary: {
      50: "{indigo.50}",
      100: "{indigo.100}",
      200: "{indigo.200}",
      300: "{indigo.300}",
      400: "{indigo.400}",
      500: "{indigo.500}",
      600: "{indigo.600}",
      700: "{indigo.700}",
      800: "{indigo.800}",
      900: "{indigo.900}",
      950: "{indigo.950}",
    },
  },
});

createApp(App)
  .use(router)
  .use(PrimeVue, {
    ripple: true,
    theme: {
      preset: MyPreset,
      options: { darkModeSelector: ".fake-dark-selector" },
    },
  })
  .use(autoAnimatePlugin)
  .mount("#app");
