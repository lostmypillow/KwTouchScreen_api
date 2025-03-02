<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import { userStore } from "../../store/userStore";
import { useRoute } from "vue-router";
import Countdown from "../../lib/Countdown";
import { alertStore } from "../../store/alertStore";
import DeleteButton from "../../components/buttons/DeleteButton.vue";
import NumButton from "../../components/buttons/NumButton.vue";
import Button from "primevue/button";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
import { InputText, InputGroup } from "primevue";
const route = useRoute();
const router = useRouter();
const callbackRoute = route.params.callback;
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  commonStore.clear();
  router.push("/app/home");
});

const handleIDInput = async () => {
  isLoading.value = true;

  try {
    const authResult = await sendToAPI("/auth/", {
      student_id: userStore.student_id,
      type: callbackRoute,
    });
    console.log(authResult)

    if (authResult.code != 200) {
      userStore.clear();
      alertStore.setMessage(authResult.data.detail || "發生錯誤");
      router.push("/app/alert");
      return;
    }

    commonStore.user_data = authResult.data;
    console.log(commonStore.user_data)

    router.push(`/app/${callbackRoute}`);
  } catch (error) {
    alertStore.setMessage("系統錯誤，請稍後再試");
    router.push("/app/alert");
  } finally {
    isLoading.value = false;
  }
};

const handleButtonClick = (number) => {
  userStore.student_id += number;
  countdown.reset();
};
onMounted(() => {
  console.log(`callback: ${callbackRoute}`);
  nextTick(() => document.querySelector(".p-inputtext").focus());
  if (commonStore.today_class_4_auth == "" && callbackRoute == "seats") {
    const router = useRouter();
    console.log("condition met")
    alertStore.setMessage("目前沒有您可選的補位資料");
    router.push("/app/alert");
  }
  countdown.start();

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
  <div class="flex w-full items-center justify-center">
    <div class="grid  max-h-full px-4 gap-2 w-1/2">
      <InputGroup>
        <InputText
          v-model="userStore.student_id"
          inputId="integeronly"
          placeholder="輸入學號"
          fluid
          inputmode="none"
          ref="inputRef"
          variant="outlined"
        />
      </InputGroup>

      <div class="grid grid-cols-3 gap-2">
        <NumButton
          v-for="number in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
          :key="number"
          :number="number"
          @click="handleButtonClick(number)"
        />

        <DeleteButton
          @click="userStore.student_id = userStore.student_id.slice(0, -1)"
        />

        <NumButton number="0" @click="handleButtonClick('0')" />

        <Button
          :disabled="
            userStore.student_id == '' || userStore.student_id.length < 6
          "
          size="small"
          severity="success"
          label="下一步"
          :loading="isLoading"
          @click="handleIDInput"
          @keydown.enter="handleIDInput"
          icon="pi pi-arrow-right"
        />
      </div>
    </div>
  </div>
</template>
