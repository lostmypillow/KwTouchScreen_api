import { getJwt } from "./getJwt";
const getApplicableAwards = async (student_id) => {
  const jwt = await getJwt(studentId);

  const headers = {
    Authorization: `Bearer ${jwt}`,
    Accept: "application/json",
  };

  const uuidResp = await axios.get(
    `https://studev.kaowei.tw/api/user?search_value=${studentId}`,
    { headers }
  );

  const userUuid = uuidResp.data.data[0].user_uuid;

  const applicableResp = await axios.get(
    `https://studev.kaowei.tw/api/scholarship/apply/applicable?user_uuid=${userUuid}`,
    { headers }
  );

  console.log(applicableResp.data);
};
