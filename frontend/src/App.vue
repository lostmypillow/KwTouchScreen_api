<script setup>
import { RouterView, useRoute, useRouter } from "vue-router";
import {
  onMounted,
  onBeforeUpdate,
  ref,
  onUpdated,
  watch,
  useTemplateRef,
  nextTick,
} from "vue";
import TimeAndDate from "./components/TimeAndDate.vue";
import VideoPlayer from "./components/VideoPlayer.vue";
import Status from "./components/Status.vue";
import { userStore } from "./store/userStore";
import { surveyStore } from "./store/surveyStore";
import { listenToLongPolling } from "./lib/listenToLongPolling";
const router = useRouter();
const route = useRoute();

listenToLongPolling();
onMounted(() => {
  // watch(
  //   () => route.fullPath,
  //   () => {
  //     if (route.fullPath.startsWith("/auth")) {
        
  //     }
  //   },
  //   { immediate: true }
  // );
});
</script>

<template>
  <div class="flex flex-col items-center justify-between gap-4 h-svh w-svw">
    <TimeAndDate />
    <Status />
    <div
      class="flex flex-col w-full h-full items-start justify-start gap-2 px-4"
    >
      <InputGroup
        v-if="route.fullPath !== '/'"
        class="flex flex-row h-14 w-full gap-2 items-center"
      >

        <InputText
          v-if="route.fullPath.startsWith('/auth')"
          v-model="userStore.student_id"
          inputId="integeronly"
          placeholder="輸入學號"
          class="shrink w-1/3 text-3xl"
          fluid
          inputmode="none"
          ref="inputRef"
          variant="outlined"
        />

        <div v-else class="flex items-center justify-center font-bold w-full">
          {{ userStore.student_id }} {{ userStore.name }}
          {{
            route.fullPath.startsWith("/seats")
              ? "今日補位"
              : route.fullPath.startsWith("/survey") &&
                surveyStore.selectedDepartment.number == 9
              ? "數輔老師教學品質"
              : route.fullPath.startsWith("/survey")
              ? "滿意度調查"
              : "系統訊息"
          }}
        </div>
        
      </InputGroup>
      <!-- </Transition> -->

      <router-view />
    </div>
    <VideoPlayer />
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
.p-inputtext {
  font-size: larger;
}
</style>
