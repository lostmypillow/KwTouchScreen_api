import { useWebSocket } from './useWebSocket'

type LogLevel = 'log' | 'warn' | 'error' | 'debug' | 'info'

const getTimestamp = () => new Date().toISOString()

export function useLogger(context = 'global') {
  const { sendMessage } = useWebSocket(import.meta.env.VITE_FASTAPI_URL)

  const log = (level: LogLevel, msg: string, data?: any) => {
    const message = `[${context}] [${getTimestamp()}] ${msg}`

    // Output to console
    console[level](message, data || '')

    // Send to WebSocket (non-blocking)
    sendMessage('client_log', {
      level,
      message,
      timestamp: getTimestamp(),
      context,
      extra: data || null
    })
  }

  return {
    log: (msg: string, data?: any) => log('log', msg, data),
    warn: (msg: string, data?: any) => log('warn', msg, data),
    error: (msg: string, data?: any) => log('error', msg, data),
    debug: (msg: string, data?: any) => log('debug', msg, data),
    info: (msg: string, data?: any) => log('info', msg, data)
  }
}
