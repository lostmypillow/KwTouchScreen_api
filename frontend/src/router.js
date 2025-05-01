import MainLayout from "./layouts/MainLayout.vue";
import {
    createWebHistory,
    createRouter,
    createWebHashHistory,
  } from "vue-router";
import HomeView from "./views/HomeView.vue";
import AuthView from "./views/AuthView.vue";
import NotFoundView from "./views/NotFoundView.vue";
import SurveyView from "./views/SurveyView.vue";
export default createRouter({
    history: createWebHistory('/touch/'),
    routes: [
        {
          path: "/",
          component: MainLayout,
          children: [
            {
                path: '',
                components: {default: HomeView }
            },
            {
                path: 'auth',
                components: {default: AuthView}
            },
            {
                path: 'survey',
                components: {default: SurveyView}
            },
            {
                path: '/:pathMatch(.*)*',
                name: 'NotFound',
                component: NotFoundView
              }
          ]
        //   children: [
        //     {
        //       path: "home",
        //       component: HomePage,
        //     },
        //     {
        //       path: "alert",
        //       component: AlertPage,
        //     },
        //     {
        //       path: "auth/:callback",
        //       component: AuthPage,
        //     },
        //     {
        //       path: "seats",
        //       component: SeatPage,
        //     },
        //     {
        //       path: "survey",
        //       component: SurveyPage,
        //     },
        //     {
        //       path: "dashboard",
        //       component: DashboardPage,
        //     },
        //     {
        //       path: "awards",
        //       component: AwardPage
        //     }
        //   ],
        },
      
        
      ]
  });