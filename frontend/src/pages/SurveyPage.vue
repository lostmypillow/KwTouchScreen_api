<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { userStore } from "../store/userStore";
import { surveyStore } from "../store/surveyStore";
import { alertStore } from "../store/alertStore";
import { postSurvey } from "../lib/postSurvey";
import Countdown from "../lib/countdown";
const selectedClass = ref("");
const router = useRouter();
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  console.log("Countdown expired, navigating to home...");
  userStore.clear()
  surveyStore.clear()
  router.push("/");
});


const handleSelectDepartment = (department) => {
  surveyStore.setDepartment(department);
  countdown.reset();
};
const handleEditDepartment = () => {
  surveyStore.resetDepartment();
  surveyStore.resetEmployee();
  countdown.reset();
};

const handleSelectEmployee = (employee) => {
  surveyStore.setEmployee(employee);
  countdown.reset();
};
const handleEditEmployee = () => {
  surveyStore.resetEmployee();
  countdown.reset();
};

const sendSurveyResult = async () => {
  isLoading.value = true;
  const surveyResult = await postSurvey();
  alertStore.setMessage(surveyResult.status != 200 ? "發生錯誤" : "滿意度送出成功!");
  router.push("/alert");
  isLoading.value = false;
};



onMounted(() => {
  countdown.start();
  const route = useRoute();
  watch(route, () => countdown.reset());
});

onUnmounted(() => countdown.stop());
</script>
<template>
  <div class="flex flex-col items-start justify-start w-full h-full gap-4">
    <!-- Class Selection -->
    <div
      v-if="surveyStore.hasNoDepartment()"
      class="flex flex-row flex-wrap items-center justify-start gap-2"
    >
      <h3>選擇部門： {{ selectedClass }}</h3>

      <Button
        size="small"
        rounded
        v-for="department in surveyStore.departmentList()"
        :key="department.number"
        :label="department.name"
        @click="handleSelectDepartment(department)"
      />
    </div>

    <!-- Class Edit -->
    <div v-else class="flex flex-row items-center justify-start gap-2">
      <h3>選擇部門： {{ surveyStore.selectedDepartment.name }}</h3>

      <Button
        :disabled="surveyStore.selectedDepartment.number == 9"
        rounded
        size="small"
        icon="pi pi-pencil"
        label="編輯"
        @click="handleEditDepartment"
        severity="success"
        variant="outlined"
      />
    </div>

    <!-- Seat Selection -->

    <div
      v-if="!surveyStore.hasNoDepartment()"
      class="flex items-start justify-start gap-2 w-full"
    >
      <h3 class="shrink-0">選擇員工：</h3>
      <ScrollPanel
        style=" .p-scrollpanel-bar: opacity: 1 !important;"
        v-if="surveyStore.hasNoEmployee()"
        class="w-full h-36 pr-4"
        :dt="{
          bar: {
            background: '{primary.color}',
          },
        }"
      >
        <div class="flex flex-col gap-4">
          <Button
            size="small"
            rounded
            v-for="employee in surveyStore.filteredEmployees()"
            :key="employee.id"
            @click="handleSelectEmployee(employee)"
          >
            <img
              id="pfp"
              :src="'http://192.168.2.17:8001/picture/employee/' + employee.id"
              alt=""
              class="h-12"
            />

            <label for="pfp">
              {{ employee.name }}
            </label>
          </Button>
        </div>
      </ScrollPanel>

      <div v-else class="flex flex-row items-start justify-start gap-2">
        {{ surveyStore.selectedEmployee.name }}

        <Button
          rounded
          size="small"
          variant="outlined"
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
      v-if="surveyStore.showRating()"
      class="flex flex-row items-center justify-start gap-2 w-full"
    >
      <h3>選擇滿意度：</h3>
      <Rating v-model="surveyStore.rating" />
    </div>

    <div
      class="flex flex-row items-center justify-end gap-4 w-full"
      v-show="surveyStore.allFinished()"
    >
      <span>確定選擇後，請按送出: </span>
      <Button
        :loading="isLoading"
        severity="success"
        label="送出"
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
