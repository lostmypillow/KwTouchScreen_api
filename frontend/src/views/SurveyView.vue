<script setup>
import { ref, onMounted,  reactive } from "vue";
import { useRouter } from "vue-router";
import { store } from "../store";
import { useCountdown } from "../composables/useCountdown";
import { useLogger } from "../composables/useLogger";
import { useAPI } from "../composables/useAPI";
const logger = useLogger();
const router = useRouter();
const currentDep = ref("");
const currentRating = ref(0);
const imageLoading = reactive({});
const currentEmp = ref();
const api = useAPI();
const { start, reset, stop } = useCountdown(30, () => {
  store.clearUserData();
  router.push("/");
});

const showTemporaryError = (message, error) => {
  logger.error(`[SurveyView.vue] Showing error dialog ${message}: ${error}`);
  store.setupDialog("error", message);
  store.showDialog();

  setTimeout(() => {
    store.closeDialog();
    reset();
    start();
  }, 3000);
};

const imageURL = (employee_id) =>
  "http://" +
  import.meta.env.VITE_FASTAPI_URL +
  "/picture/employee/" +
  employee_id;

const onSelectDepartment = (department) => {
  try {
    logger.info(`[SurveyView.vue] Selected ${department}`)
    currentDep.value = department;
    currentEmp.value = null;
    currentRating.value = 0;
    reset();
  } catch (err) {
    showTemporaryError("選擇部門時發生錯誤!", err);
  }
};

const onSelectEmployee = (employee) => {
  try {
    logger.info(`[SurveyView.vue] Selected ${JSON.stringify(employee)}`)
    currentEmp.value = employee;
    reset();
  } catch (err) {
    showTemporaryError("選擇員工時發生錯誤!", err);
  }
};

const onEditEmployee = () => {
  try {
    logger.info("[SurveyView.vue] Editing employee")
    currentEmp.value = null;
    currentRating.value = 0;
    reset();
  } catch (err) {
    showTemporaryError("修改員工時發生錯誤!", err);
  }
};

const sendSurveyResult = async () => {
  stop();
  store.setupDialog("loading", "處理中，請稍候...");
  store.showDialog();
  logger.info(`[SurveyView.vue] Calling api.sendData with URL of http://${import.meta.env.VITE_FASTAPI_URL}/survey with data of ${JSON.stringify({
      employee_id: currentEmp.value.學號,
      employee_dep: currentEmp.value.主要部門,
      student_id: store.userData.學號,
      rating: currentRating.value,
    })}`);
  const surveyResult = await api.sendData(
    `http://${import.meta.env.VITE_FASTAPI_URL}/survey/`,
    { "Content-Type": "application/json" },
    {
      employee_id: currentEmp.value.學號,
      employee_dep: currentEmp.value.主要部門,
      student_id: store.userData.學號,
      rating: currentRating.value,
    }
  );

  logger.info(
    `[SurveyView.vue] Received surveyResult: ${JSON.stringify(surveyResult)}`
  );

  if (surveyResult.success == false) {
    logger.error(
      `[SurveyView.vue] ${
        store.authStudentId
      } sending survey did NOT succeed: ${JSON.stringify(surveyResult)}`
    );

    showTemporaryError(
      typeof surveyResult?.data?.detail === "string"
        ? surveyResult.data.detail
        : "系統發生錯誤"
    );
  } else {
    store.setupDialog("success", "滿意度送出成功!");
    logger.info(`[SurveyView.vue] Survey sent successfully for ${store.userData.學號} ${store.userData.姓名}`)
    setTimeout(() => {
      store.closeDialog();
      store.clearUserData();
      router.push("/");
    }, 3000);
  }
};

onMounted(() => {
  try {
    start();
    if (store.surveyIs4Math == true) {
      currentDep.value = "數輔";
    }
    store.userData.rateable_employees.forEach((employee) => {
      try {
        imageLoading[employee.學號] = true;
      } catch (e) {
        logger.error(`[SurveyView.vue] Image loading error: ${e}`)
      }
    });
  } catch (err) {
    showTemporaryError("抱歉，系統發生錯誤!", err);
  }
});
</script>

