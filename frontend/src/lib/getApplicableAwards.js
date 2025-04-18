import { getJwt } from "./getJwt";
import axios from "axios";
export const getApplicableAwards = async (studentId) => {
  try {
    const jwt = await getJwt(studentId);
    if (jwt == "error") {
      throw new Error("JWT token error");
    }
    const headers = {
      Authorization: `Bearer ${jwt}`,
      Accept: "application/json",
    };

    const uuidResp = await axios.get(
      `https://stulearning.kaowei.tw/api/user?search_value=${studentId}`,
      { headers }
    );

    const userUuid = uuidResp.data.data[0].user_uuid;

    const applicableResp = await axios.get(
      `https://stulearning.kaowei.tw/api/scholarship/apply/applicable?user_uuid=${userUuid}`,
      { headers }
    );
    const appliedResp = await axios.get(
      `https://stulearning.kaowei.tw/api/scholarship/apply/applied?user_uuid=${userUuid}`,
      { headers }
    );
    console.log(`look here:`)
    console.log(appliedResp.data.data
    )

    // console.log(applicableResp.data.data);
    return applicableResp.data.data;
  } catch (error) {
    console.error(error);
    return "error"
  }
};
