import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth-storage')
  if (token) {
    try {
      const authData = JSON.parse(token)
      if (authData.state?.token) {
        config.headers.Authorization = `Bearer ${authData.state.token}`
      }
    } catch (error) {
      console.error('Error parsing auth token:', error)
    }
  }
  return config
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth-storage')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ==================== MEDICINES API ====================
export const medicinesAPI = {
  getAll: (skip = 0, limit = 100) =>
    apiClient.get('/medicines', { params: { skip, limit } }),
  
  getById: (id: number) =>
    apiClient.get(`/medicines/${id}`),
  
  getLowStock: () =>
    apiClient.get('/medicines/low-stock'),
  
  getOutOfStock: () =>
    apiClient.get('/medicines/out-of-stock'),
  
  create: (data: any) =>
    apiClient.post('/medicines', data),
  
  update: (id: number, data: any) =>
    apiClient.put(`/medicines/${id}`, data),
  
  delete: (id: number) =>
    apiClient.delete(`/medicines/${id}`),
}

// ==================== SALES API ====================
export const salesAPI = {
  getAll: (skip = 0, limit = 100) =>
    apiClient.get('/sales', { params: { skip, limit } }),
  
  getById: (id: number) =>
    apiClient.get(`/sales/${id}`),
  
  getTodayStats: () =>
    apiClient.get('/sales/statistics/today'),
  
  getMonthlyStats: () =>
    apiClient.get('/sales/statistics/monthly'),
  
  create: (data: any) =>
    apiClient.post('/sales', data),
}

// ==================== PREDICTIONS API ====================
export const predictionsAPI = {
  getAll: (skip = 0, limit = 100) =>
    apiClient.get('/predictions', { params: { skip, limit } }),
  
  getById: (id: number) =>
    apiClient.get(`/predictions/${id}`),
  
  getShortages: () =>
    apiClient.get('/predictions/shortages'),
  
  create: (data: any) =>
    apiClient.post('/predictions', data),
}

// ==================== DASHBOARD API ====================
export const dashboardAPI = {
  getStats: () =>
    apiClient.get('/dashboard/stats'),
}

export default apiClient
