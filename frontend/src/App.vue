<script setup>
import { RouterView, useRoute, useRouter } from "vue-router";


</script>

<template>
  <div class="flex flex-col items-center justify-between h-svh w-svw">
    <!-- <Status /> -->

    <router-view />
    <!-- <VideoPlayer /> -->
  </div>
</template>
