<script setup>
import { ref, onMounted, onUnmounted, Transition, watch } from "vue";
import websocketService from "../lib/websocketService";
import { commonStore } from "../store_old/commonStore";
import { useRouter, useRoute } from "vue-router";
import { store } from "../store";
const router = useRouter();
const route = useRoute();

/// Time
const currentTime = ref(new Date());
const formatTime = (date) => {
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
};

const formatDate = (date) => {
  const formattedDate = date.toLocaleDateString("zh-TW", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formattedDate;
};

const timeInterval = setInterval(() => {
  currentTime.value = new Date();
}, 1000);

///
const currentIndex = ref(0);
let classInterval;

const startAlternatingClass = () => {
  if (store.classesToday.length > 0) {
    classInterval = setInterval(() => {
      currentIndex.value = (currentIndex.value + 1) % store.classesToday.length;
      
    }, 5000);
  }
};

const stopAlternatingClass = () => {
  clearInterval(classInterval);
  console.log(
    `[Status.vue] [${new Date().toISOString()}] stopAlternatingClass: interval cleared`
  );
};

onUnmounted(() => {
  stopAlternatingClass();
  clearInterval(timeInterval);
  console.log(
    `[Status.vue] [${new Date().toISOString()}] onUnmounted: timeInterval and classInterval cleared`
  );
});

watch(
  () => store.classesToday.length,
  (newLength) => {
    console.log(
      `[Status.vue] [${new Date().toISOString()}] watch: classesToday length changed to ${newLength}`
    );
    if (newLength > 0) {
      startAlternatingClass();
    } else {
      stopAlternatingClass();
    }
  }
);


</script>

<template>
  <div class="flex flex-col w-full gap-4">
    <!-- time start -->
    <div
      class="grow-0 h-fit w-full flex items-center justify-center min-h[6.25%] py-2 gap-4"
    >
      {{ formatDate(currentTime) }}
      <span class="noto-mono">{{ formatTime(currentTime) }}</span>
    </div>
    <!-- time end -->

    <div class="flex flex-col w-full px-4 items-center justify-between h-full">
      <Transition mode="out-in">
        <div
          class="flex flex-row items-center justify-between w-full text-5xl font-bold"
          :key="currentIndex"
        >
          <div class="flex flex-col items-start justify-start pt-4">
            <h3>
              {{
                store.classesToday[currentIndex]
                  ? store.classesToday[currentIndex]?.內容
                  : "\u00A0"
              }}
            </h3>
            <h3>
              {{
                store.classesToday[currentIndex]
                  ? store.classesToday[currentIndex]?.教室
                  : "\u00A0"
              }}
            </h3>
          </div>

          <div class="flex text-8xl font-bold">
            {{
              store.classesToday[currentIndex]
                ? store.classesToday[currentIndex].時間
                : "\u00A0"
            }}
          </div>
        </div>
      </Transition>
    </div>
    <div
      class="justify-center text-red-500 flex flex-row w-full items-center  gap-4 px-4 
      "
    >
      <p
        class="text-2xl font-bold"
        v-if="Object.keys(store.classWithSeats).length > 0"
      >
        {{
          store.classWithSeats
            ? store.classWithSeats?.班級名稱 +
              "補位剩餘 男:" +
              store.classWithSeats.男座位?.length +
              ", 女:" +
              store.classWithSeats.女座位?.length
            : "\u00A0"
        }}
      </p>
      <span
        v-if="route.fullPath != '/' "
      ></span>
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
