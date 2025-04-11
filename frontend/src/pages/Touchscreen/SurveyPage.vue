<script setup>
import { ref, onMounted, onUnmounted, watch, computed, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
import { alertStore } from "../../store/alertStore";
import Countdown from "../../lib/Countdown";
import Button from "primevue/button";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
import BackButton from "../../components/buttons/BackButton.vue";

const imageLoading = reactive({});
const onImageLoad = (employeeId) => {
  imageLoading[employeeId] = false;
};

// Handle image load error
const onImageError = (employeeId) => {
  imageLoading[employeeId] = false;
};

const selectedClass = ref("");
const router = useRouter();
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] Countdown expired. Clearing data and navigating to home.`
  );
  commonStore.clear();
  router.push("/");
});

const currentDep = ref("");
const handleSelectDepartment = (department) => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] handleSelectDepartment called with department: ${department}`
  );
  currentDep.value = department;
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] currentDep set to: ${
      currentDep.value
    }`
  );
  currentEmp.value = null;
  currentRating.value = 0;
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] currentEmp reset to null and currentRating reset to 0`
  );
  countdown.reset();
};

const handleEditDepartment = () => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] handleEditDepartment called`
  );
  currentDep.value = "";
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] currentDep reset to empty string`
  );
  currentEmp.value = null;
  currentRating.value = 0;
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] currentEmp reset to null and currentRating reset to 0`
  );
  countdown.reset();
};

const currentEmp = ref();
const handleSelectEmployee = (employee) => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] handleSelectEmployee called with employee: ${
      employee.姓名
    }`
  );
  currentEmp.value = employee;
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] currentEmp set to: ${
      currentEmp.value.姓名
    }`
  );
  countdown.reset();
};

const handleEditEmployee = () => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] handleEditEmployee called`
  );
  currentEmp.value = null;
  currentRating.value = 0;
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] currentEmp reset to null and currentRating reset to 0`
  );
  countdown.reset();
};
onMounted(() => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] onMounted called`
  );
  countdown.start();
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] countdown started`
  );
  commonStore.user_data.rateable_employees.forEach((employee) => {
    imageLoading[employee.學號] = true;
  });
  if (commonStore.is_math_rate == true) {
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] Setting department to '數輔' based on is_math_rate`
    );
    currentDep.value = "數輔";
    if (
      commonStore.user_data.rateable_employees.filter(
        (x) => x.主要部門 == currentDep.value
      ).length == 0
    ) {
      alertStore.setMessage("目前沒有您可評分的數輔老師!");
      router.push("/alert");
    }
  }
});

onUnmounted(() => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] onUnmounted called`
  );
  countdown.stop();
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] countdown stopped`
  );
});
const sendSurveyResult = async () => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] sendSurveyResult called`
  );
  isLoading.value = true;
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] isLoading set to true`
  );
  try {
    const surveyResult = await sendToAPI("/rate/", {
      employee_id: currentEmp.value.學號,
      employee_dep: currentEmp.value.主要部門,
      student_id: commonStore.user_data.學號,
      rating: currentRating.value,
    });
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] Survey result: ${JSON.stringify(
        surveyResult
      )}`
    );
    alertStore.setMessage(
      surveyResult.code != 200 ? "發生錯誤" : "滿意度送出成功!"
    );
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] alertStore message set`
    );
    router.push("/alert");
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] Navigating to /alert`
    );
  } catch (error) {
    console.error(
      `[SurveyPage.vue] [${new Date().toISOString()}] Error sending survey result: ${error}`
    );
    alertStore.setMessage("系統錯誤，請稍後再試");
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] alertStore message set for error`
    );
    router.push("/alert");
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] Navigating to /alert on error`
    );
  } finally {
    isLoading.value = false;
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] isLoading set to false`
    );
    commonStore.is_math_rate = false;
    console.log(
      `[SurveyPage.vue] [${new Date().toISOString()}] commonStore.is_math_rate set to false`
    );
  }
};

const currentRating = ref(0);
const isRatingZero = ref(currentRating.value == 0);

const imageURL = (employee_id) => {
  console.log(
    `[SurveyPage.vue] [${new Date().toISOString()}] imageURL called with employee_id: ${employee_id}`
  );
  return (
    "http://" +
    import.meta.env.VITE_SERVER_URL +
    "/picture/employee/" +
    employee_id
  );
};
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
        已登入為 {{ commonStore.user_data.學號 }}
        {{ commonStore.user_data.姓名 }}
      </h4>
    </div>

    <!-- Class Selection -->

    <div class="flex flex-row items-center justify-start w-full gap-2">
      <h3 class="text-2xl shrink-0 font-extrabold">選擇評分部門:</h3>
      <div class="flex flex-row flex-wrap gap-1">
        <Button
          size="large"
          v-for="department in new Set(
            commonStore.user_data.rateable_employees.map((x) => x.主要部門)
          )"
          :key="department"
          :label="department"
          @click="handleSelectDepartment(department)"
          :variant="department == currentDep ? '' : 'outlined'"
          :raised="department == currentDep"
          :disabled="
            department != currentDep && commonStore.is_math_rate == true
          "
        />
      </div>
    </div>

    <div
      v-show="currentDep != ''"
      class="flex flex-row items-center justify-start w-full gap-2"
    >
      <h3 class="text-2xl shrink-0 font-extrabold">選擇評分對象:</h3>
      <ScrollPanel
        @scroll="countdown.reset()"
        :style="{ '.p-scrollpanel-bar': 'opacity: 1 !important;' }"
        v-if="currentEmp == null"
        class="w-full h-112 pr-4"
        :dt="{
          bar: {
            background: '{primary.color}',
          },
        }"
      >
        <div class="flex flex-col items-center justify-center gap-4">
          <Button
            size="large"
            variant="outlined"
            v-for="employee in new Set(
              commonStore.user_data.rateable_employees.filter(
                (x) => x.主要部門 == currentDep
              )
            )"
            :key="employee.學號"
            @click="handleSelectEmployee(employee)"
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
        <Button size="large" class="p-8" raised
          ><img
            id="pfp"
            :src="imageURL(currentEmp.學號)"
            alt=""
            class="h-12"
          />{{ currentEmp.姓名 }}</Button
        >

        <Button
          size="large"
          variant="outlined"
          icon="pi pi-pencil"
          label="修改"
          class="shrink-0 font-extrabold"
          @click="handleEditEmployee"
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
        <Rating v-model="currentRating" />
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
</style>
