import api from "./api"

export const reportService = {

  downloadLatest: async (): Promise<void> => {
    const response = await api.get("/api/reports/latest", {
      responseType: "blob",
    })

    const url  = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement("a")
    link.href  = url
    link.setAttribute(
      "download",
      `opspilot_report_${new Date().toISOString().slice(0, 10)}.pdf`
    )
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  },
}