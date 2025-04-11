import "./style.css";
import "primeicons/primeicons.css";
import { createApp } from "vue";
import {
  createWebHistory,
  createRouter,
  createWebHashHistory,
} from "vue-router";
import { definePreset } from "@primevue/themes";
import PrimeVue from "primevue/config";
import Material from "@primevue/themes/material";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Listbox from "primevue/listbox";
import InputGroup from "primevue/inputgroup";
import Rating from "primevue/rating";
import ScrollPanel from "primevue/scrollpanel";
import ProgressSpinner from "primevue/progressspinner";
import HomePage from "./pages/Touchscreen/HomePage.vue";
import AuthPage from "./pages/Touchscreen/AuthPage.vue";
import SeatPage from "./pages/Touchscreen/SeatPage.vue";
import AlertPage from "./pages/Touchscreen/AlertPage.vue";
import SurveyPage from "./pages/Touchscreen/SurveyPage.vue";
import { autoAnimatePlugin } from "@formkit/auto-animate/vue";
import App from "./App.vue";
import ToastService from 'primevue/toastservice';
import DashboardPage from "./pages/DashboardPage.vue";
import RootLayout from "./pages/Touchscreen/RootLayout.vue";
const routes = [
  {
    path: "/",
    redirect: 'home',
    component: RootLayout,
    children: [
      {
        path: "home",
        component: HomePage,
      },
      {
        path: "alert",
        component: AlertPage,
      },
      {
        path: "auth/:callback",
        component: AuthPage,
      },
      {
        path: "seats",
        component: SeatPage,
      },
      {
        path: "survey",
        component: SurveyPage,
      },
      {
        path: "/dashboard",
        component: DashboardPage,
      },
    ],
  },

  
];

const router = createRouter({
  history: createWebHistory('/touch/'),
  routes,
});

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
  .use(ToastService)

  .mount("#app");
