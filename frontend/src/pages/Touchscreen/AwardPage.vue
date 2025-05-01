<script setup>
import BackButton from "../../components/buttons/HomeButton.vue";
import { commonStore } from "../../store_old/commonStore";
import { ref, onMounted, onUnmounted } from "vue";
import Numpad from "../../components/Numpad.vue";
import { sendToStuAPI } from "../../lib/sendToStuAPI";
import { dialogStore } from "../../store_old/dialogStore";
import { useRouter } from "vue-router";
import Countdown from "../../lib/Countdown";
import websocketService from "../../lib/websocketService";
const router = useRouter();
const selectedCourse = ref();
const score = ref("");
const ranking = ref("");
const isLoading = ref(false);
const countdown = new Countdown(30, () => {
  commonStore.clear();
  router.push("/home");
});
const dummySubmit = () => console.log(score.value);

const callAPI = async () => {
  if (!selectedCourse.value || !commonStore.user_data) {
    websocketService.sendMessage(
      "client_error",
      "AwardPage.vue callAPI validation failed: selectedCourse or user_data is undefined"
    );
    dialogStore.setMessage("資料不完整，請重新操作");
    router.push("/alert");
    return;
  }

  try {
    const stuResult = await sendToStuAPI({
      student_id: commonStore.user_data.學號,
      scholarshipItem_id: selectedCourse.value.ssi_id,
      class_id: selectedCourse.value.class_id,
      scholarship_rank: ranking.value,
      score: score.value,
    });

    if (stuResult.code != 200) {
      websocketService.sendMessage(
        "client_error",
        `Scholarship submit failed: ${JSON.stringify(stuResult)}`
      );
      if (stuResult.data.detail == "scholarship apply already exists") {
        dialogStore.setMessage("抱歉，此獎學金已申請過!");
      } else {
        dialogStore.setMessage("申請失敗，請稍後再試");
      }
      router.push("/alert");
    } else {
      dialogStore.setMessage("申請完成!");
      router.push("/alert");
    }
  } catch (error) {
    websocketService.sendMessage(
      "client_error",
      `AwardPage.vue Exception in callAPI: ${JSON.stringify(error)}`
    );
    console.error(error);
    dialogStore.setMessage("系統錯誤，請稍後再試");
    router.push("/alert");
  }
};

const safeDate = (dateStr) => {
  try {
    return dateStr?.split(" ")[0] || "";
  } catch (err) {
    websocketService.sendMessage(
      "client_error",
      `AwardPage.vue Invalid date format: ${dateStr}`
    );
    return "";
  }
};

onMounted(async () => {
  try {
    countdown.start();
  } catch (err) {
    websocketService.sendMessage(
      "client_error",
      `AwardPage.vue onMounted error: ${JSON.stringify(err)}`
    );
  }
});

onUnmounted(() => {
  try {
    countdown.stop();
  } catch (err) {
    websocketService.sendMessage(
      "client_error",
      `AwardPage.vue onUnmounted error: ${JSON.stringify(err)}`
    );
  }
});
</script>

