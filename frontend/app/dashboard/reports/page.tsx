'use client'

import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { useAuthStore } from '@/hooks/use-auth'
import { useReports } from '@/hooks/use-reports'
import { Plus, MapPin, Filter } from 'lucide-react'

export default function ReportsPage() {
  const token = useAuthStore((state) => state.token)
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [sourceFilter, setSourceFilter] = useState<string>('')

  const { data, isLoading } = useReports(token!, {
    ...(statusFilter && { status: statusFilter }),
    ...(sourceFilter && { source: sourceFilter }),
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

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
        <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
          <Plus className="h-4 w-4" />
          New Report
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-1.5 text-sm"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="analyzed">Analyzed</option>
            <option value="verified">Verified</option>
            <option value="dismissed">Dismissed</option>
          </select>
          <select
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-1.5 text-sm"
          >
            <option value="">All Sources</option>
            <option value="web">Web</option>
            <option value="sms">SMS</option>
            <option value="whatsapp">WhatsApp</option>
            <option value="voice">Voice</option>
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
          {data.data.map((report) => (
            <div key={report.id} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-sm font-medium text-blue-600 uppercase">
                      {report.source}
                    </span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(report.ai_analysis?.severity)}`}>
                      {report.ai_analysis?.severity || report.status}
                    </span>
                  </div>
                  <p className="text-gray-900 mb-3">{report.raw_text}</p>
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    {report.location?.name && (
                      <span className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {report.location.name}
                      </span>
                    )}
                    <span>
                      {new Date(report.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                {report.ai_analysis && (
                  <div className="text-right">
                    <span className="text-sm font-medium text-gray-900">
                      {report.ai_analysis.hazard_type}
                    </span>
                    <p className="text-sm text-gray-500">
                      {Math.round((report.ai_analysis.confidence || 0) * 100)}% confidence
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <p className="text-gray-500">No reports found</p>
        </div>
      )}
    </div>
  )
}