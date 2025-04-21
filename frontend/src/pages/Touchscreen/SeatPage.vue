<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { alertStore } from "../../store/alertStore";
import { commonStore } from "../../store/commonStore";
import { sendToAPI } from "../../lib/sendToAPI";
import websocketService from "../../lib/websocketService";
import Countdown from "../../lib/Countdown";
import Button from "primevue/button";
import BackButton from "../../components/buttons/BackButton.vue";

const router = useRouter();
const selectedSeat = ref("");
const isLoading = ref(false);

// Helper for consistent error reporting
const reportError = (prefix, err) => {
  websocketService.sendMessage(
    "client_error",
    `${prefix}: ${typeof err === "string" ? err : JSON.stringify(err)}`
  );
};

const countdown = new Countdown(30, () => {
  try {
    commonStore.clear();
    router.push("/home");
  } catch (err) {
    reportError("Countdown callback error", err);
  }
});

const selectSeat = (seat) => {
  try {
    selectedSeat.value = seat;
  } catch (err) {
    reportError("selectSeat error", err);
  }
};

const handleSubmit = async () => {
  isLoading.value = true;

  if (!commonStore.user_data || !selectedSeat.value) {
    reportError("handleSubmit pre-check", "Missing user_data or selectedSeat");
    alertStore.setMessage("資料不完整，請重新操作");
    router.push("/alert");
    isLoading.value = false;
    return;
  }

  try {
    const seatResult = await sendToAPI("/seat/", {
      學號: commonStore.user_data.學號,
      號碼: selectedSeat.value.號碼,
    });

    websocketService.sendMessage(
      "client_action",
      `[SeatPage.vue] seatResult: ${JSON.stringify(seatResult)}`
    );

    alertStore.setMessage(
      seatResult.code != 200 ? "發生錯誤" : "選擇完成!"
    );
    router.push("/alert");
  } catch (error) {
    reportError("Error during seat submission", error);
    alertStore.setMessage("系統錯誤，請稍後再試");
    router.push("/alert");
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  try {
    countdown.start();

    watch([selectedSeat], () => {
      websocketService.sendMessage(
        "client_action",
        "Seat selection changed, resetting countdown"
      );
      countdown.reset();
    });
  } catch (err) {
    reportError("onMounted error", err);
  }
});

onUnmounted(() => {
  try {
    countdown.stop();
  } catch (err) {
    reportError("onUnmounted error", err);
  }
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
