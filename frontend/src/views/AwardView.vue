<script setup>
import { onMounted, ref, watch } from "vue";
import Numpad from "../components/Numpad.vue";
import { useRouter } from "vue-router";
import { store } from "../store";
import { useLogger } from "../composables/useLogger";
import { useCountdown } from "../composables/useCountdown";
import { useAPI } from "../composables/useAPI";
const router = useRouter();
const logger = useLogger();
const api = useAPI();
const selectedSSDObj = ref({});
const selectedSSIObj = ref({});
const selectedClassObj = ref({});
const score = ref("");
const ranking = ref("");
const isLoading = ref(false);
const { start, reset, stop } = useCountdown(50, () => {
  store.clearUserData();
  router.push("/");
});
const dummySubmit = () => console.log(score.value);

const callAPI = async () => {
  store.setupDialog("loading", "處理中，請稍候...");
  store.showDialog();
  try {
    const stuResult = await api.sendData(
      "https://stulearning.kaowei.tw/api/scholarship/apply/",
      await api.jwtHeaders(store.userData.學號),
      {
        student_id: store.userData.學號,
        scholarshipItem_id: selectedSSIObj.value.ssi_id,
        class_id: selectedClassObj.value.class_id,
        scholarship_rank: ranking.value,
        score: score.value,
      }
    );

    if (stuResult.success == false) {
      logger.error(`Scholarship submit failed: ${JSON.stringify(stuResult)}`);
      store.setupDialog(
        "error",
        stuResult.data.detail == "scholarship apply already exists"
          ? "申請失敗，此獎學金已申請過!"
          : "申請失敗，請洽導師!"
      );
      setTimeout(() => {
        store.closeDialog();
        store.clearUserData();
        router.push("/");
      }, 3000);
      return;
    } else {
      store.setupDialog("success", "已送出資料，請至App上傳佐證資料!");
      setTimeout(() => {
        store.closeDialog();
        store.clearUserData();
        router.push("/");
      }, 3000);
    }
  } catch (error) {
    logger.error(
      `AwardView.vue Exception in callAPI: ${JSON.stringify(error)}`
    );
    store.setupDialog("error", "系統錯誤，請洽導師!");
    setTimeout(() => {
      store.closeDialog();
      store.clearUserData();
      router.push("/");
    }, 3000);
    return;
  }
};
watch(selectedSSDObj, () => {
  selectedSSIObj.value = {};
  selectedClassObj.value = {};
});

// Clear class when SSI changes
watch(selectedSSIObj, () => {
  selectedClassObj.value = {};
});
onMounted(() => start());
</script>

