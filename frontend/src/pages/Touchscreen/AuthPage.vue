<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import { useRoute } from "vue-router";
import Countdown from "../../lib/Countdown";
import { alertStore } from "../../store/alertStore";
import DeleteButton from "../../components/buttons/DeleteButton.vue";
import NumButton from "../../components/buttons/NumButton.vue";
import Button from "primevue/button";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
import { InputText, InputGroup } from "primevue";
import BackButton from "../../components/buttons/BackButton.vue";
// Define props and router
const route = useRoute();
const router = useRouter();
const callbackRoute = route.params.callback;
const studentID = ref('')
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  commonStore.clear();
  router.push("/home");
});

// Helper function to log messages with a timestamp and origin
const logWithTimestamp = (level, message) => {
  const timestamp = new Date().toISOString();
  console[level](`[AuthPage.vue] [${timestamp}] ${message}`);
};

// Handle student ID input and authentication
const handleIDInput = async () => {
  logWithTimestamp("log", "Handling ID input...");
  isLoading.value = true;

  try {
    const authResult = await sendToAPI("/auth/", {
      student_id: studentID.value,
      type: callbackRoute,
    });
    logWithTimestamp(
      "log",
      `Authentication result: ${JSON.stringify(authResult)}`
    );

    if (authResult.code != 200) {
      logWithTimestamp(
        "warn",
        `Authentication failed: ${authResult.data.detail || "發生錯誤"}`
      );
   
      alertStore.setMessage(authResult.data.detail || "發生錯誤");
      router.push("/alert");
      return;
    }

    commonStore.user_data = authResult.data;
    logWithTimestamp(
      "log",
      `User data: ${JSON.stringify(commonStore.user_data)}`
    );

    router.push(`/${callbackRoute}`);
  } catch (error) {
    logWithTimestamp("error", `Error during authentication: ${error}`);
    alertStore.setMessage("系統錯誤，請稍後再試");
    router.push("/alert");
  } finally {
    isLoading.value = false;
  }
};

// Handle button click for entering student ID
const handleButtonClick = (number) => {
  logWithTimestamp("log", `Button clicked: ${number}`);
  studentID.value += number;
  countdown.reset();
};

// Component mounted logic
onMounted(() => {
  logWithTimestamp(
    "log",
    `Component mounted, callback route: ${callbackRoute}`
  );

  nextTick(() => {
    const inputElement = document.querySelector(".p-inputtext");
    if (inputElement) {
      inputElement.focus();
      logWithTimestamp("log", "Input focused.");
    }
  });

  if (commonStore.today_class_4_auth == "" && callbackRoute == "seats") {
    logWithTimestamp("log", "Condition met for redirecting to alert.");
    alertStore.setMessage("目前沒有您可選的補位資料");
    router.push("/alert");
  }

  countdown.start();

  const keydownHandler = async (e) => {
    countdown.reset();
    if (e.key === "Enter") {
      logWithTimestamp("log", `Enter key pressed: ${e.key}`);
      e.stopPropagation();
      e.preventDefault();
      window.removeEventListener("keydown", keydownHandler);
      countdown.stop();
      await handleIDInput();
    }
  };

  window.addEventListener("keydown", keydownHandler);
});

// Component unmounted logic
onUnmounted(() => {
  logWithTimestamp("log", "Component unmounted, stopping countdown...");
  countdown.stop();
});
</script>

<template>
  <div class="flex flex-col items-center justify-start gap-2 w-full h-full p-4">
    <div class="flex flex-row w-full items-center justify-between">
      <div class="flex flex-row gap-2 items-center">
        <BackButton />
        <h1 class="text-4xl font-extrabold text-center">登入</h1>
      </div>
    </div>

    <div class="flex flex-col px-4 gap-2 w-full ">
      <InputGroup class="py-4">
        <InputText
          :pt="{ root: { class: 'text-2xl' } }"
          v-model="studentID"
          inputId="integeronly"
          placeholder="輸入學號"
          fluid
          inputmode="none"
          ref="inputRef"
          variant="outlined"
        /><DeleteButton
          class="text-center"
          @click="studentID = studentID.slice(0, -1)"
        />
      </InputGroup>

      <!-- Numpad container using flexbox -->
      <div class="flex flex-wrap gap-2 justify-between w-full">
        <NumButton
          v-for="number in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
          :key="number"
          :number="number"
          class="flex-1 min-w-[30%] max-w-[32%] text-center"
          @click="handleButtonClick(number)"
        />

        <NumButton
          number="0"
          class="flex-1 w-full text-center"
          @click="handleButtonClick('0')"
        />

        <Button
          :disabled="
            studentID == '' || studentID.length < 6
          "
          severity="success"
          :loading="isLoading"
          @click="handleIDInput"
          @keydown.enter="handleIDInput"
          icon="pi pi-arrow-right"
          class="flex-1 min-w-[30%] max-w-[32%] text-center"
        >
          <span class="text-2xl font-extra-bold">登入</span></Button
        >
      </div>
    </div>
  </div>

  <!-- <div class="flex flex-col items-start justify-start gap-2">
    <div class="grid h-full px-4 gap-2 w-full">
      <InputGroup>
        <InputText
          v-model="studentID"
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
          @click="studentID = studentID.slice(0, -1)"
        />

        <NumButton number="0" @click="handleButtonClick('0')" />

        <Button
          :disabled="
            studentID == '' || studentID.length < 6
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
  </div> -->
</template>
<style scoped>
.p-inputtext {
  font-size: 2rem;
}
</style>
