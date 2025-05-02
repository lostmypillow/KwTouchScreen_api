import axios from "axios";

export const getJwt = async (studentId) => {
  try {
    const tokenResponse = await axios.post(
      "https://studev.kaowei.tw/api/token/get_token",
      new URLSearchParams({
        enumType: "student_id",
        value: studentId,
      }),
      {
        headers: {
          accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    const tokens = tokenResponse.data.token;
    if (!Array.isArray(tokens) || tokens.length === 0) {
      throw new Error("No tokens returned for the given student ID.");
    }

    const selectedToken = tokens[Math.floor(Math.random() * tokens.length)];

    const jwtResponse = await axios.post(
      "https://studev.kaowei.tw/api/token/request_jwt_token",
      new URLSearchParams({
        student_id: studentId,
        token: selectedToken,
      }),
      {
        headers: {
          accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    return jwtResponse.data.access_token;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const msg = error.response?.data?.message || error.message;

      console.error(`Axios error (${status}): ${msg}`);
      return `Request failed with status ${status}: ${msg}`;
    } else {
      console.error(`Unexpected error: ${error.message}`);
      return `Unexpected error: ${error.message}`;
    }
  }
};
