'use client'

import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/hooks/use-auth'
import { api } from '@/lib/api'
import { BarChart3, TrendingUp } from 'lucide-react'

interface Analytics {
  overview: {
    total_reports: number
    reports_today: number
    total_incidents: number
    active_incidents: number
    critical_alerts: number
  }
  trends: {
    reports_last_7_days: number[]
  }
  top_hazards: { type: string; count: number }[]
  severity_distribution: Record<string, number>
}

export default function AnalyticsPage() {
  const token = useAuthStore((state) => state.token)

  const { data, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => api.get<Analytics>('/analytics', token!),
    enabled: !!token,
  })

  const totalReports = data?.overview?.total_reports || 0
  const reportsToday = data?.overview?.reports_today || 0
  const activeIncidents = data?.overview?.active_incidents || 0
  const criticalAlerts = data?.overview?.critical_alerts || 0

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-3 rounded-lg">
              <BarChart3 className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Reports</p>
              <p className="text-2xl font-bold">{totalReports}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-3">
            <div className="bg-green-100 p-3 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Reports Today</p>
              <p className="text-2xl font-bold">{reportsToday}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-3">
            <div className="bg-orange-100 p-3 rounded-lg">
              <BarChart3 className="h-6 w-6 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Active Incidents</p>
              <p className="text-2xl font-bold">{activeIncidents}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center gap-3">
            <div className="bg-red-100 p-3 rounded-lg">
              <TrendingUp className="h-6 w-6 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Critical Alerts</p>
              <p className="text-2xl font-bold">{criticalAlerts}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-lg font-semibold mb-4">7-Day Trend</h2>
          {data?.trends?.reports_last_7_days && data.trends.reports_last_7_days.length > 0 ? (
            <div className="flex items-end justify-between h-48 gap-2">
              {data.trends.reports_last_7_days.map((count, i) => (
                <div key={i} className="flex flex-col items-center flex-1">
                  <div
                    className="w-full bg-blue-600 rounded-t"
                    style={{ height: `${(count / Math.max(...data.trends.reports_last_7_days)) * 100}%` }}
                  ></div>
                  <span className="text-xs text-gray-500 mt-2">
                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No trend data available</p>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h2 className="text-lg font-semibold mb-4">Severity Breakdown</h2>
          {data?.severity_distribution && Object.keys(data.severity_distribution).length > 0 ? (
            <div className="space-y-4">
              {Object.entries(data.severity_distribution).map(([severity, count]) => (
                <div key={severity}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700 capitalize">{severity}</span>
                    <span className="text-sm text-gray-500">{count}</span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        severity === 'critical' ? 'bg-red-500' :
                        severity === 'high' ? 'bg-orange-500' :
                        severity === 'medium' ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${(count / Object.values(data.severity_distribution).reduce((a, b) => a + b, 0)) * 100}%` }}
                    ></div>
                  </div>
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