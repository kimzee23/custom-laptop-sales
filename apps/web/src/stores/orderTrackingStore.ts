import { create } from 'zustand'

interface OrderTrackingStore {
  isOpen: boolean
  orderNumber: string
  openTracking: (orderNumber?: string) => void
  closeTracking: () => void
}

export const useOrderTrackingStore = create<OrderTrackingStore>((set) => ({
  isOpen: false,
  orderNumber: '',
  openTracking: (orderNumber = '') => set({ isOpen: true, orderNumber }),
  closeTracking: () => set({ isOpen: false, orderNumber: '' })
}))
