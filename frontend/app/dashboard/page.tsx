'use client'

import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/hooks/use-auth'
import { api } from '@/lib/api'
import { AlertTriangle, Droplets, FileText, TrendingUp } from 'lucide-react'

interface Analytics {
  overview: {
    total_reports: number
    reports_today: number
    total_incidents: number
    active_incidents: number
    critical_alerts: number
  }
  top_hazards: { type: string; count: number }[]
  severity_distribution: Record<string, number>
}

export default function DashboardPage() {
  const token = useAuthStore((state) => state.token)

  const { data, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => api.get<Analytics>('/analytics', token!),
    enabled: !!token,
  })

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 w-48 bg-gray-200 rounded mb-6"></div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    )
  }

  const stats = data?.overview || {
    total_reports: 0,
    reports_today: 0,
    total_incidents: 0,
    active_incidents: 0,
    critical_alerts: 0,
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard Overview</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-4">
            <div className="bg-blue-100 p-3 rounded-lg">
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Reports</p>
              <p className="text-2xl font-bold">{stats.total_reports}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-4">
            <div className="bg-green-100 p-3 rounded-lg">
              <Droplets className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Reports Today</p>
              <p className="text-2xl font-bold">{stats.reports_today}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-4">
            <div className="bg-orange-100 p-3 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Active Incidents</p>
              <p className="text-2xl font-bold">{stats.active_incidents}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-4">
            <div className="bg-red-100 p-3 rounded-lg">
              <TrendingUp className="h-6 w-6 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Critical Alerts</p>
              <p className="text-2xl font-bold">{stats.critical_alerts}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-lg font-semibold mb-4">Top Hazards</h2>
          {data?.top_hazards && data.top_hazards.length > 0 ? (
            <div className="space-y-3">
              {data.top_hazards.map((hazard) => (
                <div key={hazard.type} className="flex items-center justify-between">
                  <span className="text-gray-700">{hazard.type}</span>
                  <span className="font-medium">{hazard.count}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No hazard data available</p>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-lg font-semibold mb-4">Severity Distribution</h2>
          {data?.severity_distribution && Object.keys(data.severity_distribution).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(data.severity_distribution).map(([severity, count]) => (
                <div key={severity} className="flex items-center justify-between">
                  <span className="text-gray-700 capitalize">{severity}</span>
                  <span className="font-medium">{count}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No severity data available</p>
          )}
        </div>
      </div>
    </div>
  )
}