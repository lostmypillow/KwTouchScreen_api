<script setup>
import Button from "primevue/button";
defineProps(["number"]);
</script>
<template>
  <Button size="large"  variant="outlined" class="min-w-1/3">
    <span class="noto-mono font-bold text-2xl">{{ number }}</span>
  </Button>
</template>
