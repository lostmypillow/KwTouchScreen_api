import { reactive } from "vue";

export const alertStore = reactive({
  message: "",
  setMessage(message) {
    this.message = message
  },
});

