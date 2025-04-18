<script setup>
import { useRouter } from "vue-router";
import { alertStore } from "../../store/alertStore";
import { onMounted } from "vue";

import { commonStore } from "../../store/commonStore";
const router = useRouter();
const mathRoute = () => {
  commonStore.is_math_rate = true
  router.push("/auth/survey");
};

</script>
<template>
  <div class="pt-4 grid grid-rows-2 grid-cols-2 w-full h-full">
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center "
        rounded
        @click="router.push('/auth/seats')"
        label="今日補位">
      <span class="text-3xl break-words">今日補位</span>
      </Button>
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        rounded
        @click="router.push('/auth/awards')"
        label="獎學金申請">
        <span class="text-3xl break-words">獎學金申請</span></Button>
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full text-sm"
        rounded
        @click="router.push('/auth/survey')"
        label="滿意度調查">
        <span class="text-3xl break-words">滿意度調查</span>
      </Button>
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full  w-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        @click="mathRoute"
        rounded
        label="數學輔導老師教學品質">
        <span class="text-3xl break-words">數學輔導老師 <br> 教學品質</span></Button>
    </div>
  </div>
</template>
