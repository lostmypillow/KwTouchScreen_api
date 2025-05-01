<script setup>
import { useRouter } from "vue-router";
import { onMounted, nextTick } from "vue";
import DeleteButton from "../components/buttons/DeleteButton.vue";
import NumButton from "../components/buttons/NumButton.vue";
import { commonStore } from "../store_old/commonStore";
import { sendToAPI } from "../lib/sendToAPI";
import BackButton from "../components/buttons/HomeButton.vue";
import { getApplicableAwards } from "../lib/getApplicableAwards";
import { store } from "../store";
import { useLogger } from "../composables/useLogger";
import { useCountdown } from "../composables/useCountdown";
const logger = useLogger();
const router = useRouter();
const { start, reset, stop } = useCountdown(30, () => {
  store.clearUserData();
  router.push("/");
});
const showTemporaryError = (message) => {
  store.setupDialog("error", message);

  setTimeout(() => {
    store.closeDialog();
    reset();
    start();
    focusInput();
    store.authStudentId = "";
  }, 3000);
};
const handleIDInput = async () => {
  let defaultErrorMsg = "驗證失敗";
  if (store.authStudentId == "") {
    return;
  }
  logger.info(`[AuthView.vue] Handling ID input for ${store.authStudentId}`);

  logger.info("[AuthView.vue] Setting loading message");
  store.setupDialog("loading", "驗證中，請稍候...");

  logger.info("[AuthView.vue] Showing dialog");
  store.showDialog();

  try {
    logger.info("[AuthView.vue] Calling sendToAPI");
    const authResult = await sendToAPI("/auth/", {
      student_id: store.authStudentId,
      type: store.authType,
    });

    logger.info(
      `[AuthView.vue] Received authResult: ${JSON.stringify(authResult)}`
    );

    if (authResult.code != 200) {
      logger.error(
        `[AuthView.vue] ${
          store.authStudentId
        } authResult.code is not 200: ${JSON.stringify(authResult)}`
      );

      logger.info("[AuthView.vue] Setting error message");
      showTemporaryError(
        typeof authResult?.data?.detail === "string"
          ? authResult.data.detail
          : defaultErrorMsg
      );
      return;
    }

    logger.info("[AuthView.vue] Auth succeeded, saving user_data");
    console.log("look here");
    console.log(authResult.data);
    store.userData = authResult.data;

    if (store.authType == "awards") {
      logger.info(
        "[AuthView.vue] authType is 'awards', loading awards info, showing awards loading dialog message"
      );
      store.setupDialog("loading", "載入獎學金資訊中，請稍候...");

      try {
        logger.info("[AuthView.vue] Calling getApplicableAwards");
        commonStore.courses = await getApplicableAwards(
          commonStore.user_data.學號
        );
        logger.info("[AuthView.vue] Got courses:", commonStore.courses);
      } catch (err) {
        logger.error(
          `[AuthView.vue] ${
            store.authStudentId
          }  getApplicableAwards error: ${JSON.stringify(err)}`
        );

        logger.info("[AuthView.vue] Setting error message and closing in 3s");
        showTemporaryError("載入獎學金資訊時發生錯誤");
        return;
      }

      if (
        !commonStore.courses ||
        commonStore.courses.length === 0 ||
        commonStore.courses === "error"
      ) {
        logger.error(
          `[AuthView.vue] ${store.authStudentId}  No applicable awards found or invalid response for: ${commonStore.user_data.學號}. Showing no applicable awards dialog message`
        );

        showTemporaryError("目前沒有您可申請的獎學金");
        return;
      }
    } else if (store.authType && store.surveyIs4Math == true) {
      if (
        store.userData.rateable_employees.filter(
          (x) => x.主要部門 === "數輔"
        ) === 0
      ) {
        showTemporaryError("目前沒有您可評分的數輔老師!");
      }
    }

    logger.info("[AuthView.vue] All checks passed, showing success");
    store.setupDialog("success", `驗證成功!`);
    setTimeout(() => {
      logger.info("[AuthView.vue] Closing dialog and navigating");
      store.closeDialog();
      router.push(`/${store.authType}`);
    }, 1000);
  } catch (error) {
    logger.error(
      `[AuthView.vue] ${store.authStudentId}  Error during authentication: ${error}`
    );
    showTemporaryError(defaultErrorMsg);
    return;
  }
};

const listenForEnterKey = () => {
  const keydownHandler = async (e) => {
    try {
      reset();
      if (e.key === "Enter") {
        e.stopPropagation();
        e.preventDefault();
        window.removeEventListener("keydown", keydownHandler);
        stop();
        await handleIDInput();
        return;
      }
    } catch (err) {
      logger.error(`[AuthView.vue] keydownHandler error: ${err}`);
      return;
    }
  };

  window.addEventListener("keydown", keydownHandler);
};
// Handle button click for entering student ID
const handleButtonClick = (number) => {
  store.authStudentId += number;
  reset();
  start();
};
const focusInput = () => {
  const inputElement = document.querySelector(".p-inputtext");
  if (inputElement) {
    inputElement.focus();
  }
};
const backspace = () => {
  store.authBackspace();
  reset();
  start();
};
// Component mounted logic
onMounted(() => {
  start();
  try {
    nextTick(() => focusInput());
    listenForEnterKey();
  } catch (err) {
    logger.error(`[AuthView.vue] onMounted error: ${err}`);
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
          v-model="store.authStudentId"
          inputId="integeronly"
          placeholder="輸入學號"
          fluid
          inputmode="none"
          ref="inputRef"
          variant="outlined"
        />
        <DeleteButton class="text-center" @click="backspace" />
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
            store.authStudentId == '' || store.authStudentId.length < 6
          "
          severity="success"
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

::v-deep(.p-dialog-header-actions) {
  display: none !important;
}
</style>
