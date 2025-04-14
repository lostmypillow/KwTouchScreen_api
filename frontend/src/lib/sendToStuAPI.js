import axios from "axios";

export async function sendToStuAPI(urlFragment, data) {
  console.log(`[sendToStuAPI.js] [${new Date().toISOString()}] Function called with urlFragment: ${urlFragment}, data: ${JSON.stringify(data)}`);

  let errorData = {};

  try {
    console.log(`[sendToStuAPI.js] [${new Date().toISOString()}] Attempting to send POST request to server...`);
    
    const res = await axios.post(
      "http://" + import.meta.env.VITE_SERVER_URL + urlFragment,
      data,
      {
        headers: { "Content-Type": "application/json" },
      }
    );
    
    console.log(`[sendToStuAPI.js] [${new Date().toISOString()}] Response received from server: ${JSON.stringify(res.data)}`);
    
    return {
      code: 200,
      data: res.data,
    };
  } catch (error) {
    console.error(`[sendToStuAPI.js] [${new Date().toISOString()}] Error encountered during API request:`);
    console.error(error)
    
    if (error.response) {
      console.log(`[sendToStuAPI.js] [${new Date().toISOString()}] Server responded with status: ${error.response.status}, data: ${JSON.stringify(error.response.data)}`);
      return {
        code: error.response.status,
        data: error.response.data,
      };
    } else if (error.request) {
      // The request was made but no response was received
      console.log(`[sendToStuAPI.js] [${new Date().toISOString()}] No response received, error.request: ${JSON.stringify(error.request)}`);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log(`[sendToStuAPI.js] [${new Date().toISOString()}] Error during setup: ${error.message}`);
    }
  }
}
