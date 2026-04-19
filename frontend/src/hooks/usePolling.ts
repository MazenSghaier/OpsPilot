import { useEffect, useRef, useCallback } from "react"

export function usePolling(
  fn: () => Promise<void>,
  intervalMs: number,
  enabled = true
) {
  const intervalRef = useRef<NodeJS.Timeout | null>(null)
  
  const fnRef = useRef(fn)
  useEffect(() => {
    fnRef.current = fn
  }, [fn])

  const stop = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }, [])

  const start = useCallback(() => {
    stop()
    fnRef.current()
    intervalRef.current = setInterval(() => {
      fnRef.current()
    }, intervalMs)
  }, [intervalMs, stop])

  useEffect(() => {
    if (!enabled) {
      stop()
      return
    }
    start()
    return stop
  }, [enabled, start, stop])
}