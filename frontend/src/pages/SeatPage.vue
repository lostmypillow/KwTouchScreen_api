<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { userStore } from "../store/userStore";
import { alertStore } from "../store/alertStore";
import { statusStore } from "../store/statusStore";
import { useRoute } from "vue-router";
import { postSeats } from "../lib/postSeats";
import Countdown from "../lib/countdown";
const router = useRouter();
const selectedSeat = ref("");
const isLoading = ref(false)
const countdown = new Countdown(30, () => router.push("/"));
const selectSeat = (seat) => selectedSeat.value = seat
const resetSeat = () => selectedSeat.value = ""
const handleSubmit = async () => {
  isLoading.value = true
  const seatResult = await postSeats(selectedSeat.value);
  alertStore.setMessage(seatResult.status != 200 ? "發生錯誤" : "選擇完成!");
  isLoading.value = false
  router.push("/alert");
};

onMounted(() => {
  countdown.start();
  const route = useRoute();
  watch([route, selectedSeat], () => countdown.reset());
});

onUnmounted(() => countdown.stop());
</script>
<template>
  <div>
    <div class="flex flex-row items-center justify-start gap-2 mb-4">
      <h3>
        班級： {{ statusStore.today_class.name }} ({{
          statusStore.today_class.other_name
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
          v-for="seatOption in statusStore.returnSeats(userStore.gender)"
          :key="seatOption.sn"
          :label="seatOption.name"
          @click="selectSeat(seatOption.sn)"
        />
      </div>

      <!-- Seat Edit -->
      <div v-else class="flex flex-row items-center justify-start gap-2">
        <h3>
          選擇座位：
          {{
            statusStore
              .returnSeats(userStore.gender)
              .find((item) => item.sn == selectedSeat)["name"]
          }}
        </h3>
        <Button
          rounded
          size="small"
          variant="outlined"
          icon="pi pi-pencil"
          label="編輯"
          @click="resetSeat"
          severity="success"
        />
      </div>
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
</template>
