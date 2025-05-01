<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  text: {
    type: String,
    default: ''
  },
  iconClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

// Computed wrapper for v-model:visible
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>

<template>
  <Dialog
    v-model:visible="visible"
    modal
    :closable="false"
    :contentStyle="{ minWidth: '200px' }"
    :showHeader="false"
  >
    <template #closebutton>
      <!-- Removes the close button -->
    </template>
    <div
      class="flex flex-row gap-4 w-full items-center justify-start h-fit pt-6"
    >
      <i :class="iconClass" style="font-size: 2rem"></i>
      <p class="text-2xl">{{ text }}</p>
    </div>
  </Dialog>
</template>