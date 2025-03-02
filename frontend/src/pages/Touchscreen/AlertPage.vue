<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { alertStore } from "../../store/alertStore";
import Countdown from "../../lib/Countdown";
import { commonStore } from "../../store/commonStore";

// Define props to handle error
defineProps(["error"]);

// Initialize router and countdown
const router = useRouter();
const countdown = new Countdown(3, () => {
  commonStore.clear();
  router.push("/home");
});
const fake_countdown = ref(3);

// Helper function to log messages with a timestamp and origin
const logWithTimestamp = (level, message) => {
  const timestamp = new Date().toISOString();
  console[level](`[AlertPage.vue] [${timestamp}] ${message}`);
};

onMounted(() => {
  try {
    logWithTimestamp('log', 'AlertPage.vue mounted, starting fake countdown...');
    const interval = setInterval(() => {
      if (fake_countdown.value > 0) {
        fake_countdown.value--;
        logWithTimestamp('log', `Fake countdown: ${fake_countdown.value} seconds remaining.`);
      } else {
        clearInterval(interval);
        logWithTimestamp('log', 'Fake countdown completed.');
      }
    }, 1000);
  } catch (error) {
    logWithTimestamp('error', `Error during fake countdown in onMounted: ${error}`);
  }
});

// Start countdown when the component is mounted
onMounted(() => {
  try {
    logWithTimestamp('log', 'Starting real countdown...');
    countdown.start();
  } catch (error) {
    logWithTimestamp('error', `Error starting countdown in onMounted: ${error}`);
  }
});

// Stop countdown when the component is unmounted
onUnmounted(() => {
  try {
    logWithTimestamp('log', 'AlertPage.vue unmounted, stopping countdown...');
    countdown.stop();
  } catch (error) {
    logWithTimestamp('error', `Error stopping countdown in onUnmounted: ${error}`);
  }
});
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full h-full gap-4">
    <h2 class="text-5xl font-bold">{{ alertStore.message }}</h2>
    <h2 class="text-3xl font-bold">
      {{ fake_countdown }}秒後回主畫面
    </h2>
  </div>
</template>
