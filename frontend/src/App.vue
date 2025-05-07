<script setup>
import { RouterView } from "vue-router";
import { useWebSocket } from "./composables/useWebSocket";
import { store } from "./store";
import { watch } from "vue";
import { useLogger } from "./composables/useLogger";
const ws = useWebSocket();
const logger = useLogger()
watch(ws.receivedMessage, (newMessage) => {
  if (newMessage.action == "update class") {
    store.ClassWithSeats = newMessage.message.class_with_seats;
    store.ClassesToday = newMessage.message.classes_today;
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
    <router-view />
  </div>
</template>
