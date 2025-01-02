import { CapacitorHttp } from "@capacitor/core";
export async function getQueueLength(params) {
  const response = await CapacitorHttp.get({
    url: import.meta.env.VITE_SERVER_URL + "/video/queue",
  });
  if (response.status != 200) {
    console.error(response)
  }
  return response.data.length;
}
