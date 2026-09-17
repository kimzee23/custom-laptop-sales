import { create } from 'zustand'
import { CartItem } from '@/types'

interface CartStore {
  items: CartItem[]
  isOpen: boolean
  isCheckoutOpen: boolean
  addItem: (item: Omit<CartItem, 'id' | 'totalPrice'>) => void
  removeItem: (id: string) => void
  updateQuantity: (id: string, quantity: number) => void
  clearCart: () => void
  toggleCart: () => void
  setIsOpen: (isOpen: boolean) => void
  setIsCheckoutOpen: (isOpen: boolean) => void
  getTotalItems: () => number
  getSubtotal: () => number
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],
  isOpen: false,
  isCheckoutOpen: false,

  addItem: (newItem) => {
    set((state) => {
      // Check if exact same item and configuration exists
      const existingIndex = state.items.findIndex(
        (i) => i.productId === newItem.productId && 
               JSON.stringify(i.configuration || {}) === JSON.stringify(newItem.configuration || {})
      )

      if (existingIndex > -1) {
        const updated = [...state.items]
        const item = updated[existingIndex]
        const newQty = item.quantity + newItem.quantity
        updated[existingIndex] = {
          ...item,
          quantity: newQty,
          totalPrice: newQty * item.unitPrice,
        }
        return { items: updated, isOpen: true }
      }

      const generatedId = `cart-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`
      const addedItem: CartItem = {
        ...newItem,
        id: generatedId,
        totalPrice: newItem.quantity * newItem.unitPrice,
      }
      return { items: [...state.items, addedItem], isOpen: true }
    })
  },

  removeItem: (id) => {
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    }))
  },

  updateQuantity: (id, quantity) => {
    if (quantity <= 0) {
      get().removeItem(id)
      return
    }
    set((state) => ({
      items: state.items.map((item) =>
        item.id === id
          ? { ...item, quantity, totalPrice: quantity * item.unitPrice }
          : item
      ),
    }))
  },

  clearCart: () => set({ items: [] }),
  toggleCart: () => set((state) => ({ isOpen: !state.isOpen })),
  setIsOpen: (isOpen) => set({ isOpen }),
  setIsCheckoutOpen: (isCheckoutOpen) => set({ isCheckoutOpen }),

  getTotalItems: () => {
    return get().items.reduce((acc, item) => acc + item.quantity, 0)
  },

  getSubtotal: () => {
    return get().items.reduce((acc, item) => acc + item.totalPrice, 0)
  },
}))
