import React, { useEffect, useState } from 'react'
import { AlertCircle, TrendingUp, Package, AlertTriangle, BarChart3 } from 'lucide-react'
import { dashboardAPI, medicinesAPI, salesAPI } from '../services/api'
import toast from 'react-hot-toast'

interface DashboardStats {
  total_medicines: number
  low_stock_medicines: number
  out_of_stock_medicines: number
  total_sales_today: number
  total_units_sold_today: number
  critical_alerts: number
  pending_predictions: number
}

function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [lowStockItems, setLowStockItems] = useState([])
  const [todaySales, setTodaySales] = useState(0)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [statsRes, lowStockRes, salesTodayRes] = await Promise.all([
        dashboardAPI.getStats(),
        medicinesAPI.getLowStock(),
        salesAPI.getTodayStats(),
      ])

      setStats(statsRes.data)
      setLowStockItems(lowStockRes.data.slice(0, 5))
      setTodaySales(salesTodayRes.data.total_amount)
    } catch (error: any) {
      toast.error('Failed to load dashboard data')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-gray-600">Loading dashboard...</div>
      </div>
    )
  }

  const StatCard = ({ title, value, icon: Icon, color }: any) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon size={24} className="text-white" />
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg shadow p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">Welcome to AI Pharmacy Management</h2>
        <p className="text-green-100">Monitor your pharmacy inventory and sales in real-time</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Medicines"
          value={stats?.total_medicines}
          icon={Package}
          color="bg-blue-500"
        />
        <StatCard
          title="Low Stock Items"
          value={stats?.low_stock_medicines}
          icon={AlertTriangle}
          color="bg-yellow-500"
        />
        <StatCard
          title="Out of Stock"
          value={stats?.out_of_stock_medicines}
          icon={AlertCircle}
          color="bg-red-500"
        />
        <StatCard
          title="Today's Sales"
          value={`₹${todaySales.toFixed(2)}`}
          icon={TrendingUp}
          color="bg-green-500"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Low Stock Items */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="text-yellow-500" size={24} />
            <h3 className="text-xl font-bold text-gray-800">Low Stock Alerts</h3>
          </div>

          {lowStockItems.length > 0 ? (
            <div className="space-y-3">
              {lowStockItems.map((item: any) => (
                <div key={item.id} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                  <div>
                    <p className="font-semibold text-gray-800">{item.medicine_name}</p>
                    <p className="text-sm text-gray-600">Stock: {item.current_stock} | Reorder: {item.reorder_level}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-yellow-600">⚠️ Low</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 py-4">All medicines are well-stocked!</p>
          )}
        </div>

        {/* Key Metrics */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="text-green-500" size={24} />
            <h3 className="text-xl font-bold text-gray-800">Summary</h3>
          </div>

          <div className="space-y-4">
            <div className="p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600">Units Sold Today</p>
              <p className="text-2xl font-bold text-blue-600">{stats?.total_units_sold_today}</p>
            </div>

            <div className="p-3 bg-red-50 rounded-lg">
              <p className="text-sm text-gray-600">Critical Alerts</p>
              <p className="text-2xl font-bold text-red-600">{stats?.critical_alerts}</p>
            </div>

            <div className="p-3 bg-purple-50 rounded-lg">
              <p className="text-sm text-gray-600">Pending Predictions</p>
              <p className="text-2xl font-bold text-purple-600">{stats?.pending_predictions}</p>
            </div>
          </div>

          <button
            onClick={fetchDashboardData}
            className="w-full mt-4 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          >
            🔄 Refresh
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
