<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import { commonStore } from "../store_old/commonStore";
import { useWebSocket } from "../composables/useWebSocket";
import { store } from "../store";
import { useLogger } from "../composables/useLogger";
const dialogIcon = ref("");
const dialogText = ref("");
const isLoading = ref(false);
const router = useRouter();
const ws = useWebSocket();
const logger = useLogger();
const routeToMathSurvey = () => {
  store.surveyIs4Math = true;
  routeToAuth("survey");
};

const routeToAuth = (authType) => {
  logger.info(store.checkSeatsAvailbility());
  store.authType = authType;

  if (store.authType == "seat" && store.checkSeatsAvailbility() == false) {
    store.setupDialog("error", "目前沒有您可選的補位資料");
    store.showDialog();
    setTimeout(() => store.closeDialog(), 3000);
    return;
  }
  try {
    router.push("/auth");
  } catch (err) {
    logger.error("client_error", `Navigation error to '${path}': ${err}`);
  }
};
</script>
<template>
  <div class="pt-4 grid grid-rows-2 grid-cols-2 w-full h-full">
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center"
        rounded
        @click="routeToAuth('seat')"
        label="今日補位"
      >
        <span class="text-3xl break-words">今日補位</span>
      </Button>
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        rounded
        @click="() => routeToAuth('award')"
        label="獎學金申請"
      >
        <span class="text-3xl break-words">獎學金申請</span>
      </Button>
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full text-sm"
        rounded
        @click="() => routeToAuth('survey')"
        label="滿意度調查"
      >
        <span class="text-3xl break-words">滿意度調查</span>
      </Button>
    </div>
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center text-[calc(1vw+1em)] break-words"
        @click="routeToMathSurvey"
        rounded
        label="數學輔導老師教學品質"
      >
        <span class="text-3xl break-words"
          >數學輔導老師 <br />
          教學品質</span
        >
      </Button>
    </div>
  </div>
</template>