<template>
  <div
    class="flex flex-col items-center justify-start w-full h-full gap-4 p-4 text-2xl"
  >
    <div class="flex flex-row w-full items-center justify-between">
      <div class="flex flex-row gap-2 items-center">
        <BackButton />
        <h1 class="text-4xl font-extrabold">獎學金申請</h1>
      </div>

      <h4 class="text-base">
        已登入為 {{ commonStore.user_data.學號 }}
        {{ commonStore.user_data.姓名 }}
      </h4>
    </div>

    <Stepper value="1" class="basis-[40rem]" linear>
      <StepList>
        <Step value="1">班級</Step>
        <Step value="2">排名</Step>
        <Step value="3">分數</Step>
        <Step value="4">確認</Step>
      </StepList>
      <StepPanels>
        <StepPanel v-slot="{ activateCallback }" value="1">
          <div class="flex flex-col h-48">
            <div
              class="border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium"
            >
              <Select
                v-model="selectedCourse"
                :options="commonStore.scholarship_dates"
                optionLabel="ssd_id"
                placeholder="請選擇班級"
                class="w-full md:w-56"
                checkmark
                @focus="countdown.reset()"
              >
                <template #option="slotProps">
                  <div class="flex items-center">
                    <!-- Customize display here -->
                    <span class="font-bold text-blue-600">{{
                      slotProps.option.class_name
                    }}</span>
                    <span class="ml-2 text-green-600"
                      >$ {{ slotProps.option.money }}</span
                    >
                    <span class="ml-2">
                      {{ safeDate(slotProps.option.start_time) }} ~{{
                        safeDate(slotProps.option.end_time)
                      }}
                    </span>
                  </div>
                </template>
              </Select>
            </div>
          </div>
          <div class="flex pt-6 justify-end">
            <Button
              label="下一步"
              :disabled="selectedCourse == null"
              icon="pi pi-arrow-right"
              iconPos="right"
              @click="activateCallback('2') && countdown.reset()"
            />
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" value="2">
          <div class="flex flex-col h-fit">
            <div
              class="border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex flex-col justify-center items-center font-medium"
            >
              <InputGroup class="py-4">
                <InputText
                  :pt="{ root: { class: 'text-4xl' } }"
                  v-model="score"
                  inputId="integeronly"
                  placeholder="排名"
                  fluid
                  inputmode="none"
                  ref="inputRef"
                  variant="outlined"
                /><DeleteButton
                  class="text-center"
                  @click="score = score.slice(0, -1)"
                />
              </InputGroup>
              <Numpad
                v-model="score"
                :isLoading="isLoading"
                :minLength="6"
                buttonLabel="登入"
                @pressed="countdown.reset()"
              />
            </div>
          </div>
          <div class="flex pt-6 justify-between">
            <Button
              label="上一步"
              severity="secondary"
              icon="pi pi-arrow-left"
              @click="activateCallback('1') && countdown.reset()"
            />
            <Button
              label="下一步"
              :disabled="score == ''"
              icon="pi pi-arrow-right"
              iconPos="right"
              @click="activateCallback('3') && countdown.reset()"
            />
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" value="3">
          <div class="flex flex-col h-fit">
            <div
              class="border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-col flex justify-center items-center font-medium"
            >
              <InputGroup class="py-4">
                <InputText
                  :pt="{ root: { class: 'text-2xl' } }"
                  v-model="ranking"
                  inputId="integeronly"
                  placeholder="分數"
                  fluid
                  inputmode="none"
                  ref="inputRef"
                  variant="outlined"
                /><DeleteButton
                  class="text-center"
                  @click="ranking = ranking.slice(0, -1)"
                />
              </InputGroup>
              <Numpad
                v-model="ranking"
                :isLoading="isLoading"
                :minLength="6"
                buttonLabel="登入"
                @submit="dummySubmit"
              />
            </div>
          </div>
          <div class="flex pt-6 justify-between">
            <Button
              label="上一步"
              severity="secondary"
              icon="pi pi-arrow-left"
              @click="activateCallback('2') && countdown.reset()"
            />
            <Button
              label="下一步"
              :disabled="ranking == ''"
              icon="pi pi-arrow-right"
              iconPos="right"
              @click="activateCallback('4') && countdown.reset()"
            />
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" value="4">
          <div class="flex flex-col h-fit">
            <div
              class="border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-col flex justify-center items-center font-medium"
            >
              <div class="flex flex-col w-full gap-4">
                <p>學號: {{ commonStore.user_data.學號 }}</p>
                <p>姓名: {{ commonStore.user_data.姓名 }}</p>
                <p>
                  班級名稱:
                  {{ selectedCourse ? selectedCourse.class_name : "" }}
                </p>

                <p>分數: {{ score }}</p>

                <p>排名: {{ ranking }}</p>
              </div>
            </div>
          </div>
          <div class="flex pt-6 justify-between">
            <Button
              label="上一步"
              severity="secondary"
              icon="pi pi-arrow-left"
              @click="activateCallback('3') && countdown.reset()"
            />
            <Button
              severity="success"
              label="送出"
              icon="pi pi-check"
              @click="callAPI"
            />
          </div>
        </StepPanel>
      </StepPanels>
    </Stepper>
  </div>
</template>
<style scoped>
.p-inputtext {
  font-size: 2rem;
}
</style>
