import { reactive } from "vue";

export const commonStore = reactive({
  today_class_4_auth: "",
  today_class_4_display: "",
  male_seats: [],
  female_seats: [],
  user_data: {},
  is_math_rate: false,
  clear() {
    this.is_math_rate = false;
    this.user_data = {};
  },
  seats() {
    return this.user_data.性別 == "男" ? this.male_seats : this.female_seats;
  },
});
