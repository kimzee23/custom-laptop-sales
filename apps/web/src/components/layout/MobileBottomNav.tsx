'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Home, SlidersHorizontal, ShoppingCart, Heart, User, UserPlus } from 'lucide-react'
import { useCartStore } from '@/stores/cartStore'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { useAuthStore } from '@/stores/authStore'

export const MobileBottomNav: React.FC = () => {
  const pathname = usePathname()
  const { toggleCart, getTotalItems } = useCartStore()
  const { items: wishlistItems, setIsOpen: setWishlistOpen } = useWishlistStore()
  const { openConfigurator } = useConfiguratorStore()
  const { user, isAuthenticated } = useAuthStore()

  const totalCartItems = getTotalItems()
  const totalWishlistItems = wishlistItems.length

  const handleOpenConfigurator = () => {
    openConfigurator({
      id: 'prod-titanforge-predator-16',
      title: 'TitanForge Predator 16 Pro Gaming Laptop',
      slug: 'titanforge-predator-16-pro',
      base_price: 1450000,
      image_url: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80',
      gallery_images: [],
      rating: 4.9,
      review_count: 48,
      stock: 18,
      is_featured: true,
      is_flash_deal: true,
      is_best_seller: true,
      is_customizable: true,
      specs: {
        processor: 'Intel Core i9-14900HX',
        ram: '32GB DDR5',
        storage: '1TB NVMe',
        gpu: 'RTX 4070 8GB',
      }
    })
  }

  return (
    <nav className="sm:hidden fixed bottom-0 left-0 right-0 z-30 bg-white/95 backdrop-blur-md border-t border-border shadow-[0_-4px_16px_rgba(0,0,0,0.06)] px-2 py-1.5 flex items-center justify-around">
      
      {/* Home */}
      <Link
        href="/"
        className={`flex flex-col items-center justify-center min-w-[54px] py-1 text-[10px] font-bold transition-colors ${
          pathname === '/' ? 'text-primary' : 'text-slate-500 hover:text-navy'
        }`}
      >
        <Home size={20} />
        <span className="mt-0.5">Home</span>
      </Link>

      {/* Build / Customizer */}
      <button
        type="button"
        onClick={handleOpenConfigurator}
        className="flex flex-col items-center justify-center min-w-[54px] py-1 text-[10px] font-bold text-slate-500 hover:text-navy transition-colors"
      >
        <SlidersHorizontal size={20} className="text-primary" />
        <span className="mt-0.5 text-primary">Customizer</span>
      </button>

      {/* Cart */}
      <button
        type="button"
        onClick={toggleCart}
        className="flex flex-col items-center justify-center min-w-[54px] py-1 text-[10px] font-bold text-slate-500 hover:text-navy transition-colors relative"
      >
        <div className="relative">
          <ShoppingCart size={20} />
          {totalCartItems > 0 && (
            <span className="absolute -top-1.5 -right-2 bg-primary text-white text-[9px] font-black w-4 h-4 rounded-full flex items-center justify-center shadow-sm">
              {totalCartItems}
            </span>
          )}
        </div>
        <span className="mt-0.5">Cart</span>
      </button>

      {/* Wishlist */}
      <button
        type="button"
        onClick={() => setWishlistOpen(true)}
        className="flex flex-col items-center justify-center min-w-[54px] py-1 text-[10px] font-bold text-slate-500 hover:text-navy transition-colors relative"
      >
        <div className="relative">
          <Heart size={20} />
          {totalWishlistItems > 0 && (
            <span className="absolute -top-1.5 -right-2 bg-error text-white text-[9px] font-black w-4 h-4 rounded-full flex items-center justify-center shadow-sm">
              {totalWishlistItems}
            </span>
          )}
        </div>
        <span className="mt-0.5">Saved</span>
      </button>

      {/* Sign Up or My Account Button */}
      {isAuthenticated && user ? (
        <Link
          href="/account"
          className={`flex flex-col items-center justify-center min-w-[54px] py-1 text-[10px] font-bold transition-colors ${
            pathname?.startsWith('/account') ? 'text-primary' : 'text-slate-500 hover:text-navy'
          }`}
        >
          <div className="w-5 h-5 rounded-full bg-primary text-white flex items-center justify-center text-[10px] font-bold">
            {user.name ? user.name.charAt(0) : 'U'}
          </div>
          <span className="mt-0.5 truncate max-w-[50px]">{user.name.split(' ')[0]}</span>
        </Link>
      ) : (
        <Link
          href="/auth/register"
          className="flex flex-col items-center justify-center min-w-[54px] py-1 text-[10px] font-extrabold text-primary hover:text-primary-hover transition-colors"
        >
          <div className="w-5 h-5 rounded-md bg-primary/10 text-primary flex items-center justify-center">
            <UserPlus size={14} />
          </div>
          <span className="mt-0.5 text-primary">Sign Up</span>
        </Link>
      )}

    </nav>
  )
}
