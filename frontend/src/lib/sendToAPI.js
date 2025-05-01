import axios from "axios";
import websocketService from "./websocketService";

export async function sendToAPI(urlFragment, data) {
  const apiUrl = "http://" + import.meta.env.VITE_FASTAPI_URL + urlFragment;

  try {
    const res = await axios.post(apiUrl, data, {
      headers: { "Content-Type": "application/json" },
    });

    return {
      code: 200,
      data: res.data,
    };
  } catch (error) {
    if (error.response) {
      // Server responded with an error status
      websocketService.sendMessage(
        "client_error",
        `Response error.\nData: ${JSON.stringify(data)}\nResponse $ ${error.response.status}: ${JSON.stringify(
          error.response.data
        )}`
      );

    

      return {
        code: error.response.status,
        data: error.response.data,
      };
    } else if (error.request) {
      // Request sent but no response received
      websocketService.sendMessage(
        "client_error",
        `No response received. Request: ${JSON.stringify(error.request)}`
      );
    } else {
      // Setup or config error
      websocketService.sendMessage(
        "client_error",
        `Axios setup error: ${error.message}`
      );
    }

    return {
      code: 500,
      data: {
        detail: "系統錯誤，請稍後再試",
      },
    };
  }
}
