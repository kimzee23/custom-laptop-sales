import { create } from 'zustand'
import { Product } from '@/types'

interface WishlistStore {
  items: Product[]
  isOpen: boolean
  toggleWishlist: (product: Product) => void
  isInWishlist: (productId: string) => boolean
  removeItem: (productId: string) => void
  setIsOpen: (isOpen: boolean) => void
}

export const useWishlistStore = create<WishlistStore>((set, get) => ({
  items: [],
  isOpen: false,
  toggleWishlist: (product) => {
    set((state) => {
      const exists = state.items.some((item) => item.id === product.id)
      if (exists) {
        return { items: state.items.filter((item) => item.id !== product.id) }
      }
      return { items: [...state.items, product] }
    })
  },
  isInWishlist: (productId) => {
    return get().items.some((item) => item.id === productId)
  },
  removeItem: (productId) => {
    set((state) => ({
      items: state.items.filter((item) => item.id !== productId)
    }))
  },
  setIsOpen: (isOpen) => set({ isOpen })
}))

