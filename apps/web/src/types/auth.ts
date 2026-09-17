import { LaptopConfigurationState } from './index'

export interface UserAddress {
  id: string
  title: string // e.g. "Home", "Office", "Studio"
  fullName: string
  phone: string
  street: string
  city: string
  state: string
  isDefault: boolean
}

export interface SavedCustomBuild {
  id: string
  title: string
  productId: string
  productTitle: string
  imageUrl: string
  totalPrice: number
  savedAt: string
  configuration: LaptopConfigurationState
  specsSummary: {
    cpu?: string
    ram?: string
    storage?: string
    gpu?: string
    color?: string
  }
}

export interface User {
  id: string
  name: string
  email: string
  phone?: string
  avatarUrl?: string
  role: 'customer' | 'admin'
  joinedAt: string
  rewardPoints: number
  addresses: UserAddress[]
  savedBuilds?: SavedCustomBuild[]
}

export interface LoginCredentials {
  email: string
  password: string
  rememberMe?: boolean
}

export interface RegisterData {
  name: string
  email: string
  phone: string
  password: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<{ success: boolean; error?: string }>
  register: (data: RegisterData) => Promise<{ success: boolean; error?: string }>
  socialLogin: (provider: 'google' | 'github' | 'apple') => Promise<{ success: boolean; error?: string }>
  logout: () => void
  updateProfile: (data: Partial<Pick<User, 'name' | 'phone' | 'avatarUrl'>>) => void
  addAddress: (address: Omit<UserAddress, 'id'>) => void
  updateAddress: (id: string, address: Partial<UserAddress>) => void
  deleteAddress: (id: string) => void
  setDefaultAddress: (id: string) => void
  saveCustomBuild: (build: Omit<SavedCustomBuild, 'id' | 'savedAt'>) => void
  removeSavedBuild: (id: string) => void
  clearError: () => void
}
