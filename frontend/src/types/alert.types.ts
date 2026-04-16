export type Severity = "low" | "medium" | "high" | "critical"

export interface Metrics {
  cpu: number
  memory: number
  error_rate: number
  latency_p99: number
}
