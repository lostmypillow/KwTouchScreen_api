<script setup>
import { useRouter } from "vue-router";
import { onMounted, nextTick, onUnmounted } from "vue";
import DeleteButton from "../components/buttons/DeleteButton.vue";
import NumButton from "../components/buttons/NumButton.vue";
import { store } from "../store";
import { useLogger } from "../composables/useLogger";
import { useCountdown } from "../composables/useCountdown";
import { useAPI } from "../composables/useAPI";
const logger = useLogger();
const router = useRouter();
const api = useAPI();
const { start, reset, stop } = useCountdown(30, () => {
  store.clearUserData();
  router.push("/");
});
const showTemporaryError = (message) => {
  store.setupDialog("error", message);

  setTimeout(() => {
    store.closeDialog();
    store.clearUserData();
    reset();
    focusInput();
    window.addEventListener("keydown", keydownHandler);
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
    const authResult = await api.sendData(
      `http://${import.meta.env.VITE_FASTAPI_URL}/auth/`,
      { "Content-Type": "application/json" },
      {
        student_id: store.authStudentId,
        type: store.authType,
      }
    );

    if (authResult.success == false) {
      logger.error(
        `[AuthView.vue] ${
          store.authStudentId
        } authentication did NOT succeed: ${JSON.stringify(authResult)}`
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
    store.userData = authResult.data;

    if (store.authType == "award") {
      logger.info(
        "[AuthView.vue] authType is 'awards', loading awards info, showing awards loading dialog message"
      );
      store.setupDialog("loading", "載入獎學金資訊中，請稍候...");

      try {
        store.scholarshipDates = (
          await api.getApplicableAwards(store.userData.學號)
        ).data;
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
        !store.scholarshipDates ||
        store.scholarshipDates.length === 0 ||
        store.scholarshipDates === "error"
      ) {
        logger.error(
          `[AuthView.vue] ${store.authStudentId}  No applicable awards found or invalid response for: ${store.userData.學號}. Showing no applicable awards dialog message`
        );

        showTemporaryError("目前沒有您可申請的獎學金");
        return;
      }
    } else if (store.authType == 'survey' && store.surveyIs4Math == true) {
      console.log('look here')
      console.log( store.userData.rateable_employees.filter(
          (x) => x.主要部門 === "數輔"
        ))
      if (
        store.userData.rateable_employees.filter(
          (x) => x.主要部門 === "數輔"
        ).length == 0
      ) {
        console.log("No teachers for survey")
        showTemporaryError("目前沒有您可評分的數輔老師!");
        return;
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

const keydownHandler = async (e) => {
  try {
    stop();
    if (e.key === "Enter") {
      e.stopPropagation();
      e.preventDefault();
      window.removeEventListener("keydown", keydownHandler);

      await handleIDInput();
      return;
    }
  } catch (err) {
    logger.error(`[AuthView.vue] keydownHandler error: ${err}`);
    return;
  }
};

// Handle button click for entering student ID
const handleButtonClick = (number) => {
  store.authStudentId += number;
  reset();
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
};
window.addEventListener("keydown", keydownHandler);
// Component mounted logic
onMounted(() => {
  start();
  try {
    nextTick(() => focusInput());
  } catch (err) {
    logger.error(`[AuthView.vue] onMounted error: ${err}`);
  }
});
onUnmounted(()=>  window.removeEventListener("keydown", keydownHandler))
</script>

<template>
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
        :disabled="store.authStudentId == '' || store.authStudentId.length < 6"
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
</template>
<style scoped>
.p-inputtext {
  font-size: 2rem;
}

::v-deep(.p-dialog-header-actions) {
  display: none !important;
}
</style>
