import api from "./api"
import { JiraTicketPayload, JiraTicketResponse } from "../types/api.types"

export const jiraService = {

  createTicket: async (payload: JiraTicketPayload): Promise<JiraTicketResponse> => {
    const response = await api.post<JiraTicketResponse>("/api/jira/ticket", payload)
    return response.data
  },
}