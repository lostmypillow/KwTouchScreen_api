import { ref, onUnmounted } from 'vue'

export function useCountdown(initialTime = 30, onFinish?: () => void) {
  const timeLeft = ref(initialTime)
  const running = ref(false)
  let interval: ReturnType<typeof setInterval>

  const start = () => {
    running.value = true
    interval = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--
      } else {
        stop()
        onFinish?.()
      }
    }, 1000)
  }

  const stop = () => {
    running.value = false
    clearInterval(interval)
  }

  const reset = () => {
    stop()
    timeLeft.value = initialTime
    start()
  }

  onUnmounted(stop)

  return { timeLeft, start, stop, reset, running }
}
