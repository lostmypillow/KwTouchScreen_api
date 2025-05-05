<script setup>
import Status from '../components/Status.vue';
import VideoPlayer from '../components/VideoPlayer.vue';
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import MiddleLayout from './MiddleLayout.vue';

const route = useRoute()

// Wrap in MiniLayout if meta says so
const useMiddleLayout = computed(() => route.meta.useMiniLayout === true)
</script>


<template>
    <Status />
    
    <template v-if="useMiddleLayout">
      <MiddleLayout>
        <router-view />
      </MiddleLayout>
    </template>
    <template v-else>
      <router-view />
    </template>
    <VideoPlayer />
  </template>
  