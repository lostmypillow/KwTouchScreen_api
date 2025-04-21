<script setup>
import { RouterView } from "vue-router";
import { onMounted } from "vue";
import VideoPlayer from "../../components/bottom/VideoPlayer.vue";
import Status from "../../components/top/Status.vue";
import websocketService from "../../lib/websocketService";

onMounted(() => websocketService.initializeWebSocket());
</script>

<template>
  <div class="flex flex-col items-center justify-between h-svh w-svw">
    <Status />
    <router-view />
    <VideoPlayer />
  </div>
</template>
