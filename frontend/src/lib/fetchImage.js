export const fetchImage = async (employee_id) => {
  const serverUrl = import.meta.env.VITE_SERVER_URL + "/picture/employee/" + employee_id;

  // Use a promise to handle the async behavior
  try {
    const response = await fetch(serverUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const blob = await response.blob();
    const blobUrl = URL.createObjectURL(blob);
    console.log("Blob URL:", blobUrl);
    return blobUrl;
  } catch (error) {
    console.error("Error fetching image:", error);
    throw error; // Re-throw the error for further handling
  }
}
