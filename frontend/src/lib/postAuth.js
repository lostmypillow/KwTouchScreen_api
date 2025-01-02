import { CapacitorHttp } from "@capacitor/core";
import { userStore } from "../store/userStore";
import { statusStore } from "../store/statusStore";
export async function postAuth(callbackRoute) {
  const options = {
    url: import.meta.env.VITE_SERVER_URL + "/auth/",
    headers: { "content-type": "application/json" },
    data: {
      student_id: userStore.student_id,
      course: statusStore.today_class,
      type: callbackRoute,
    },
  };

  const response = await CapacitorHttp.post(options);
  if (response.status != 200) {
    console.error(response)
  }
  return response;
}
