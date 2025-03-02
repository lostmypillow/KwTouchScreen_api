<script setup>
import { RouterView, useRoute, useRouter } from "vue-router";
import {
  onMounted,
  onUnmounted,
  onBeforeUpdate,
  ref,
  onUpdated,
  watch,
  useTemplateRef,
  nextTick,
} from "vue";
import VideoPlayer from "../../components/bottom/VideoPlayer.vue";
import Status from "../../components/top/Status.vue"
import websocketService from "../../lib/websocketService";

const route = useRoute();

onMounted(() => {
  websocketService.initializeWebSocket();
  websocketService.sendMessage("heartbeat");
});


</script>

<template>
  <div class="flex flex-col items-center justify-between h-svh w-svw">
    <Status />

    <router-view />
    <VideoPlayer />
  </div>
</template>
