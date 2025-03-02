<script setup>
import Button from "primevue/button";
defineProps(["number"]);
</script>
<template>
  <Button size="small"  variant="outlined" class="min-w-1/3">
    <span class="noto-mono font-bold">{{ number }}</span>
  </Button>
</template>
