<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const currentTime = ref(new Date());

onMounted(() => {
  const intervalId = setInterval(() => {
    currentTime.value = new Date();
  }, 1000);

  onUnmounted(() => {
    clearInterval(intervalId);
  });
});

const formatTime = (date) => {
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
};

const formatDate = (date) => {
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return date.toLocaleDateString("zh-TW", options);
};
</script>
<template>
  <div class="grow-0 h-fit w-full flex items-center justify-center pt-4 gap-4 min-h[6.25%]">
    {{ formatDate(currentTime) }} 
    <span class="noto-mono">{{ formatTime(currentTime) }}</span>
  </div>
</template>
