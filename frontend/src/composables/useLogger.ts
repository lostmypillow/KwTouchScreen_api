import { useWebSocket } from './useWebSocket'

type LogLevel = 'log' | 'warn' | 'error' | 'debug' | 'info'


export function useLogger() {
  const { sendMessage } = useWebSocket()

  const log = (level: LogLevel, msg: string, data?: any) => {
    // Output to console
    console[level](msg, data || '')

    // Send to WebSocket (non-blocking)
    sendMessage('client_log', `[${level}] ${msg}`)
  }

  return {
    log: (msg: string, data?: any) => log('log', msg, data),
    warn: (msg: string, data?: any) => log('warn', msg, data),
    error: (msg: string, data?: any) => log('error', msg, data),
    debug: (msg: string, data?: any) => log('debug', msg, data),
    info: (msg: string, data?: any) => log('info', msg, data)
  }
}
