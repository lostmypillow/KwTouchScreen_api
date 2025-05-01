<script setup>
import { useRouter } from "vue-router";
import { store } from "../../store";
const router = useRouter();
const goHome = () => {
  store.clearUserData()
  router.push("/");
};
</script>

<template>
  <Button size="large" @click="goHome"
    ><i class="pi pi-home"></i>回主畫面</Button
  >
</template>