<template>
  <!-- Class Selection -->

  <div class="flex flex-row items-center justify-start w-full gap-2">
    <h3 class="text-2xl shrink-0 font-extrabold">選擇評分部門:</h3>
    <div
      class="flex flex-row flex-wrap gap-1"
      v-if="store.userData.rateable_employees"
    >
      <Button
        size="large"
        v-for="department in new Set(
          store.userData.rateable_employees.map((x) => x.主要部門)
        )"
        :key="department"
        :label="department"
        @click="onSelectDepartment(department)"
        :variant="department == currentDep ? '' : 'outlined'"
        :raised="department == currentDep"
        :disabled="department != currentDep && store.surveyIs4Math == true"
      />
    </div>
  </div>

  <div
    v-show="currentDep != ''"
    class="flex flex-row items-start justify-start w-full gap-2"
  >
    <h3 class="text-2xl shrink-0 font-extrabold">選擇評分對象:</h3>
    <ScrollPanel
      @scroll="reset()"
      v-if="currentEmp == null"
      class="w-full h-112 pr-4"
    >
      <div
        class="flex flex-col items-start justify-center gap-4"
        v-if="store.userData.rateable_employees"
      >
        <Button
          size="large"
          variant="outlined"
          v-for="employee in new Set(
            store.userData.rateable_employees.filter(
              (x) => x.主要部門 == currentDep
            )
          )"
          :key="employee.學號"
          @click="onSelectEmployee(employee)"
          class="p-8"
        >
          <transition name="out-in">
            <Skeleton
              v-if="imageLoading[employee.學號]"
              width="4rem"
              height="3rem"
              class="h-12"
            />
          </transition>

          <transition name="out-in">
            <img
              v-show="!imageLoading[employee.學號]"
              @load="imageLoading[employee.學號] = false"
              @error="imageLoading[employee.學號] = false"
              id="pfp"
              :src="imageURL(employee.學號)"
              alt=""
              class="h-12"
            />
          </transition>

          <label class="text-2xl" for="pfp">
            {{ employee.姓名 }}
          </label>
        </Button>
      </div>
    </ScrollPanel>

    <div v-else class="flex flex-row items-center justify-start gap-2">
      <Button size="large" class="p-8 text-2xl" raised
        ><img
          id="pfp"
          :src="imageURL(currentEmp.學號)"
          alt=""
          class="h-12"
        /><label class="text-2xl" for="pfp">{{
          currentEmp.姓名
        }}</label></Button
      >

      <Button
        size="large"
        variant="outlined"
        icon="pi pi-pencil"
        label="修改"
        class="shrink-0 font-extrabold"
        @click="onEditEmployee"
        rounded
      />
    </div>
  </div>

  <!-- Seat Edit -->

  <!-- Rating -->
  <div
    v-if="currentDep != '' && currentEmp != null"
    class="flex flex-row items-center justify-between gap-2 w-full"
  >
    <div class="flex flex-row gap-2 items-center">
      <h3 class="text-2xl shrink-0 font-extrabold">選擇滿意度：</h3>
      <Rating
        :style="{ '.p-rating-icon': 'font-size: 2rem !important' }"
        v-model="currentRating"
      />
    </div>
  </div>
  <Button
    size="large"
    class="w-full text-3xl font-extrabold"
    v-show="currentDep != '' && currentEmp != null && currentRating > 0"
    severity="success"
    label="送出"
    icon="pi pi-check"
    @click="sendSurveyResult"
  />
</template>

<style scoped>
/* Keep only the vertical scrollbar visible */
:deep(.p-scrollpanel-bar.p-scrollpanel-bar-y) {
  opacity: 1 !important; /* Keep vertical scrollbar visible */
  visibility: visible !important; /* Ensure vertical scrollbar is always visible */
}

/* Prevent hover/active opacity change for the vertical scrollbar */
:deep(.p-scrollpanel:hover .p-scrollpanel-bar.p-scrollpanel-bar-y),
:deep(.p-scrollpanel:active .p-scrollpanel-bar.p-scrollpanel-bar-y) {
  opacity: 1 !important;
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
::v-deep(.p-rating-icon) {
  font-size: 2rem !important;
  width: 30px;
  height: 30px;
}
</style>
