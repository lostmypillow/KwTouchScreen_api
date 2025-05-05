<script setup>
import { RouterView } from "vue-router";
import { useWebSocket } from "./composables/useWebSocket";
import { store } from "./store";
import { watch } from "vue";
const ws = useWebSocket();
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
    <!-- {{ ws.receivedMessage  }} -->
    <router-view />
  </div>
</template>
