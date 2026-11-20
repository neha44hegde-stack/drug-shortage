import React from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { LogOut, Home, Pill, ShoppingCart, Brain } from 'lucide-react'
import { useAuthStore } from '../store/authStore'

function Layout() {
  const navigate = useNavigate()
  const { logout, user } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { icon: Home, label: 'Dashboard', path: '/' },
    { icon: Pill, label: 'Medicines', path: '/medicines' },
    { icon: ShoppingCart, label: 'Sales', path: '/sales' },
    { icon: Brain, label: 'Predictions', path: '/predictions' },
  ]

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-green-600">💊 Pharmacy</h1>
          <p className="text-gray-600 text-sm">AI Management System</p>
        </div>

        <nav className="mt-8">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className="w-full flex items-center gap-3 px-6 py-3 text-gray-700 hover:bg-green-50 hover:text-green-600 transition"
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            )
          })}
        </nav>

        <div className="absolute bottom-0 w-64 p-6 border-t">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-sm font-semibold text-gray-800">{user?.username}</p>
              <p className="text-xs text-gray-600 capitalize">{user?.role}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 bg-red-600 text-white py-2 rounded hover:bg-red-700 transition"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="px-8 py-6 flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-800">AI Pharmacy Management</h2>
            <div className="text-sm text-gray-600">
              {new Date().toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          <Outlet />
        </div>
      </div>
    </div>
  )
}

export default Layout
