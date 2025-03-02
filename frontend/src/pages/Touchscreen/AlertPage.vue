<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { alertStore } from "../../store/alertStore";
import Countdown from "../../lib/Countdown";
import { commonStore } from "../../store/commonStore";
defineProps(["error"]);

const router = useRouter();

const countdown = new Countdown(3, () => {
  commonStore.clear();
  router.push("/app/home");
});

const fake_countdown = ref(3);

onMounted(() => {
  const interval = setInterval(() => {
    if (fake_countdown.value > 0) {
      fake_countdown.value--;
    } else {
      clearInterval(interval);
    }
  }, 1000);
});
onMounted(()=> countdown.start())
onUnmounted(()=> countdown.stop())

</script>
<template>
  <div class="flex flex-col items-center justify-center w-full h-full gap-4">
    <h2 class="text-xl font-bold">{{ alertStore.message }}</h2>
    <h2 class="text-xl font-bold" >
      {{ fake_countdown }}秒後回主畫面
    </h2>
  </div>
</template>
