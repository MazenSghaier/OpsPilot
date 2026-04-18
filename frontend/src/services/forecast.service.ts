import api from "./api"
import { ForecastResult } from "../types/forecast.types"

export const forecastService = {

  getForecast: async (service: string): Promise<ForecastResult> => {
    const response = await api.get<ForecastResult>(`/api/predict/${service}`)
    return response.data
  },
}