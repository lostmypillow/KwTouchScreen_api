<script setup>
import { useRouter } from "vue-router";
import { Button } from "primevue";
import { surveyStore } from "../store/surveyStore";
import { alertStore } from "../store/alertStore";
import { onMounted } from "vue";
import { userStore } from "../store/userStore";
const router = useRouter();
const mathRoute = () => {
  surveyStore.selectedDepartment = {
    number: 9,
    name: "數輔",
  };
  router.push("/auth/survey");
};

const temporaryRedirect = () => {
  alertStore.setMessage("未開放功能")
  router.push('/alert')
}

onMounted(() =>{
  userStore.clear()

})
</script>
<!-- TODO button size -->
<template>
  <div
    class="grid grid-rows-2 grid-cols-2 w-full h-full"
  >
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        rounded 
        @click="router.push('/auth/seats')"
        label="今日補位"
      />
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        rounded 
        @click="temporaryRedirect"
        label="獎學金申請"
      />
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full text-sm"
        rounded 
        @click="router.push('/auth/survey')"
        label="滿意度調查"
      />
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        @click="mathRoute"
        rounded 
        label="數學輔導老師教學品質"
      />
    </div>
  </div>
</template>
