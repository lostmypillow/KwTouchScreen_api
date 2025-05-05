<!-- MiniLayout.vue -->
<script setup>
import { useRoute, useRouter } from "vue-router";
import { store } from "../store";
const route = useRoute();
const router = useRouter();
const goHome = () => {
  store.clearUserData();
  router.push("/");
  return;
};
</script>

<template>
  <div class="flex flex-col items-center justify-start gap-2 w-full h-full p-4">
    <div class="flex flex-row w-full items-center justify-between">
      <div class="flex flex-row gap-2 items-center">
        <Button size="large" @click="goHome"
          ><i class="pi pi-home"></i>回主畫面</Button
        >
        <h1 class="text-4xl font-extrabold text-center">
          {{
            route.fullPath == "/auth"
              ? "登入"
              : route.fullPath == "/survey"
              ? "滿意度調查"
              : route.fullPath == "/seat"
              ? "今日補位"
              : route.fullPath == "/dashboard"
              ? "Dashboard"
              : "獎學金申請"
          }}
        </h1>
      </div>
      <h4 class="text-base" v-if="store.userData.姓名 != 'XXX'">
        已登入為 {{ store.userData.學號 }}
        {{ store.userData.姓名 }}
      </h4>
    </div>
    <slot></slot>
  </div>
</template>
