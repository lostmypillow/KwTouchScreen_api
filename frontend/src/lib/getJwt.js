export const getJwt = async (studentId) => {
    const headers = {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    };
  
    const tokenResp = await axios.post(
      'https://studev.kaowei.tw/api/token/get_token',
      new URLSearchParams({
        enumType: 'student_id',
        value: studentId
      }),
      { headers }
    );
  
    const tokens = tokenResp.data.token;
    const token = tokens[Math.floor(Math.random() * tokens.length)];
  
    const jwtResp = await axios.post(
      'https://studev.kaowei.tw/api/token/request_jwt_token',
      new URLSearchParams({
        student_id: studentId,
        token: token
      }),
      { headers }
    );
  
    return jwtResp.data.access_token;
  };