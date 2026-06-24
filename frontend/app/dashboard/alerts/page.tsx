'use client'

import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/hooks/use-auth'
import { api } from '@/lib/api'
import { Bell, Filter, Send } from 'lucide-react'

interface Alert {
  id: string
  title: string
  severity: string
  channel: string
  status: string
  incident_id?: string
  sent_at?: string
  created_at: string
}

interface AlertList {
  data: Alert[]
  pagination: Record<string, number>
}

export default function AlertsPage() {
  const token = useAuthStore((state) => state.token)

  const { data, isLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => api.get<AlertList>('/alerts', token!),
    enabled: !!token,
  })

  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800'
      case 'high':
        return 'bg-orange-100 text-orange-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'sent':
        return 'bg-green-100 text-green-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getChannelIcon = (channel?: string) => {
    return <Bell className="h-4 w-4" />
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Alerts</h1>
        <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
          <Send className="h-4 w-4" />
          Create Alert
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>
          <select className="border border-gray-300 rounded-md px-3 py-1.5 text-sm">
            <option value="">All Status</option>
            <option value="sent">Sent</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
          <select className="border border-gray-300 rounded-md px-3 py-1.5 text-sm">
            <option value="">All Channels</option>
            <option value="sms">SMS</option>
            <option value="email">Email</option>
            <option value="whatsapp">WhatsApp</option>
            <option value="push">Push</option>
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-24 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      ) : data?.data && data.data.length > 0 ? (
        <div className="space-y-4">
          {data.data.map((alert) => (
            <div key={alert.id} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-gray-400">{getChannelIcon(alert.channel)}</span>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {alert.title}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(alert.severity)}`}>
                      {alert.severity}
                    </span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(alert.status)}`}>
                      {alert.status}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    <span className="uppercase">{alert.channel}</span>
                    <span>{new Date(alert.created_at).toLocaleDateString()}</span>
                    {alert.sent_at && (
                      <span>Sent: {new Date(alert.sent_at).toLocaleString()}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <p className="text-gray-500">No alerts found</p>
        </div>
      )}
    </div>
  )
}