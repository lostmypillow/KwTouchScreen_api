<script setup>
import { useRouter } from 'vue-router';
import { commonStore } from '../../store/commonStore';
const router = useRouter()
const goHome = () => {
  console.log(`[Status.vue] [${new Date().toISOString()}] goHome function called`);
  router.push("/home");
  commonStore.clear();
};
</script>

<template>
    <Button
size="large"
        @click="goHome"
      ><i class="pi pi-home"></i>回主畫面</Button>
</template>