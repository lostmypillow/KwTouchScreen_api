import { useWebSocket } from './useWebSocket'

type LogLevel = 'log' | 'warn' | 'error' | 'debug' | 'info'

const getTimestamp = () => new Date().toISOString()

export function useLogger(context = 'global') {
  const { sendMessage } = useWebSocket()

  const log = (level: LogLevel, msg: string, data?: any) => {
    const timestamp = getTimestamp()
    const message = `[${context}] [${timestamp}] ${msg}`

    // Output to console
    console[level](message, data || '')

    // Send to WebSocket (non-blocking)
    sendMessage('client_log', {
      level,
      message,
      timestamp: timestamp,
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
