import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { AuthState, User, UserAddress, SavedCustomBuild, LoginCredentials, RegisterData } from '@/types/auth'

// Pre-seeded demo customers for fast 1-click testing
export const DEMO_ACCOUNTS: Array<{ label: string; email: string; pass: string; user: User }> = [
  {
    label: 'Emeka Adeleke (Pro Gamer & Creator)',
    email: 'emeka.adeleke@example.com',
    pass: 'password123',
    user: {
      id: 'usr_emeka_01',
      name: 'Emeka Adeleke',
      email: 'emeka.adeleke@example.com',
      phone: '08031234567',
      avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
      role: 'customer',
      joinedAt: '2024-01-15',
      rewardPoints: 4800,
      addresses: [
        {
          id: 'addr_01',
          title: 'Home / Studio',
          fullName: 'Emeka Adeleke',
          phone: '08031234567',
          street: 'Plot 14B, Admiralty Way, Lekki Phase 1',
          city: 'Lekki / Lagos Island',
          state: 'Lagos State',
          isDefault: true,
        },
        {
          id: 'addr_02',
          title: 'Tech Hub Office',
          fullName: 'Emeka Adeleke',
          phone: '08031234567',
          street: '28 Commercial Avenue, Sabo, Yaba',
          city: 'Yaba / Mainland',
          state: 'Lagos State',
          isDefault: false,
        }
      ],
      savedBuilds: [
        {
          id: 'build_01',
          title: 'My Custom TitanForge Predator 16',
          productId: 'prod-titanforge-predator-16',
          productTitle: 'TitanForge Predator 16 Pro Gaming Laptop',
          imageUrl: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80',
          totalPrice: 1650000,
          savedAt: '2024-03-01',
          configuration: {
            productId: 'prod-titanforge-predator-16',
            productTitle: 'TitanForge Predator 16 Pro Gaming Laptop',
            basePrice: 1450000,
            colorId: 'opt-color-space-grey',
            ramId: 'opt-ram-64gb',
            storageId: 'opt-storage-2tb',
            accessoryIds: ['opt-acc-sleeve']
          },
          specsSummary: {
            cpu: 'Intel Core i9-14900HX',
            ram: '64GB DDR5',
            storage: '2TB NVMe PCIe 4.0',
            gpu: 'RTX 4070 8GB GDDR6',
            color: 'Space Grey Stealth'
          }
        }
      ]
    }
  },
  {
    label: 'Zainab Abubakar (Software Engineer)',
    email: 'zainab.a@example.com',
    pass: 'password123',
    user: {
      id: 'usr_zainab_02',
      name: 'Zainab Abubakar',
      email: 'zainab.a@example.com',
      phone: '08129876543',
      avatarUrl: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80',
      role: 'customer',
      joinedAt: '2024-02-10',
      rewardPoints: 2150,
      addresses: [
        {
          id: 'addr_03',
          title: 'Primary Residence',
          fullName: 'Zainab Abubakar',
          phone: '08129876543',
          street: '5 Ahmadu Bello Way, Victoria Island',
          city: 'Victoria Island',
          state: 'Lagos State',
          isDefault: true,
        }
      ],
      savedBuilds: []
    }
  }
]

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials: LoginCredentials) => {
        set({ isLoading: true, error: null })
        
        // Simulate network latency
        await new Promise((resolve) => setTimeout(resolve, 600))

        // Check if matches demo accounts
        const matchedDemo = DEMO_ACCOUNTS.find(
          (acc) => acc.email.toLowerCase() === credentials.email.toLowerCase()
        )

        if (matchedDemo) {
          if (credentials.password === matchedDemo.pass || credentials.password.length >= 6) {
            set({
              user: matchedDemo.user,
              token: `jwt_token_${matchedDemo.user.id}_${Date.now()}`,
              isAuthenticated: true,
              isLoading: false,
              error: null
            })
            return { success: true }
          } else {
            set({ isLoading: false, error: 'Invalid password. Try password123' })
            return { success: false, error: 'Invalid password. Try password123' }
          }
        }

        // Generic mock customer login for any valid email & password
        if (credentials.email.includes('@') && credentials.password.length >= 6) {
          const newUser: User = {
            id: `usr_${Date.now()}`,
            name: credentials.email.split('@')[0].replace(/[\._]/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            email: credentials.email,
            phone: '08000000000',
            role: 'customer',
            joinedAt: new Date().toISOString().split('T')[0],
            rewardPoints: 500,
            addresses: [],
            savedBuilds: []
          }

          set({
            user: newUser,
            token: `jwt_token_${newUser.id}_${Date.now()}`,
            isAuthenticated: true,
            isLoading: false,
            error: null
          })
          return { success: true }
        }

        const err = 'Invalid email or password (must be at least 6 characters).'
        set({ isLoading: false, error: err })
        return { success: false, error: err }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true, error: null })
        await new Promise((resolve) => setTimeout(resolve, 800))

        if (!data.name || !data.email || !data.password) {
          const err = 'Please fill in all required fields.'
          set({ isLoading: false, error: err })
          return { success: false, error: err }
        }

        const newUser: User = {
          id: `usr_${Date.now()}`,
          name: data.name,
          email: data.email,
          phone: data.phone,
          role: 'customer',
          joinedAt: new Date().toISOString().split('T')[0],
          rewardPoints: 1000, // Welcome signup bonus
          addresses: [],
          savedBuilds: []
        }

        set({
          user: newUser,
          token: `jwt_token_${newUser.id}_${Date.now()}`,
          isAuthenticated: true,
          isLoading: false,
          error: null
        })

        return { success: true }
      },

      socialLogin: async (provider) => {
        set({ isLoading: true, error: null })
        await new Promise((resolve) => setTimeout(resolve, 700))

        const demoName = provider === 'google' ? 'Google User' : provider === 'github' ? 'Dev Creator' : 'Apple ID Member'
        const newUser: User = {
          id: `usr_${provider}_${Date.now()}`,
          name: demoName,
          email: `${provider}.member@example.com`,
          avatarUrl: `https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80`,
          role: 'customer',
          joinedAt: new Date().toISOString().split('T')[0],
          rewardPoints: 1000,
          addresses: [],
          savedBuilds: []
        }

        set({
          user: newUser,
          token: `jwt_token_${provider}_${Date.now()}`,
          isAuthenticated: true,
          isLoading: false,
          error: null
        })

        return { success: true }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null
        })
      },

      updateProfile: (data) => {
        const currentUser = get().user
        if (!currentUser) return
        set({
          user: {
            ...currentUser,
            ...data
          }
        })
      },

      addAddress: (addressData) => {
        const currentUser = get().user
        if (!currentUser) return
        const newAddress: UserAddress = {
          ...addressData,
          id: `addr_${Date.now()}`
        }
        const updatedAddresses = addressData.isDefault
          ? currentUser.addresses.map(a => ({ ...a, isDefault: false })).concat(newAddress)
          : [...currentUser.addresses, newAddress]

        set({
          user: {
            ...currentUser,
            addresses: updatedAddresses
          }
        })
      },

      updateAddress: (id, updatedFields) => {
        const currentUser = get().user
        if (!currentUser) return
        let updated = currentUser.addresses.map(a => a.id === id ? { ...a, ...updatedFields } : a)
        if (updatedFields.isDefault) {
          updated = updated.map(a => a.id === id ? a : { ...a, isDefault: false })
        }
        set({
          user: {
            ...currentUser,
            addresses: updated
          }
        })
      },

      deleteAddress: (id) => {
        const currentUser = get().user
        if (!currentUser) return
        set({
          user: {
            ...currentUser,
            addresses: currentUser.addresses.filter(a => a.id !== id)
          }
        })
      },

      setDefaultAddress: (id) => {
        const currentUser = get().user
        if (!currentUser) return
        set({
          user: {
            ...currentUser,
            addresses: currentUser.addresses.map(a => ({
              ...a,
              isDefault: a.id === id
            }))
          }
        })
      },

      saveCustomBuild: (buildData) => {
        const currentUser = get().user
        if (!currentUser) return
        const newBuild: SavedCustomBuild = {
          ...buildData,
          id: `build_${Date.now()}`,
          savedAt: new Date().toISOString().split('T')[0]
        }
        const existing = currentUser.savedBuilds || []
        set({
          user: {
            ...currentUser,
            savedBuilds: [newBuild, ...existing]
          }
        })
      },

      removeSavedBuild: (id) => {
        const currentUser = get().user
        if (!currentUser) return
        set({
          user: {
            ...currentUser,
            savedBuilds: (currentUser.savedBuilds || []).filter(b => b.id !== id)
          }
        })
      },

      clearError: () => set({ error: null })
    }),
    {
      name: 'realtech_auth_storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
)
