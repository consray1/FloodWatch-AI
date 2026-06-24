'use client'

import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/hooks/use-auth'
import { api } from '@/lib/api'
import { MapPin, Plus, Filter } from 'lucide-react'
import Link from 'next/link'

interface Incident {
  id: string
  title: string
  hazard_type: string
  severity: string
  status: string
  location: { lat: number; lng: number; name?: string }
  reporter_count: number
  risk_score?: number
  created_at: string
}

interface IncidentList {
  data: Incident[]
  pagination: Record<string, number>
}

export default function IncidentsPage() {
  const token = useAuthStore((state) => state.token)

  const { data, isLoading } = useQuery({
    queryKey: ['incidents'],
    queryFn: () => api.get<IncidentList>('/incidents', token!),
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
      case 'active':
        return 'bg-blue-100 text-blue-800'
      case 'contained':
        return 'bg-yellow-100 text-yellow-800'
      case 'resolved':
        return 'bg-green-100 text-green-800'
      case 'closed':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Incidents</h1>
        <Link
          href="/dashboard/incidents/new"
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          <Plus className="h-4 w-4" />
          Create Incident
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>
          <select className="border border-gray-300 rounded-md px-3 py-1.5 text-sm">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="contained">Contained</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
          <select className="border border-gray-300 rounded-md px-3 py-1.5 text-sm">
            <option value="">All Severity</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      ) : data?.data && data.data.length > 0 ? (
        <div className="space-y-4">
          {data.data.map((incident) => (
            <Link
              key={incident.id}
              href={`/dashboard/incidents/${incident.id}`}
              className="block bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {incident.title}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(incident.severity)}`}>
                      {incident.severity}
                    </span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(incident.status)}`}>
                      {incident.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    {incident.hazard_type} • {incident.reporter_count} reports
                  </p>
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    {incident.location?.name && (
                      <span className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {incident.location.name}
                      </span>
                    )}
                    <span>
                      {new Date(incident.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                {incident.risk_score !== undefined && incident.risk_score !== null && (
                  <div className="text-right">
                    <span className="text-sm font-medium text-gray-900">Risk Score</span>
                    <p className="text-2xl font-bold text-blue-600">
                      {incident.risk_score.toFixed(1)}
                    </p>
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <p className="text-gray-500">No incidents found</p>
        </div>
      )}
    </div>
  )
}