<template>
  <Stepper value="1" class="basis-[40rem]" linear>
    <StepList>
      <Step value="1">選擇</Step>
      <Step value="2">排名</Step>
      <Step value="3">分數</Step>
      <Step value="4">確認</Step>
    </StepList>
    <StepPanels>
      <StepPanel v-slot="{ activateCallback }" value="1">
        <div class="flex flex-col h-fit">
          <div
            class="border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex flex-col justify-center w-[40rem] items-center font-medium gap-4"
          >
            <Select
              v-model="selectedSSDObj"
              :options="store.scholarshipDates"
              optionLabel="name"
              placeholder="請選擇"
              class="w-full text-2xl"
              checkmark
              @focus="reset"
            >
              <!-- Dropdown Option -->
              <template #option="slotProps">
                <span class="text-2xl">
                  {{ slotProps.option.year }}學年 第{{
                    slotProps.option.semester
                  }}學期 第{{ slotProps.option.times }}次
                </span>
              </template>

              <!-- Selected Value Display -->
              <template #value="slotProps">
                <span v-if="slotProps.value" class="text-2xl">
                  {{ slotProps.value.year }}學年 第{{
                    slotProps.value.semester
                  }}學期 第{{ slotProps.value.times }}次
                </span>
                <span v-else class="text-gray-400">請選擇學年</span>
              </template>
            </Select>

            <Select
              v-if="selectedSSDObj.scholarship_items"
              v-model="selectedSSIObj"
              :options="selectedSSDObj.scholarship_items"
              placeholder="請選擇獎項"
              class="w-full text-2xl"
              @focus="reset"
              checkmark
            >
              {{ selectedSSIObj }}
              <template #option="slotProps">
                <span class="text-2xl"
                  >{{ slotProps.option.name }} -
                  <span class="font-bold text-green-700"
                    >${{ slotProps.option.money }}</span
                  ></span
                >
              </template>
              <template #value="slotProps">
                <span class="text-2xl" v-if="slotProps.value">
                  {{ slotProps.value.name }} -
                  <span class="font-bold text-green-700"
                    >${{ slotProps.value.money }}</span
                  ></span
                ><span v-else class="text-gray-400">請選擇獎項</span>
              </template>
            </Select>

            <Select
              v-if="selectedSSIObj.classes"
              v-model="selectedClassObj"
              :options="selectedSSIObj.classes"
              optionLabel="class_name"
              placeholder="請選擇班級"
              class="w-full text-2xl"
              @focus="reset"
              checkmark
            >
              <template #option="slotProps">
                <span class="text-2xl">{{
                  slotProps.option.class_name
                }}</span></template
              >
            </Select>
          </div>
        </div>
        <div class="flex pt-6 justify-end">
          <Button
            label="下一步"
            :disabled="Object.keys(selectedClassObj) == 0"
            icon="pi pi-arrow-right"
            iconPos="right"
            @click="activateCallback('2') && reset()"
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
                placeholder="請輸入排名"
                fluid
                inputmode="none"
                ref="inputRef"
                variant="outlined"
              /><DeleteButton
                class="text-center"
                @click="score = score.slice(0, -1) && reset()"
              />
            </InputGroup>
            <Numpad
              v-model="score"
              :isLoading="isLoading"
              :minLength="6"
              buttonLabel="登入"
              @pressed="reset()"
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
                placeholder="請輸入分數"
                fluid
                inputmode="none"
                ref="inputRef"
                variant="outlined"
              /><DeleteButton
                class="text-center"
                @click="ranking = ranking.slice(0, -1) && reset()"
              />
            </InputGroup>
            <Numpad
              v-model="ranking"
              :isLoading="isLoading"
              :minLength="6"
              @pressed="reset()"
            />
          </div>
        </div>
        <div class="flex pt-6 justify-between">
          <Button
            label="上一步"
            severity="secondary"
            icon="pi pi-arrow-left"
            @click="activateCallback('2') && reset()"
          />
          <Button
            label="下一步"
            :disabled="ranking == ''"
            icon="pi pi-arrow-right"
            iconPos="right"
            @click="activateCallback('4') && reset()"
          />
        </div>
      </StepPanel>
      <StepPanel v-slot="{ activateCallback }" value="4">
        <div class="flex flex-col h-fit">
          <div
            class="border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-col flex justify-center items-center font-medium"
          >
            <div class="flex flex-col w-full gap-4 text-2xl">
              <p>學號: {{ store.userData.學號 }}</p>
              <p>姓名: {{ store.userData.姓名 }}</p>
              <p>
                獎學金學年: {{ selectedSSDObj.year }}學年 第{{
                  selectedSSDObj.semester
                }}學期 第{{ selectedSSDObj.times }}次
              </p>
              <p>獎學金名稱: {{ selectedSSIObj.name }}</p>

              <p>
                獎學金班級:
                {{ selectedClassObj.class_name }}
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
            @click="activateCallback('3') && reset()"
          />
          <Button
            severity="success"
            label="提交申請"
            icon="pi pi-check"
            @click="callAPI"
          />
        </div>
      </StepPanel>
    </StepPanels>
  </Stepper>
</template>
<style scoped>
.p-inputtext {
  font-size: 2rem;
}
</style>
