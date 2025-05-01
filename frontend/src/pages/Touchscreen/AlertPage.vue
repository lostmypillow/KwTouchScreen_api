<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { dialogStore } from "../../store_old/dialogStore";
import Countdown from "../../lib/Countdown";
import { commonStore } from "../../store_old/commonStore";
import websocketService from "../../lib/websocketService";
// Define props to handle error
defineProps(["error"]);
const router = useRouter();
const countdown = new Countdown(3, () => {
  commonStore.clear();
  router.push("/home");
});
const fake_countdown = ref(3);

onMounted(() => {
  try {
    const interval = setInterval(() => {
      if (fake_countdown.value > 0) {
        fake_countdown.value--;
      } else {
        clearInterval(interval);
      }
    }, 1000);
  } catch (error) {
    websocketService.sendMessage(
      "client_error",
      `Error during fake countdown in onMounted: ${error}`
    );
  }
});

onMounted(() => {
  try {
    countdown.start();
  } catch (error) {
    websocketService.sendMessage(
      "client_error",
      `Error starting countdown in onMounted: ${JSON.stringify(error)}`
    );
  }
});

// Stop countdown when the component is unmounted
onUnmounted(() => {
  try {
    countdown.stop();
  } catch (error) {
    websocketService.sendMessage(
      "client_error",
      `Error stopping countdown in onUnmounted: ${JSON.stringify(error)}`
    );
  }
});
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full h-full gap-4">
    <h2 class="text-5xl font-bold">{{ dialogStore.message }}</h2>
    <h2 class="text-3xl font-bold">{{ fake_countdown }}秒後回主畫面</h2>
  </div>
</template>
