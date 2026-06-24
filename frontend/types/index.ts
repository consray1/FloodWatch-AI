export type AlertSeverity = 'low' | 'medium' | 'high' | 'critical'
export type ReportSource = 'web' | 'sms' | 'whatsapp' | 'voice' | 'icpac'
export type IncidentStatus = 'active' | 'contained' | 'resolved' | 'closed'

export interface Location {
  lat: number
  lng: number
  name?: string
}

export interface Pagination {
  page: number
  limit: number
  total: number
  total_pages: number
}