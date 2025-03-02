import { reactive } from "vue";

export const statusStore = reactive({
  current_list: [],
  today_class: {},
  withSeatList: [],
  setTodayClass(today_data) {
    this.today_class = today_data;
  },
  setList(current_list) {
    this.current_list = current_list;
  },
  setWithSeatList(current_list) {
    this.withSeatList = current_list;
  },
  returnSeats(gender) {
    return gender == "male" ? this.today_class.male_seats : this.today_class.female_seats;
  },
});
