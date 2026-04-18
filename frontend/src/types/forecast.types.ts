export interface ForecastResult {
  predicted_value: number | null
  upper_bound: number | null
  lower_bound: number | null
  will_breach: boolean
  threshold: number
  minutes_ahead: number
  message?: string
}

export interface ForecastPoint {
  time: string
  predicted: number
  upper: number
  lower: number
}

export const SERVICES = [
  "checkout",
  "auth",
  "inventory",
  "payments",
  "notifications",
] as const

export type ServiceName = typeof SERVICES[number]