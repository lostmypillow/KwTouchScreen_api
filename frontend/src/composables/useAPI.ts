import axios from "axios";
import { useLogger } from "./useLogger";

const logger = useLogger();

export function useAPI() {
  const BASE_URL = "https://stulearning.kaowei.tw/api";
  const defaultHeaders = {
    accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  };
  const jwtHeaders = async (studentId: string) => ({
    Authorization: `Bearer ${(await getJwt(studentId)).data}`,
    Accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  });

  const handleAxiosError = (error: any, context: string) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status ?? "N/A";
      const message = error.response?.data?.message || error.message;
      logger.error(`${context} - Axios error (${status}): ${message}`);
      return {
        success: false,
        error: `Error ${status}: ${message}`,
        data: null,
      };
    } else {
      logger.error(`${context} - Unknown error: ${error.message}`);
      return {
        success: false,
        error: `Unknown error: ${error.message}`,
        data: null,
      };
    }
  };

  const sendData = async (
    url: string,
    headers: Record<string, string>,
    data: any
  ) => {
    try {
      const response = await axios.post(url, data, { headers });
      return {
        success: true,
        error: null,
        data: response.data,
      };
    } catch (error) {
      const errorData = error.response?.data;
      const errorMsg =
        error.response?.data?.message || error.message || "Unknown error";

      return {
        success: false,
        error: `POST ${url} failed: ${errorMsg}`,
        data: errorData,
      };
    }
  };

  const getJwt = async (studentId: string) => {

    const tokenData = new URLSearchParams({
      enumType: "student_id",
      value: studentId,
    });

    const tokenRes = await sendData(`${BASE_URL}/token/get_token`, defaultHeaders, tokenData);
    if (!tokenRes.success || !Array.isArray(tokenRes.data?.token)) {
      return {
        success: false,
        error: "Token retrieval failed",
        data: null,
      };
    }

    const tokens = tokenRes.data.token;
    const selectedToken = tokens[Math.floor(Math.random() * tokens.length)];


    const jwtRes = await sendData(`${BASE_URL}/token/request_jwt_token`, defaultHeaders, new URLSearchParams({
      student_id: studentId,
      app_token: selectedToken,
    }));
    if (jwtRes.success) {
      return {
        success: true,
        error: null,
        data: jwtRes.data.access_token,
      };
    } else {
      return {
        success: false,
        error: "JWT generation failed",
        data: null,
      };
    }
  };

  const getApplicableAwards = async (studentId: string) => {
    const jwtResult = await getJwt(studentId);
    if (!jwtResult.success) return jwtResult;

    const authHeaders = {
      Authorization: `Bearer ${jwtResult.data}`,
      Accept: "application/json",
    };

    try {
      const uuidResp = await axios.get(
        `${BASE_URL}/user`,
        { headers: authHeaders }
      );
      const userUuid = uuidResp.data.data?.[0]?.user_uuid;
      if (!userUuid) throw new Error("User UUID not found");

      const applicableResp = await axios.get(
        `${BASE_URL}/scholarship/apply/applicable?user_uuid=${userUuid}`,
        { headers: authHeaders }
      );

      logger.info("Applicable scholarships:", applicableResp.data.data);

      return {
        success: true,
        error: null,
        data: applicableResp.data.data.scholarship_dates,
      };
    } catch (error) {
      return handleAxiosError(error, "Fetching awards");
    }
  };

  return {
    jwtHeaders,
    defaultHeaders,
    sendData,
    getJwt,
    getApplicableAwards,
  };
}
