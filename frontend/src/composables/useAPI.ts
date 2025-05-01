import axios from 'axios'
import { useLogger } from './useLogger'
const logger = useLogger()
export function useAPI() {
  const sendToAPI = async (urlFragment: string, data: any) => {
    const apiUrl = `http://${import.meta.env.VITE_FASTAPI_URL}/${urlFragment}`

    try {
      const res = await axios.post(apiUrl, data, {
        headers: { 'Content-Type': 'application/json' },
      })

      return res
    } catch (error: any) {
      if (error.response) {
        logger.error(
          `Response error.\nData: ${JSON.stringify(data)}\nResponse $ ${error.response.status}: ${JSON.stringify(
            error.response.data
          )}`
        )

        return {
          code: error.response.status,
          data: error.response.data,
        }
      } else if (error.request) {
        logger.error(
          `No response received. Request: ${JSON.stringify(error.request)}`
        )
      } else {
        logger.error(
          `Axios setup error: ${error.message}`
        )
      }

      return {
        code: 500,
        data: {
          detail: '系統錯誤，請稍後再試',
        },
      }
    }
  }

  const sendToStuAPI = sendToAPI // alias for student version if needed

  return { sendToAPI, sendToStuAPI }
}