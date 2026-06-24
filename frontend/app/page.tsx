import Link from 'next/link'
import { AlertTriangle, Droplets, Map, Bell, BarChart3 } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="border-b bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Droplets className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">FloodWatch AI</span>
          </div>
          <nav className="flex items-center gap-4">
            <Link href="/auth/login" className="text-gray-600 hover:text-gray-900">
              Login
            </Link>
            <Link
              href="/auth/register"
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </header>

      <main>
        <section className="py-20 text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Turning Early Warnings into Verified Action
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Community-generated flood intelligence enhanced by AI. Report incidents,
            track incidents on a live map, and receive real-time alerts.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/auth/register"
              className="bg-blue-600 text-white px-8 py-3 rounded-md text-lg hover:bg-blue-700"
            >
              Report an Incident
            </Link>
            <Link
              href="/dashboard"
              className="border border-gray-300 text-gray-700 px-8 py-3 rounded-md text-lg hover:bg-gray-50"
            >
              View Dashboard
            </Link>
          </div>
        </section>

        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-6">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AlertTriangle className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">1. Report</h3>
                <p className="text-gray-600">
                  Citizens submit reports via web, SMS, WhatsApp, or voice
                </p>
              </div>
              <div className="text-center p-6">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Map className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">2. Analyze</h3>
                <p className="text-gray-600">
                  AI classifies hazards, extracts locations, and detects duplicates
                </p>
              </div>
              <div className="text-center p-6">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Bell className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">3. Alert</h3>
                <p className="text-gray-600">
                  Responders and communities receive real-time alerts
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-16 bg-blue-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">Dashboard Features</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <BarChart3 className="h-10 w-10 text-blue-600 mb-4" />
                <h3 className="font-semibold mb-2">Analytics</h3>
                <p className="text-gray-600 text-sm">
                  View trends, risk scores, and incident statistics
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <Map className="h-10 w-10 text-blue-600 mb-4" />
                <h3 className="font-semibold mb-2">Live Map</h3>
                <p className="text-gray-600 text-sm">
                  Interactive GIS map with real-time incident visualization
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <AlertTriangle className="h-10 w-10 text-blue-600 mb-4" />
                <h3 className="font-semibold mb-2">Incident Management</h3>
                <p className="text-gray-600 text-sm">
                  Track, update, and resolve incidents efficiently
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <Bell className="h-10 w-10 text-blue-600 mb-4" />
                <h3 className="font-semibold mb-2">Alert System</h3>
                <p className="text-gray-600 text-sm">
                  Send SMS, WhatsApp, and push notifications
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            FloodWatch AI - Community-powered flood intelligence
          </p>
        </div>
      </footer>
    </div>
  )
}