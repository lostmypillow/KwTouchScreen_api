import "./style.css";
import "primeicons/primeicons.css";
import { createApp } from "vue";
import { createWebHistory, createRouter } from "vue-router";
import { definePreset } from "@primevue/themes";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Listbox from "primevue/listbox";
import InputGroup from "primevue/inputgroup";
import Rating from "primevue/rating";
import ScrollPanel from "primevue/scrollpanel";
import ProgressSpinner from "primevue/progressspinner";
import App from "./App.vue";
import HomePage from "./pages/HomePage.vue";
import AuthPage from "./pages/AuthPage.vue";
import SeatPage from "./pages/SeatPage.vue";
import AlertPage from "./pages/AlertPage.vue";
import SurveyPage from "./pages/SurveyPage.vue";
import { autoAnimatePlugin } from "@formkit/auto-animate/vue";

const routes = [
  {
    path: "/",
    component: HomePage,
  },
  {
    path: "/alert",
    component: AlertPage,
  },
  {
    path: "/auth/:callback",
    component: AuthPage,
  },
  {
    path: "/seats",
    component: SeatPage,
  },
  {
    path: "/survey",
    component: SurveyPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const MyPreset = definePreset(Aura, {
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
  .component("Button", Button)
  .component("InputText", InputText)
  .component("InputGroup", InputGroup)
  .component("Listbox", Listbox)
  .component("Rating", Rating)
  .component("ProgressSpinner", ProgressSpinner)
  .component("ScrollPanel", ScrollPanel)
  .use(autoAnimatePlugin)
  .mount("#app");
