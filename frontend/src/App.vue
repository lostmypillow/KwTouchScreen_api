<script setup>
import { RouterView } from "vue-router";
import { dialogStore } from "./store_old/dialogStore";
import { useWebSocket } from "./composables/useWebSocket";
import { store } from "./store";
import { watch } from "vue";
const ws = useWebSocket()
watch(ws.receivedMessage, (newMessage) => {

if (newMessage.action == "update class") {
  store.classWithSeats = newMessage.message.class_with_seats
  store.classesToday = newMessage.message.classes_today
  
  // classesToday.value = ;
  // classWithSeat.value = ;
  // commonStore.today_class_4_auth = classWithSeat.value.班別
  //   ? classWithSeat.value.班別
  //   : "";
  // commonStore.today_class_4_display = classWithSeat.value.班級名稱;
  // commonStore.male_seats = classWithSeat.value.男座位;
  // commonStore.female_seats = classWithSeat.value.女座位;
}
});
</script>

<template>
  <div class="flex flex-col items-center justify-between h-svh w-svw">
    <CustomDialog
      v-model="store.dialogVisibility"
      :text="store.dialogMessage"
      :iconClass="store.dialogClass"
    />
    <!-- {{ ws.receivedMessage  }} -->
    <router-view />
  </div>
</template>
