import { reactive } from "vue";

export const alertStore = reactive({
  message: "",
  setMessage(message, secondMessage) {
    this.message = message
  },
});

