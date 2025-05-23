<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useCountdown } from "../composables/useCountdown";
import { useLogger } from "../composables/useLogger";
import { useAPI } from "../composables/useAPI";
import { store } from "../store";
const logger = useLogger();
const router = useRouter();
const api = useAPI();
const { start, reset } = useCountdown(30, () => {
  store.clearUserData();
  router.push("/");
});
const selectedSeat = ref("");

const selectSeat = (seat) => {
  try {
    logger.info(`Selected seat: ${JSON.stringify(seat)}`)
    selectedSeat.value = seat;
  } catch (err) {
    logger.error(`[SeatView.vue] selectSeat error: ${JSON.stringify(err)}`);
  }
};

const handleSubmit = async () => {
  logger.info(
    "[SeatView.vue] Submit button pressed, setting up dialog: 處理中，請稍候..."
  );
  store.setupDialog("loading", "處理中，請稍候...");
  store.showDialog();

  if (!store.userData || !selectedSeat.value) {
    logger.error(
      `[SeatView.vue] handleSubmit pre-check: Missing user_data? ${!store.userData}. SelectedSeat is null? ${!selectedSeat.value}. Setting up dialog: 資料不完整，請重新操作`
    );
    store.setupDialog("error", "資料不完整，請重新操作");
    setTimeout(() => store.closeDialog(), 3000);
    return;
  }

  try {
    logger.error(
      `[SeatView.vue] Calling API with URL of http://${
        import.meta.env.VITE_FASTAPI_URL
      }/seat/, with data of ${JSON.stringify({
        學號: store.userData.學號,
        號碼: selectedSeat.value.號碼,
      })}`
    );
    const seatResult = await api.sendData(
      `http://${import.meta.env.VITE_FASTAPI_URL}/seat/`,
      { "Content-Type": "application/json" },
      {
        學號: store.userData.學號,
        號碼: selectedSeat.value.號碼,
      }
    );

    logger.info(`[SeatView.vue] seatResult: ${JSON.stringify(seatResult)}`);
    if (seatResult.success == true) {
      logger.info(
        `[SeatView.vue] seatResult is true, showing dialog: 選擇完成!`
      );
      store.setupDialog("success", "選擇完成!");
      setTimeout(() => {
        store.closeDialog();
        store.clearUserData();
        logger.info(
          `[SeatView.vue] Closed dialog, cleared userData. Now navigating back to home`
        );
        router.push("/");
        return;
      }, 3000);
    }
  } catch (error) {
    logger.error(
      `[SeatView.vue] Error during seat submission: ${JSON.stringify(
        error
      )}, showing dialog: 抱歉! 系統發生錯誤，請洽導師!`
    );
    store.setupDialog("error", "抱歉! 系統發生錯誤，請洽導師!");
    setTimeout(() => {
      store.closeDialog();
      logger.info("Closing dialog");
    }, 3000);
  }
};
const returnGenderedSeats = () => {
  return store.userData.性別 == "男"
    ? store.ClassWithSeats.男座位
    : store.ClassWithSeats.女座位;
};
onMounted(() => {
  try {
    start();
    watch([selectedSeat], () => {
      reset();
      logger.info(
        `[SeatView.vue] Selected seat changed to ${JSON.stringify(
          selectedSeat.value
        )}, resetting and restarting countdown`
      );
    });
  } catch (err) {
    logger.error(`[SeatView.vue] onMounted error ${JSON.stringify(err)}`);
  }
});
</script>

<template>
  <div class="flex flex-col items-start justify-start gap-2 w-full">
    <h3 class="text-2xl font-extrabold">
      班級： {{ store.ClassWithSeats.班級名稱 }} ({{
        store.ClassWithSeats.班別
      }})
    </h3>

    <h3 class="text-2xl shrink-0 font-extrabold">
      選擇座位：{{ selectedSeat.座位 }}
    </h3>

    <div class="flex flex-row flex-wrap items-center justify-start gap-4">
      <Button
        class="text-xl font-extrabold"
        size="large"
        v-for="seatOption in returnGenderedSeats()"
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
</template>
