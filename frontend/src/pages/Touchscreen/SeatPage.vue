<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { alertStore } from "../../store/alertStore";
import { useRoute } from "vue-router";
import Countdown from "../../lib/Countdown";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
import Button from "primevue/button";

const router = useRouter();
const selectedSeat = ref("");
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  commonStore.clear();
  router.push("/home");
});

const selectSeat = (seat) => {
  console.log(
    `[SeatPage.vue] [${new Date().toISOString()}] Selected Seat: ${seat}`
  );
  selectedSeat.value = seat;
};

const resetSeat = () => {
  console.log(
    `[SeatPage.vue] [${new Date().toISOString()}] Resetting seat selection.`
  );
  selectedSeat.value = "";
};

const handleSubmit = async () => {
  console.log(
    `[SeatPage.vue] [${new Date().toISOString()}] Handling submit...`
  );
  isLoading.value = true;
  try {
    const seatResult = await sendToAPI("/seat/", {
      學號: commonStore.user_data.學號,
      號碼: selectedSeat.value.號碼,
    });
    console.log(
      `[SeatPage.vue] [${new Date().toISOString()}] seatResult: ${JSON.stringify(
        seatResult
      )}`
    );
    alertStore.setMessage(seatResult.code != 200 ? "發生錯誤" : "選擇完成!");
    router.push("/alert");
  } catch (error) {
    console.error(
      `[SeatPage.vue] [${new Date().toISOString()}] Error during seat submission: ${error}`
    );
    alertStore.setMessage("系統錯誤，請稍後再試");
    router.push("/alert");
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  console.log(
    `[SeatPage.vue] [${new Date().toISOString()}] Mounted and starting countdown...`
  );
  countdown.start();
  watch([selectedSeat], () => {
    console.log(
      `[SeatPage.vue] [${new Date().toISOString()}] Seat selection changed, resetting countdown...`
    );
    countdown.reset();
  });
});

onUnmounted(() => {
  console.log(
    `[SeatPage.vue] [${new Date().toISOString()}] Unmounted and stopping countdown...`
  );
  countdown.stop();
});
</script>

<template>
  <div
    class="flex flex-col items-center justify-start w-full h-full gap-4 p-4 text-2xl"
  >
    <div class="flex flex-row w-full items-center justify-between">
      <div class="flex flex-row gap-2 items-center">
        <BackButton />
        <h1 class="text-4xl font-extrabold">今日補位</h1>
      </div>

      <h4 class="text-base">
        已登入為 {{ commonStore.user_data.學號 }}
        {{ commonStore.user_data.姓名 }}
      </h4>
    </div>

    <div class="flex flex-row items-start justify-start gap-2 mb-4 w-full">
      <h3 class="text-2xl shrink-0 font-extrabold">班級：</h3>
      {{ commonStore.today_class_4_display }} ({{
        commonStore.today_class_4_auth
      }})
    </div>

    <!-- Seat Selection -->

    <div class="flex flex-col items-start justify-start gap-2 w-full">
      <h3 class="text-2xl shrink-0 font-extrabold">選擇座位：</h3>
      {{ selectedSeat.座位 }}

      <div class="flex flex-row flex-wrap items-center justify-start gap-4">
        <Button
          class="text-xl font-extrabold"
          size="large"
          v-for="seatOption in commonStore.seats()"
          :key="seatOption.號碼"
          :label="seatOption.座位"
          @click="selectSeat(seatOption)"
          :raised="selectedSeat.座位 == seatOption.座位"
          :variant="selectedSeat.座位 == seatOption.座位 ? '' : 'outlined'"
        />
      </div>
    </div>

    <!-- Submit Button -->
    <div
      v-if="selectedSeat !== ''"
      class="flex flex-row items-center justify-end gap-2 w-full"
    >
      <Button
        class="w-full"
        severity="success"
        label="送出"
        :loading="isLoading"
        @click="handleSubmit"
        icon="pi pi-check"
        size="large"
      />
    </div>
  </div>
</template>
