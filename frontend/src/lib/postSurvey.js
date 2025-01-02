import { CapacitorHttp } from "@capacitor/core";
import { userStore } from "../store/userStore";
import { surveyStore } from "../store/surveyStore";
export async function postSurvey(selectedSeat) {
  const options = {
    url: import.meta.env.VITE_SERVER_URL + "/survey/",
    headers: { "content-type": "application/json" },
    data: {
      employee_id: surveyStore.selectedEmployee.id,
      student_id: userStore.student_id,
      rating: surveyStore.rating,
    },
  };
  const response = CapacitorHttp.post(options);
  if ((await response).status != 200) {
    console.error(response)
  }
  return response;
}
