<script setup>
import NumButton from "../components/buttons/NumButton.vue";
import Button from "primevue/button";

const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  minLength: {
    type: Number,
    default: 6, // default validation logic
  },
  buttonLabel: {
    type: String,
    default: "登入", // default text for the submit button
  },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const handleButtonClick = (number) => {
  emit("update:modelValue", props.modelValue + number);
};

const handleDelete = () => {
  emit("update:modelValue", props.modelValue.slice(0, -1));
};

const handleSubmit = () => {
  emit("submit");
};
</script>

<template>
  <div class="flex flex-wrap gap-2 justify-between w-full">
    <NumButton
      v-for="number in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
      :key="number"
      :number="number"
      class="flex-1 min-w-[30%] max-w-[32%] text-center"
      @click="handleButtonClick(number)"
    />

    <NumButton
      number="0"
      class="flex-1 w-full text-center"
      @click="handleButtonClick('0')"
    />


  </div>
</template>
