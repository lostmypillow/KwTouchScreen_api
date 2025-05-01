import { reactive } from "vue";
import { useRouter } from "vue-router";

export const dialogStore = reactive({
  router: useRouter(),
  visible: false,
  message: "",
  iconClass: "",
  temporary: false,
  setMessage(severity, message) {
    if (severity == "error") {
      this.iconClass = "pi pi-times";
    } else if (severity == "loading") {
      this.iconClass = "pi pi-spin pi-spinner"
    } else if (severity == 'success') {
      this.iconClass= "pi pi-check-circle"
    }
    this.message = message;
  },
  showDialog() {
    this.visible = true;
  },
  closeDialog() {
    this.message = ""
    this.iconClass = ""
    this.visible = false;
    this.temporary = false
  },
  startDelayClose() {
    
    setTimeout(() => this.closeDialog(), 3000);
  }
});
