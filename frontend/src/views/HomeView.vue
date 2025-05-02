<script setup>
import { useRouter } from "vue-router";
import { useLogger } from "../composables/useLogger";
import { store } from "../store";
import { useAPI } from "../composables/useAPI";
import { v1 as uuidv1 } from "uuid";
const router = useRouter();
const logger = useLogger();
const api = useAPI()
const routeToAuth = (authType) => {
  if (authType == "mathSurvey") {
    store.surveyIs4Math = true;
    authType = "survey";
  }

  store.authType = authType;

  if (store.authType == "seat" && store.checkSeatsAvailbility() == false) {
    store.setupDialog("error", `目前沒有您可選的補位資料`);
    store.showDialog();
    setTimeout(() => store.closeDialog(), 3000);
    return;
  }

  try {
    router.push("/auth");
    return;
  } catch (err) {
    logger.error(`Navigation error to '${authType}': ${JSON.stringify(err)}`);
    store.setupDialog("error", `系統發生錯誤!`);
    store.showDialog();
    setTimeout(() => store.closeDialog(), 3000);
    return;
  }
};
const c = async () => {
  const v = await api.getApplicableAwards('300003')
  console.log(v)
}
</script>
<template>
  <button @click="c">meow</button>
  <div class="pt-4 grid grid-rows-2 grid-cols-2 w-full h-full">
    <div class="w-full h-full p-4">
      <Button
        class="h-full w-full flex-1 text-center"
        rounded
        @click="() => routeToAuth('seat')"
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
        @click="() => routeToAuth('mathSurvey')"
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
