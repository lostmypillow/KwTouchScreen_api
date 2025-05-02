<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useCountdown } from "../composables/useCountdown";
import HomeButton from "../components/buttons/HomeButton.vue";
import { useLogger } from "../composables/useLogger";
import { store } from "../store";
import { useAPI } from "../composables/useAPI";
const logger = useLogger();
const router = useRouter();
const api = useAPI();
const { start, reset, stop } = useCountdown(30, () => {
  store.clearUserData();
  router.push("/");
});
const selectedSeat = ref("");


const selectSeat = (seat) => {
  try {
    selectedSeat.value = seat;
  } catch (err) {
    logger.error(`selectSeat error: ${err}`);
  }
};

const handleSubmit = async () => {
  store.setupDialog("loading", "處理中，請稍候...");
  store.showDialog();

  if (!store.userData || !selectedSeat.value) {
    logger.error("handleSubmit pre-check: Missing user_data or selectedSeat");
    store.setupDialog("error", "資料不完整，請重新操作");
    setTimeout(() => store.closeDialog(), 3000);
    return;
  }

  try {
    const seatResult = await api.sendData(
      `http://${import.meta.env.VITE_FASTAPI_URL}/seat/`,
      { "Content-Type": "application/json" },
      {
        學號: store.userData.學號,
        號碼: selectedSeat.value.號碼,
      }
    );

    logger.info(`[SeatPage.vue] seatResult: ${JSON.stringify(seatResult)}`);
    if (seatResult.success == true) {
      store.setupDialog("success", "選擇完成!");
      setTimeout(() => {
        store.closeDialog();
        store.clearUserData();
        router.push("/");
        return;
      }, 3000);
    }
  } catch (error) {
    logger.error(`Error during seat submission ${JSON.stringify(error)}`);
    store.setupDialog("error", "抱歉! 系統發生錯誤，請洽導師!");
    setTimeout(() => store.closeDialog(), 3000);
  }
};

onMounted(() => {
  try {
    start();
    watch([selectedSeat], () => reset());
  } catch (err) {
    logger.error(`onMounted error ${JSON.stringify(err)}`);
  }
});
</script>

<template>
  <div
    class="flex flex-col items-center justify-start w-full h-full gap-4 p-4 text-2xl"
  >
    <div class="flex flex-row w-full items-center justify-between">
      <div class="flex flex-row gap-2 items-center">
        <HomeButton />
        <h1 class="text-4xl font-extrabold">今日補位</h1>
      </div>

      <h4 class="text-base">
        已登入為 {{ store.userData.學號 }}
        {{ store.userData.姓名 }}
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
        @click="handleSubmit"
        icon="pi pi-check"
        size="large"
      />
    </div>
  </div>
</template>
