import MainLayout from "./layouts/MainLayout.vue";
import {
  createWebHistory,
  createRouter,
} from "vue-router";
import HomeView from "./views/HomeView.vue";
import AuthView from "./views/AuthView.vue";
import NotFoundView from "./views/NotFoundView.vue";
import SurveyView from "./views/SurveyView.vue";
import SeatView from "./views/SeatView.vue";
import AwardView from "./views/AwardView.vue";
import DashboardView from "./views/DashboardView.vue";
export default createRouter({
  history: createWebHistory("/touch/"),
  routes: [
    {
      path: "/",
      component: MainLayout,
      children: [
        {
          path: "",
          components: { default: HomeView },
          meta: { useMiniLayout: false },
        },
        {
          path: "auth",
          components: { default: AuthView },
          meta: { useMiniLayout: true },
        },
        {
          path: "survey",
          components: { default: SurveyView },
          meta: { useMiniLayout: true },
        },
        {
          path: "seat",
          components: { default: SeatView },
          meta: { useMiniLayout: true },
        },
        {
          path: "award",
          components: { default: AwardView },
          meta: { useMiniLayout: true },
        },
        {
          path: "dashboard",
          components: {default: DashboardView},
          meta: { useMiniLayout: true },
        },
        {
          path: "/:pathMatch(.*)*",
          name: "NotFound",
          component: NotFoundView,
        },
      ],
    },
  ],
});
