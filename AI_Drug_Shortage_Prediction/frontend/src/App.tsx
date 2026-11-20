import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

// Pages
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Medicines from './pages/Medicines'
import Sales from './pages/Sales'
import Predictions from './pages/Predictions'
import Layout from './components/Layout'

// Context
import { useAuthStore } from './store/authStore'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          {isAuthenticated ? (
            <Route element={<Layout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/medicines" element={<Medicines />} />
              <Route path="/sales" element={<Sales />} />
              <Route path="/predictions" element={<Predictions />} />
            </Route>
          ) : (
            <Route path="*" element={<Navigate to="/login" replace />} />
          )}
        </Routes>
      </BrowserRouter>
      <Toaster />
    </>
  )
}

export default App
