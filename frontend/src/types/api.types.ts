export interface ApiError {
  detail: string
  status: number
}

export interface JiraTicketPayload {
  summary: string
  description: string
  severity: string
}

export interface JiraTicketResponse {
  ticket_key: string
  url: string
}