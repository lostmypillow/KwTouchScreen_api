<script setup>
import { onMounted, onUnmounted } from "vue";
import { ref } from "vue";
import { fetchImage } from "../lib/fetchImage";
const imageSrc = ref("");
const props = defineProps(["employee_id"]);
onMounted(async () => (imageSrc.value = await fetchImage(props.employee_id)));
onUnmounted(() => URL.revokeObjectURL(imageSrc.value));
</script>
<template>
  <img id="pfp" :src="imageSrc" alt="" class="h-12" />
</template>
