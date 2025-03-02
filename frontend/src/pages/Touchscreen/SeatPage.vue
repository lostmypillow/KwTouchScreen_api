<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { alertStore } from "../../store/alertStore";
import { useRoute } from "vue-router";
import Countdown from "../../lib/countdown";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
import Button from "primevue/button";
const router = useRouter();
const selectedSeat = ref("");
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  commonStore.clear();
  router.push("/app/home");
});
const selectSeat = (seat) => (selectedSeat.value = seat);
const resetSeat = () => (selectedSeat.value = "");
const handleSubmit = async () => {
  isLoading.value = true;
  const seatResult = await sendToAPI("/seat/", {
    學號: commonStore.user_data.學號,
    號碼: selectedSeat.value.號碼,
  });
  alertStore.setMessage(seatResult.code != 200 ? "發生錯誤" : "選擇完成!");
  isLoading.value = false;
  router.push("/app/alert");
};

onMounted(() => {
  countdown.start();
  watch([selectedSeat], () => countdown.reset());
});

onUnmounted(() => countdown.stop());
</script>
<template>
  <div class="flex flex-col items-start justify-center w-full h-full gap-4 px-8">
    <div class="flex flex-row items-center justify-start gap-2 mb-4">
      <h3>
        班級： {{ commonStore.today_class_4_display }} ({{
          commonStore.today_class_4_auth
        }})
      </h3>
    </div>

    <!-- Seat Selection -->
    <div>
      <div
        v-if="selectedSeat === ''"
        class="flex flex-row flex-wrap items-center justify-start gap-2"
      >
        <h3>選擇座位：</h3>
        <Button
          size="small"
          v-for="seatOption in commonStore.seats()"
          :key="seatOption.號碼"
          :label="seatOption.座位"
          @click="selectSeat(seatOption)"
        />
      </div>

      <!-- Seat Edit -->
      <div v-else class="flex flex-row items-center justify-start gap-2">
        <h3>
          選擇座位：
          {{ selectedSeat.座位 }}
        </h3>
        <Button
          icon="pi pi-pencil"
          label="編輯"
          @click="resetSeat"
          severity="success"
        />
      </div>
    </div>

    <!-- Submit Button -->
    <div
      v-if="selectedSeat !== ''"
      class="flex flex-row items-center justify-end gap-2 w-full"
    >
      <span>確定選擇後，請按送出:</span>
      <Button
        severity="success"
        label="送出"
        :loading="isLoading"
        @click="handleSubmit"
        icon="pi pi-check"
      />
    </div>
  </div>
</template>
