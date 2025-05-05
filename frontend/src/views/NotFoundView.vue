<script setup>
import { onMounted } from "vue";
import { useCountdown } from "../composables/useCountdown";
import { useRouter } from "vue-router";
import { store } from "../store";
const router = useRouter();
const { timeLeft, start } = useCountdown(3, () => {
  store.clearUserData();
  router.push("/");
});
onMounted(() => start());
</script>
<template>
  <div class="flex flex-col gap-4 w-full h-full items-center justify-center">
    <h1 class="text-4xl font-extrabold">您所尋找的頁面不存在</h1>
    <h2 class="text-2xl font-bold">系統將在 {{ timeLeft }} 秒後自動返回首頁</h2>
  </div>
</template>
