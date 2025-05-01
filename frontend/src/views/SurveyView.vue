<script setup>
import { ref, onMounted, onUnmounted, watch, computed, reactive } from "vue";
import { useRouter } from "vue-router";
import { dialogStore } from "../store_old/dialogStore";
import Countdown from "../lib/Countdown";
import Button from "primevue/button";
import { commonStore } from "../store_old/commonStore";
import { sendToAPI } from "../lib/sendToAPI";
import BackButton from "../components/buttons/HomeButton.vue";
import websocketService from "../lib/websocketService";
import { store } from "../store";
import { useCountdown } from "../composables/useCountdown";
import { useLogger } from "../composables/useLogger";
const logging = useLogger()
const router = useRouter();
const isLoading = ref(false);
const currentDep = ref("");
const currentRating = ref(0);
const imageLoading = reactive({});
const currentEmp = ref();

const reportError = (prefix, error) => {
  websocketService.sendMessage(
    "client_error",
    `${prefix}: ${typeof error === "string" ? error : JSON.stringify(error)}`
  );
};
const showTemporaryError = (message) => {
  store.setupDialog("error", message);
  store.showDialog()

  setTimeout(() => {
    store.closeDialog();
    reset();
    start();
  }, 3000);
};
const { start, reset, stop } = useCountdown(30, () => {
  store.clearUserData()
  router.push("/");
});
const onImageLoad = (employeeId) => {
  imageLoading[employeeId] = false;
};

const onImageError = (employeeId) => {
  imageLoading[employeeId] = false;
};

const imageURL = (employee_id) => {
  try {
    return (
      "http://" +
      import.meta.env.VITE_FASTAPI_URL +
      "/picture/employee/" +
      employee_id
    );
  } catch (err) {
    logging.error(`imageURL generation error ${JSON.stringify(err)}`);
    return;
  }
};

const onSelectDepartment = (department) => {
  try {
    currentDep.value = department;
    currentEmp.value = null;
    currentRating.value = 0;
    reset();
  } catch (err) {
    reportError("onSelectDepartment error", err);
  }
  // console.log('Selected dep:')
  // console.log(typeof department)
  // console.log(department)
};

const onSelectEmployee = (employee) => {
  try {
    currentEmp.value = employee;
    reset();
  } catch (err) {
    reportError("onSelectEmployee error", err);
  }
  // console.log("Selected Employee:")
  // console.log(typeof employee)
  // console.log(employee)
};

const onEditEmployee = () => {
  try {
    currentEmp.value = null;
    currentRating.value = 0;
    reset();
  } catch (err) {
    reportError("onEditEmployee error", err);
  }
};

const sendSurveyResult = async () => {
  isLoading.value = true;

  try {
    const surveyResult = await sendToAPI("/survey/", {
      employee_id: currentEmp.value.學號,
      employee_dep: currentEmp.value.主要部門,
      student_id: store.userData.學號,
      rating: currentRating.value,
    });

    dialogStore.setMessage(
      surveyResult.code != 200 ? "發生錯誤" : "滿意度送出成功!"
    );
    router.push("/alert");
  } catch (error) {
    reportError("sendSurveyResult exception", error);
    commonStore.is_math_rate = false;
    dialogStore.setMessage("系統錯誤，請稍後再試");
    router.push("/alert");
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  try {
    start();
    if (store.surveyIs4Math) {
      currentDep.value = "數輔"
    }
    store.userData.rateable_employees.forEach((employee) => {
      try {
        imageLoading[employee.學號] = true;
      } catch (e) {
        reportError("imageLoading init error", e);
      }
    });
  } catch (err) {
    reportError("onMounted error", err);
  }
});

</script>


<template>
  <div
    class="flex flex-col items-center justify-start w-full h-full gap-4 p-4 text-2xl"
  >
    <div class="flex flex-row w-full items-center justify-between">
      <div class="flex flex-row items-center justify-start gap-2">
        <BackButton />
        <h1 class="text-4xl font-extrabold">滿意度調查</h1>
      </div>

      <h4 class="text-base">
        已登入為 {{ store.userData.學號 }}
        {{ store.userData.姓名 }}
      </h4>
    </div>

    <!-- Class Selection -->

    <div class="flex flex-row items-center justify-start w-full gap-2">
      <h3 class="text-2xl shrink-0 font-extrabold">選擇評分部門:</h3>
      <div class="flex flex-row flex-wrap gap-1" v-if="store.userData.rateable_employees">
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
          :disabled="
            department != currentDep && store.surveyIs4Math == true
          "
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
        :style="{ '.p-scrollpanel-bar': 'opacity: 1 !important' }"
        v-if="currentEmp == null"
        class="w-full h-112 pr-4"
        :dt="{
          bar: {
            background: '{primary.color}',
          },
        }"
      >
        <div class="flex flex-col items-start justify-center gap-4" v-if="store.userData.rateable_employees">
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
                @load="onImageLoad(employee.學號)"
                @error="onImageError(employee.學號)"
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
        <Rating :style="{'.p-rating-icon':'font-size: 2rem !important'}" v-model="currentRating" />
      </div>
    </div>
    <Button
      size="large"
      class="w-full text-3xl font-extrabold"
      v-show="currentDep != '' && currentEmp != null && currentRating > 0"
      :loading="isLoading"
      severity="success"
      label="送出"
      icon="pi pi-check"
      @click="sendSurveyResult"
    />
  </div>
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
  height:30px;
}
</style>
