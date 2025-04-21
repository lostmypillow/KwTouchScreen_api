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
import { getApplicableAwards } from "../../lib/getApplicableAwards";
import websocketService from "../../lib/websocketService";
// Define props and router
const route = useRoute();
const router = useRouter();
const callbackRoute = route.params.callback;
const studentID = ref("");
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  commonStore.clear();
  router.push("/home");
});

const handleIDInput = async () => {
  websocketService.sendMessage(
    "client_action",
    `AuthPage.vue Handling ID input for ${studentID.value}`
  );
  isLoading.value = true;
  let defaultError = "發生錯誤";

  try {
    const authType = callbackRoute;
    const authResult = await sendToAPI("/auth/", {
      student_id: studentID.value,
      type: authType,
    });
    if (studentID.value.length > 6) {
      defaultError += "\n: 學號打太長了嗎?";
    }

    if (authResult.code != 200) {
      websocketService.sendMessage(
        "client_error",
        `AuthPage.vue ${studentID.value} Authentication failed: ${
          JSON.stringify(authResult.data.detail) || "發生錯誤"
        }`
      );

      alertStore.setMessage(
        typeof authResult?.data?.detail === "string"
          ? authResult.data.detail
          : defaultError
      );

      router.push("/alert");
      return;
    }

    commonStore.user_data = authResult.data;

    if (callbackRoute == "awards") {
      try {
        commonStore.courses = await getApplicableAwards(
          commonStore.user_data.學號
        );
      } catch (err) {
        websocketService.sendMessage(
          "client_error",
          `AuthPage.vue ${studentID.value}  getApplicableAwards error: ${JSON.stringify(err)}`
        );
        alertStore.setMessage("獲取獎學金資料時發生錯誤");
        router.push("/alert");
        return;
      }

      if (
        !commonStore.courses ||
        commonStore.courses.length === 0 ||
        commonStore.courses === "error"
      ) {
        websocketService.sendMessage(
          "client_error",
          `AuthPage.vue ${studentID.value}  No applicable awards found or invalid response for: ${commonStore.user_data.學號}`
        );
        alertStore.setMessage("目前沒有您可申請的獎學金");
        router.push("/alert");
        return;
      }
    }

    router.push(`/${callbackRoute}`);
  } catch (error) {
    if (studentID.value.length > 6) {
      defaultError += "\n提示: 學號打太長了嗎?";
    }
    websocketService.sendMessage(
      "client_error",
      `AuthPage.vue ${studentID.value}  Error during authentication: ${error}`
    );
    alertStore.setMessage(defaultError);
    router.push("/alert");
    return;
  } finally {
    isLoading.value = false;
  }
};

// Handle button click for entering student ID
const handleButtonClick = (number) => {
  studentID.value += number;
  countdown.reset();
};

// Component mounted logic
onMounted(() => {
  try {
    nextTick(() => {
      const inputElement = document.querySelector(".p-inputtext");
      if (inputElement) {
        inputElement.focus();
      }
    });

    if (commonStore.today_class_4_auth == "" && callbackRoute == "seats") {
      alertStore.setMessage("目前沒有您可選的補位資料");
      router.push("/alert");
    }

    countdown.start();

    const keydownHandler = async (e) => {
      try {
        countdown.reset();
        if (e.key === "Enter") {
          e.stopPropagation();
          e.preventDefault();
          window.removeEventListener("keydown", keydownHandler);
          countdown.stop();
          await handleIDInput();
        }
      } catch (err) {
        websocketService.sendMessage(
          "client_error",
          `AuthPage.vue keydownHandler error: ${err}`
        );
      }
    };

    window.addEventListener("keydown", keydownHandler);
  } catch (err) {
    websocketService.sendMessage(
      "client_error",
      `AuthPage.vue onMounted error: ${err}`
    );
  }
});

// Component unmounted logic
onUnmounted(() => {
  try {
    countdown.stop();
  } catch (err) {
    websocketService.sendMessage("client_error", `AuthPage.vue onUnmounted error: ${JSON.stringify(err)}`);
  }
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

    <div class="flex flex-col px-4 gap-2 w-full">
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
        />
        <DeleteButton
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
          :disabled="studentID == '' || studentID.length < 6 || isLoading"
          severity="success"
          :loading="isLoading"
          @click="handleIDInput"
          @keydown.enter="handleIDInput"
          icon="pi pi-arrow-right"
          class="flex-1 min-w-[30%] max-w-[32%] text-center"
        >
          <span class="text-2xl font-extra-bold"> 登入 </span>
        </Button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.p-inputtext {
  font-size: 2rem;
}
</style>
