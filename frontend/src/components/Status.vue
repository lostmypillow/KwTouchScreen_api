<script setup>
import { ref, onMounted, onUnmounted, Transition, watch } from "vue";
import { statusStore } from "../store/statusStore";
import axios from "axios";

const currentIndex = ref(0);
let interval;

const startAlternating = () => {
  if (statusStore.current_list.length > 0) {
    interval = setInterval(() => {
      currentIndex.value = (currentIndex.value + 1) % statusStore.current_list.length;
    }, 5000);
  }
};

const stopAlternating = () => {
  clearInterval(interval);
};

watch(() => statusStore.current_list.length, (newLength) => {
  if (newLength > 0) {
    startAlternating();
  } else {
    stopAlternating();
  }
});

onMounted(() => {
  if (statusStore.current_list.length > 0) {
    startAlternating();
  }
});

onUnmounted(() => {
  stopAlternating();
});
</script>

<template>
  <div class="flex flex-col w-full px-6 items-center justify-between gap-4 min-h-[13%]">
    <Transition mode="out-in">
      <div
        class="flex flex-row items-center justify-between w-full text-xl font-bold min-h-[8.75%]"
        :key="currentIndex"
      >
        <div class="flex flex-col items-start justify-start"  v-if="statusStore.current_list[currentIndex]">
          <h3>{{ statusStore.current_list[currentIndex]?.location }}</h3>
          <h3>{{ statusStore.current_list[currentIndex]?.name }}</h3>
        </div>

        <div class="flex text-4xl font-bold"  v-if="statusStore.current_list[currentIndex]">
          {{ statusStore.current_list[currentIndex].time }}
        </div>
      </div>
    </Transition>

    <div v-if="statusStore.today_class.name != null" class="text-red-500 min-h-[3.75%]">
      {{ statusStore.today_class?.name }} 補位剩餘 男:
      {{ statusStore.today_class.male_seats?.length }}, 女:
      {{ statusStore.today_class.female_seats?.length }}
    </div>
  </div>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
