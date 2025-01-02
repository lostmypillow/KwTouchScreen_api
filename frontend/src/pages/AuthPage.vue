<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import { userStore } from "../store/userStore";
import { useRoute } from "vue-router";
import { surveyStore } from "../store/surveyStore";
import { statusStore } from "../store/statusStore";
import { postAuth } from "../lib/postAuth";
import Countdown from "../lib/countdown";
import { alertStore } from "../store/alertStore";
const route = useRoute();
const router = useRouter();
const callbackRoute = route.params.callback;
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  console.log("Countdown expired, navigating to home...");
  userStore.clear()
  router.push("/");
});

async function handleIDInput() {
  isLoading.value = true;
  const authResult = await postAuth(callbackRoute);
  if (authResult.status != 200) {
    userStore.clear();
    alertStore.setMessage(
      authResult.data.detail ? authResult.data.detail : "發生錯誤"
    );
    router.push("/alert");
  } else {
    userStore.importData(authResult.data);
    if (callbackRoute == "survey") {
      surveyStore.setEmployees(userStore.rateable_employees);
    }
    router.push("/" + callbackRoute);
  }

  isLoading.value = false;
}

const handleButtonClick = (number) => {
  userStore.student_id += number;
  countdown.reset();
};
onMounted(() => {
  nextTick(() => document.querySelector(".p-inputtext").focus());
  if (statusStore.today_class.main_number == null) {
    const router = useRouter();
    alertStore.setMessage("目前沒有您可選的補位資料");
    router.push("/alert");
  }
  countdown.start();
  const route = useRoute();
  watch(route, () => {
    countdown.reset();
  });

  const keydownHandler = async (e) => {
    countdown.reset();
    if (e.key === "Enter") {
      console.log(e.key);
      e.stopPropagation();
      e.preventDefault();
      window.removeEventListener("keydown", keydownHandler);
      countdown.stop();
      await handleIDInput();
    }
  };
  window.addEventListener("keydown", keydownHandler);
});
onUnmounted(() => countdown.stop());
</script>
<template>
  <div
    class="flex flex-col w-full h-full items-start justify-center "
  >
    <div
      v-for="row in [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
      ]"
      class="flex items-center justify-between w-full h-full gap-2"
    >
      <Button
        size="small"
        variant="outlined"
        rounded
        v-for="number in row"
        class="w-full h-fit"
        @click="handleButtonClick(number)"
      >
        <span class="noto-mono font-bold text-2xl">{{ number }}</span></Button
      >
    </div>
    <div class="flex flex-row items-center justify-between w-full h-full gap-2">
      <Button
          severity="danger"
          rounded
           size="small"
          icon="pi pi-delete-left"
          label="刪除"
          class="w-full h-full"
          @click="userStore.student_id = userStore.student_id.slice(0, -1)"
        />
      <Button
        size="small"
        rounded
        variant="outlined"
        class="w-full h-fit"
        @click="handleButtonClick('0')"
      >
        <span class="noto-mono font-bold text-2xl">0</span>
      </Button>
      <Button
        :disabled="userStore.student_id == '' || userStore.student_id.length < 6"
        rounded
        size="small"
        class="w-full h-full"
        severity="success"
        label="下一步"
        :loading="isLoading"
        @click="handleIDInput"
        @keydown.enter="handleIDInput"
        icon="pi pi-arrow-right"
      >
      </Button>
    </div>
  </div>
</template>
