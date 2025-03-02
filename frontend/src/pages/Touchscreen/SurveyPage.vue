<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { alertStore } from "../../store/alertStore";
import Countdown from "../../lib/Countdown";
import Button from "primevue/button";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
const selectedClass = ref("");
const router = useRouter();
const isLoading = ref(false);
const countdown = new Countdown(30, () =>{
  commonStore.clear()
  router.push("/app")});

const currentDep = ref("");
const handleSelectDepartment = (department) => {
  currentDep.value = department;
  currentEmp.value = null;
  currentRating.value = 0
  countdown.reset();
};
const handleEditDepartment = () => {
  currentDep.value = "";
  currentEmp.value = null;
  currentRating.value = 0
  countdown.reset();
};

const currentEmp = ref();
const handleSelectEmployee = (employee) => {
  currentEmp.value = employee;
  countdown.reset();
};
const handleEditEmployee = () => {
  currentEmp.value = null;
  currentRating.value = 0
  countdown.reset();
};

const sendSurveyResult = async () => {
  isLoading.value = true;
  const surveyResult = await sendToAPI(
    '/rate/',
    {
      employee_id:  currentEmp.value.學號,
      employee_dep: currentEmp.value.主要部門,
      student_id: commonStore.user_data.學號,
      rating:  currentRating.value,
    } 
  );
  alertStore.setMessage(
    surveyResult.code != 200 ? "發生錯誤" : "滿意度送出成功!"
  );
  router.push("/app/alert");
  isLoading.value = false;
  commonStore.is_math_rate = false
};
const currentRating = ref(0);
const isRatingZero = ref(currentRating.value == 0)
onMounted(() => {
  countdown.start();
 
  
  if (commonStore.is_math_rate == true) {
    currentDep.value = "數輔"
  }
});
onUnmounted(() => countdown.stop());

const imageURL = (employee_id) => {
  return (
    "http://" +
    import.meta.env.VITE_SERVER_URL +
    "/picture/employee/" +
    employee_id
  );
};
</script>
<template>
  <div class="flex flex-col items-center justify-center w-full h-full gap-4 p-4 text-xl">
    <!-- Class Selection -->
 
    <div
      class="flex flex-row flex-wrap items-center justify-start gap-2"
    >
      <h3>選擇部門： {{ selectedClass }}</h3>

      <Button
        v-for="department in new Set(
          commonStore.user_data.rateable_employees.map((x) => x.主要部門)
        )"
        :key="department"
        :label="department"
        @click="handleSelectDepartment(department)"
        :variant="department == currentDep ? '' : 'outlined'"
        :disabled="department != currentDep && commonStore.is_math_rate == true"
      /> 
    </div>

    <div
      v-show="currentDep != ''"
      class="flex flex-row items-center justify-center gap-2 w-full"
    >
      <h3 class="shrink-0">選擇員工：</h3>
      <ScrollPanel
      @scroll="countdown.reset()"
        style=".p-scrollpanel-bar: opacity: 1 !important;"
        v-if="currentEmp == null"
        class="w-fit h-56 pr-4"
        :dt="{
          bar: {
            background: '{primary.color}',
          },
        }"
      >
        <div class="flex flex-col items-center justify-center gap-4">
          <Button
            v-for="employee in new Set(
              commonStore.user_data.rateable_employees.filter(
                (x) => x.主要部門 == currentDep
              )
            )"
            :key="employee.學號"
            @click="handleSelectEmployee(employee)"
            class="p-8"
          >
            <img id="pfp" :src="imageURL(employee.學號)" alt="" class="h-12" />

            <label class="text-2xl" for="pfp">
              {{ employee.姓名 }}
            </label>
          </Button>
        </div>
      </ScrollPanel>

      <div v-else class="flex flex-row items-center justify-start gap-2">
        {{ currentEmp.姓名 }}

        <Button
          icon="pi pi-pencil"
          label="編輯"
          @click="handleEditEmployee"
          severity="success"
        />
      </div>
    </div>

    <!-- Seat Edit -->

    <!-- Rating -->
    <div
      v-if="currentDep != '' && currentEmp != null"
      class="flex flex-row items-center justify-center gap-2 w-full"
    >
      <h3>選擇滿意度：</h3>
      <Rating v-model="currentRating" />
    </div>

    <div
      class="flex flex-row items-center justify-end gap-4 w-full"
      v-show="currentDep != '' && currentEmp != null && currentRating > 0"
    >
      <span>確定選擇後，請按送出: </span>
      <Button
        :loading="isLoading"
        severity="success"
        label="送出"
        icon="pi pi-check"
        @click="sendSurveyResult"
      />
    </div>
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
</style>
