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
  logger.info(`[AuthView.vue] Showing temporary error dialog: ${message}`);

  setTimeout(() => {
    store.closeDialog();
    logger.info("[AuthView.vue] Dialog closed");
    store.authStudentId = ""
    logger.info("[AuthView.vue] authStudentId cleared");
    reset();
    logger.info("[AuthView.vue] Countdown reset and restarted");
    focusInput();
    logger.info("[AuthView.vue] Input focused");
    window.addEventListener("keydown", keydownHandler);
    logger.info("[AuthView.vue] Keydown handler added");
  }, 3000);
};
const handleIDInput = async () => {
  logger.info(`[AuthView.vue] Login button pressed for ${store.authStudentId}`);
  let defaultErrorMsg = "驗證失敗";
  if (store.authStudentId == "") {
    logger.info(`[AuthView.vue] Input was empty, function returning early`);
    return;
  }
  store.setupDialog("loading", "驗證中，請稍候...");
  store.showDialog();
  logger.info("[AuthView.vue] Showing loading dialog: 驗證中，請稍候...");

  try {
    logger.info(
      `[AuthView.vue] Calling API with URL of http://${
        import.meta.env.VITE_FASTAPI_URL
      }/auth/ with data of ${JSON.stringify({
        student_id: store.authStudentId,
        type: store.authType,
      })}`
    );
    const authResult = await api.sendData(
      `http://${import.meta.env.VITE_FASTAPI_URL}/auth/`,
      { "Content-Type": "application/json" },
      {
        student_id: store.authStudentId,
        type: store.authType,
      }
    );
    logger.info(`API result: ${JSON.stringify(authResult)}`);

    if (authResult.success == false) {
      logger.error(
        `[AuthView.vue] ${store.authStudentId} authResult success value is FALSE`
      );
      showTemporaryError(
        typeof authResult?.data?.detail === "string"
          ? authResult.data.detail
          : defaultErrorMsg
      );
      return;
    }

    if (store.authType == "award") {
      store.setupDialog("loading", "載入獎學金資訊中，請稍候...");
      logger.info(
        "[AuthView.vue] Since authType is 'award', showing loading dialog: 載入獎學金資訊中，請稍候...`)"
      );

      try {
        logger.info("[AuthView.vue] Calling applicable awards API...");
        store.scholarshipDates = (
          await api.getApplicableAwards(authResult.data.學號)
        ).data;
        logger.info(`Awards data saved as ${store.scholarshipDates}`)
      } catch (err) {
        logger.error(
          `[AuthView.vue] ${
            store.authStudentId
          }  api.getApplicableAwards error: ${JSON.stringify(err)}`
        );
        showTemporaryError("載入獎學金資訊時發生錯誤");
        return;
      }

      if (
        !store.scholarshipDates ||
        store.scholarshipDates.length === 0 ||
        store.scholarshipDates === "error"
      ) {
        logger.error(
          `[AuthView.vue] Error while getting applicable awards for: ${
            store.authStudentId
          }. Null? ${!store.scholarshipDates}. Empty/no length? ${
            store.scholarshipDates.length === 0
          }. Equals error? ${store.scholarshipDates === "error"}.`
        );
        showTemporaryError("目前沒有您可申請的獎學金");
        return;
      }
    } else if (store.authType == "survey" && store.surveyIs4Math == true) {
      logger.info(
        `[AuthView.vue] authType is survey and surveyIs4Math is true. No math tutors available? ${
          authResult.data.rateable_employees.filter((x) => x.主要部門 === "數輔")
            .length == 0
        }.`
      );
      if (
        authResult.data.rateable_employees.filter((x) => x.主要部門 === "數輔")
          .length == 0
      ) {
        showTemporaryError("目前沒有您可評分的數輔老師!");
        return;
      }
    }

    logger.info(
      "[AuthView.vue] All checks passed, saving results and showing success dialog: 驗證成功!"
    );
    store.userData = authResult.data;
    store.setupDialog("success", `驗證成功!`);
    setTimeout(() => {
      logger.info(
        `[AuthView.vue] Closing dialog and navigating to /${store.authType}`
      );
      store.closeDialog();
      router.push(`/${store.authType}`);
    }, 1000);
  } catch (error) {
    logger.error(
      `[AuthView.vue]  Error during authentication for ${
        store.authStudentId
      } : ${JSON.stringify(error)}`
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
    logger.error(`[AuthView.vue] keydownHandler error: ${JSON.stringify(err)}`);
    return;
  }
};

// Handle button click for entering student ID
const handleButtonClick = (number) => {
  try {
    store.authStudentId += number;
    reset();
  } catch (error) {
    logger.error(`[AuthView.vue] buttonClick error: ${JSON.stringify(error)}`);
  }
};
const focusInput = () => {
  const inputElement = document.querySelector(".p-inputtext");
  if (inputElement) {
    inputElement.focus();
  }
};
const backspace = () => {
  try {
    store.authBackspace();
    reset();
  } catch (error) {
    logger.error(`[AuthView.vue] backspace error: ${JSON.stringify(error)}`);
  }
};
window.addEventListener("keydown", keydownHandler);
// Component mounted logic
onMounted(() => {
  start();
  try {
    nextTick(() => focusInput());
  } catch (error) {
    logger.error(`[AuthView.vue] onMounted error: ${JSON.stringify(error)}`);
  }
});
onUnmounted(() => {
  try {
    window.removeEventListener("keydown", keydownHandler);
  } catch (error) {
    logger.error(
      `[AuthView.vue] removing keydownHandler error: ${JSON.stringify(error)}`
    );
  }
});
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
