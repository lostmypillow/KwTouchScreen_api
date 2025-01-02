<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { alertStore } from "../store/alertStore";
import { userStore } from "../store/userStore";
import { surveyStore } from "../store/surveyStore";
import Countdown from "../lib/countdown";
defineProps(["error"]);

const router = useRouter();

const currentCountdown = ref();

const countdown = new Countdown(
  4,
  () => {
    console.log("Countdown expired, navigating to home...");
    userStore.clear();
    router.push("/");
  },
  (currentValue) => (currentCountdown.value = currentValue)
);

onMounted(() => {
  userStore.clear();
  surveyStore.clear();
  countdown.start();
  const route = useRoute();
  watch(route, () => countdown.reset());
});

onUnmounted(() => countdown.reset());
</script>
<template>
  <div class="flex flex-col items-center justify-center w-full h-full gap-4">
    <h2 class="text-xl font-bold">{{ alertStore.message }}</h2>
    <h2 class="text-xl font-bold" v-if="currentCountdown != null">
      {{ currentCountdown }}秒後回主畫面
    </h2>
  </div>
</template>
