import axios from "axios";
export async function useAwards(studentId: string) {
  try {
    const jwtHeaders = {
      accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
    };

    const tokenResp = await axios.post(
      "https://studev.kaowei.tw/api/token/get_token",
      new URLSearchParams({
        enumType: "student_id",
        value: studentId,
      }),
      { headers: jwtHeaders }
    );

    const tokens: string[] = tokenResp.data.token;
    const token = tokens[Math.floor(Math.random() * tokens.length)];

    const jwtResp = await axios.post(
      "https://studev.kaowei.tw/api/token/request_jwt_token",
      new URLSearchParams({
        student_id: studentId,
        token,
      }),
      { headers: jwtHeaders }
    );
    const jwt = jwtResp.data.access_token;
    if (jwt === "error") throw new Error("JWT token error");

    const applicableHeaders = {
      Authorization: `Bearer ${jwt}`,
      Accept: "application/json",
    };

    const applicableResp = await axios.get(
      `https://studev.kaowei.tw/api/scholarship/apply/applicable?user_uuid=${
        (
          await axios.get(
            `https://studev.kaowei.tw/api/user?search_value=${studentId}`,
            { headers: applicableHeaders }
          )
        ).data.data[0].user_uuid
      }`,
      { headers: applicableHeaders }
    );

    const appliedResp = await axios.get(
      `https://studev.kaowei.tw/api/scholarship/apply/applied?user_uuid=${userUuid}`,
      { headers: applicableHeaders }
    );

    // console.log('look here:')
    // console.log(appliedResp.data.data)
    // console.log(applicableResp.data.data)

    return applicableResp.data.data;
  } catch (error) {
    console.error(error);
    return "error";
  }
}
