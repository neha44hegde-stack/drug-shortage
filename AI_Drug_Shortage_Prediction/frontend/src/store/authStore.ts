import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
  role: string
}

interface AuthStore {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string, role: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username, password) => {
        try {
          const response = await axios.post('/api/auth/login', {
            username,
            password,
          })
          
          const { access_token, token_type } = response.data
          
          // Set token in axios headers
          axios.defaults.headers.common['Authorization'] = `${token_type} ${access_token}`
          
          // Get user data (you might want to decode JWT or add another endpoint)
          set({
            token: access_token,
            isAuthenticated: true,
            user: {
              id: 1,
              username,
              email: '',
              role: 'pharmacist'
            }
          })
        } catch (error) {
          throw error
        }
      },

      register: async (username, email, password, role) => {
        try {
          await axios.post('/api/auth/register', {
            username,
            email,
            password,
            role,
          })
        } catch (error) {
          throw error
        }
      },

      logout: () => {
        delete axios.defaults.headers.common['Authorization']
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      setUser: (user) => {
        set({ user })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
