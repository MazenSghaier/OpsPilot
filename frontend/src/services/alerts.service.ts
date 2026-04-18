import api from "./api"
import { Alert, AlertsResponse, IngestPayload, IngestResponse } from "../types/alert.types"

export const alertsService = {

  getAlerts: async (limit = 20): Promise<Alert[]> => {
    const response = await api.get<AlertsResponse>("/api/alerts", {
      params: { limit },
    })
    return response.data.alerts
  },

  ingest: async (payload: IngestPayload): Promise<IngestResponse> => {
    const response = await api.post<IngestResponse>("/api/ingest", payload)
    return response.data
  },
}