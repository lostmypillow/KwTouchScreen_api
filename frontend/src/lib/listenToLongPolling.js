import { CapacitorHttp } from "@capacitor/core";
import { statusStore } from "../store/statusStore";
export function listenToLongPolling() {
  function poll(type) {
    CapacitorHttp.get({
      url: import.meta.env.VITE_SERVER_URL + "/eventpoll/" + type,
    })
      .then((response) => response.data)
      .then((data) => {
        console.log(data);
        if (data.type === "remaining") {
          statusStore.setTodayClass(data.data);
          type = 1;
        } else {
          statusStore.setList(data.data);
          console.log("i ran");
          type = 0;
        }

        setTimeout(() => {
          poll(type);
        }, 5000);
      })
      .catch((error) => {
        console.error("Error occurred during long-polling:", error);
        setTimeout(poll, 10000); 
      });
  }
  poll(0);
}
