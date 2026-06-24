import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

export interface Report {
  id: string
  source: string
  status: string
  raw_text: string
  location: {
    lat?: number
    lng?: number
    name?: string
  }
  ai_analysis?: {
    hazard_type: string
    severity: string
    confidence: number
  }
  created_at: string
}

export interface ReportCreate {
  source: string
  raw_text: string
  location_lat?: number
  location_lng?: number
  location_name?: string
}

export const reportsApi = {
  list: (token: string, params?: Record<string, string>) => {
    const query = params ? `?${new URLSearchParams(params)}` : ''
    return api.get<{ data: Report[]; pagination: Record<string, number> }>(`/reports${query}`, token)
  },

  get: (id: string, token: string) =>
    api.get<Report>(`/reports/${id}`, token),

  create: (data: ReportCreate, token: string) =>
    api.post<Report>('/reports', data, token),
}

export function useReports(token: string, params?: Record<string, string>) {
  return useQuery({
    queryKey: ['reports', params],
    queryFn: () => reportsApi.list(token, params),
  })
}

export function useReport(id: string, token: string) {
  return useQuery({
    queryKey: ['report', id],
    queryFn: () => reportsApi.get(id, token),
    enabled: !!id,
  })
}

export function useCreateReport() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ data, token }: { data: ReportCreate; token: string }) =>
      reportsApi.create(data, token),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports'] })
    },
  })
}