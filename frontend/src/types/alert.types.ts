export type Severity = "low" | "medium" | "high" | "critical"

export interface Metrics {
  cpu: number
  memory: number
  error_rate: number
  latency_p99: number
}

export interface Alert {
  id?: string
  service: string
  severity: Severity
  anomaly_score: number
  metrics: Metrics
  explanation: string
  timestamp?: string
}

export interface AlertsResponse {
  alerts: Alert[]
  count: number
}

export interface IngestPayload {
  service: string
  cpu: number
  memory: number
  error_rate: number
  latency_p99: number
  log_snippet?: string
}

export interface IngestResponse {
  received: boolean
  service: string
  anomaly_detected: boolean
  anomaly_score: number
  severity: Severity | "none"
  message: string
}