import { CapacitorHttp } from "@capacitor/core";
import { userStore } from "../store/userStore";
import { statusStore } from "../store/statusStore";
export async function postSeats(selectedSeat) {
   
    const options = {
        url: import.meta.env.VITE_SERVER_URL + "/seats/",
        headers: { "content-type": "application/json" },
        data: {
          student_id: userStore.student_id.toString(),
          sn: selectedSeat,
        },
      }
      const response = CapacitorHttp.post(options)
      if ((await response).status != 200) {
        console.error(response)
      }
      return response

}
