import { reactive } from "vue";

export const userStore = reactive({
  student_id: "",
  auth_seat: false,
  name: "",
  gender: "",
  rateable_employees: [],
  importData(incoming_data) {
    this.student_id = incoming_data.student_id;
    this.auth_seat = incoming_data.auth_seat
    this.name = incoming_data['name'];
    this.gender = incoming_data['gender'];
    this.rateable_employees = incoming_data.rateable_employees
  },
  clear() {
    this.student_id = "";
    this.auth_seat = false
    this.name = "";
    this.gender = "";
    this.rateable_employees = []
  },
});
