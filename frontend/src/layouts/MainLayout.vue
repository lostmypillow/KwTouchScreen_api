<script setup>
import CustomDialog from '../components/CustomDialog.vue';
import Status from '../components/Status.vue';
import VideoPlayer from '../components/bottom/VideoPlayer.vue';
</script>


<template>
    <Status />
    <router-view name="default" />
    <VideoPlayer />
  </template>
  