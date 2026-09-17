'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Search, ShoppingCart, Heart, User, Sparkles, SlidersHorizontal, LogOut, ChevronDown, Package, ShieldCheck, MapPin } from 'lucide-react'
import { useCartStore } from '@/stores/cartStore'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useOrderTrackingStore } from '@/stores/orderTrackingStore'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { useAuthStore } from '@/stores/authStore'
import { Button } from '@/components/ui/Button'

interface StoreHeaderProps {
  onSearchChange?: (query: string) => void
}

export const StoreHeader: React.FC<StoreHeaderProps> = ({ onSearchChange }) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearchFocused, setIsSearchFocused] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)
  
  const { toggleCart, getTotalItems } = useCartStore()
  const { items: wishlistItems, setIsOpen: setWishlistOpen } = useWishlistStore()
  const { openTracking } = useOrderTrackingStore()
  const { openConfigurator } = useConfiguratorStore()
  const { user, isAuthenticated, logout } = useAuthStore()

  const totalCartItems = getTotalItems()
  const totalWishlistItems = wishlistItems.length

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (onSearchChange) {
      onSearchChange(searchQuery)
    }
  }

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20 gap-4 lg:gap-8">
          
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-2.5 flex-shrink-0 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-primary-sky flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
              <Sparkles size={22} className="animate-pulse-subtle" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-black tracking-tight text-navy leading-none font-display">
                REAL<span className="text-primary">TECH</span>
              </span>
              <span className="text-[10px] font-bold tracking-widest text-muted uppercase">
                Custom Laptops & Store
              </span>
            </div>
          </Link>

          {/* Prominent Search Bar */}
          <div className="flex-1 max-w-2xl relative hidden sm:block">
            <form onSubmit={handleSearch} className="relative">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value)
                    if (onSearchChange) onSearchChange(e.target.value)
                  }}
                  onFocus={() => setIsSearchFocused(true)}
                  onBlur={() => setTimeout(() => setIsSearchFocused(false), 200)}
                  placeholder="Search laptops, RTX 4070, 32GB RAM, OLED, brands, or accessories..."
                  className="w-full h-11 pl-11 pr-24 rounded-full border-2 border-border bg-background text-sm text-foreground placeholder:text-muted focus:border-primary focus:bg-white focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-inner"
                />
                <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-muted" />
                <Button
                  type="submit"
                  variant="primary"
                  size="sm"
                  className="absolute right-1.5 top-1/2 -translate-y-1/2 rounded-full px-4 h-8"
                >
                  Search
                </Button>
              </div>
            </form>

            {/* Instant Search Suggestions Dropdown */}
            {isSearchFocused && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-dropdown border border-border p-3 z-50 animate-fade-in">
                <div className="text-[11px] font-bold text-muted uppercase tracking-wider px-2 py-1">
                  Popular Searches
                </div>
                <div className="flex flex-wrap gap-1.5 p-1">
                  {['TitanForge Predator', 'RTX 4070 Laptops', '32GB RAM Deals', 'Student Lightweight', 'OLED Creator 16"', 'Thunderbolt Docks'].map((term) => (
                    <button
                      key={term}
                      onClick={() => {
                        setSearchQuery(term)
                        if (onSearchChange) onSearchChange(term)
                      }}
                      className="px-2.5 py-1 text-xs bg-primary-soft text-navy hover:bg-primary-light hover:text-primary rounded-lg transition-colors font-medium"
                    >
                      {term}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Action CTAs: Custom Builder CTA, Wishlist, Account, Cart */}
          <div className="flex items-center gap-2 sm:gap-3">
            
            {/* Quick Builder CTA button */}
            <Button 
              variant="secondary" 
              size="md" 
              className="hidden lg:inline-flex gap-2 border border-primary/20"
              onClick={() => {
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
              }}
            >
              <SlidersHorizontal size={16} className="text-primary" />
              <span>Custom Builder</span>
            </Button>

            {/* Wishlist */}
            <button
              onClick={() => setWishlistOpen(true)}
              className="relative p-2.5 rounded-xl text-navy hover:bg-primary-soft hover:text-primary transition-colors"
              title="Saved Builds & Wishlist"
            >
              <Heart size={22} />
              {totalWishlistItems > 0 && (
                <span className="absolute top-1 right-1 w-5 h-5 bg-error text-white text-[11px] font-extrabold rounded-full flex items-center justify-center shadow-sm">
                  {totalWishlistItems}
                </span>
              )}
            </button>

            {/* Account & User Menu */}
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                onBlur={() => setTimeout(() => setIsUserMenuOpen(false), 250)}
                className="hidden sm:flex items-center gap-2 p-2 rounded-xl text-navy hover:bg-primary-soft hover:text-primary transition-colors text-xs font-semibold"
                title={isAuthenticated ? `Signed in as ${user?.name}` : "Sign In or View Account"}
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs ${
                  isAuthenticated 
                    ? 'bg-primary text-white shadow-sm' 
                    : 'bg-primary-soft text-primary'
                }`}>
                  {isAuthenticated && user?.name ? (
                    user.name.charAt(0)
                  ) : (
                    <User size={18} />
                  )}
                </div>
                <div className="text-left hidden md:block leading-tight">
                  <span className="block text-[10px] text-muted font-normal">
                    {isAuthenticated ? 'My Account' : 'Welcome'}
                  </span>
                  <span className="font-bold text-navy flex items-center gap-1">
                    {isAuthenticated ? user?.name.split(' ')[0] : 'Sign In'}
                    <ChevronDown size={12} className="text-muted" />
                  </span>
                </div>
              </button>

              {/* User Dropdown Menu */}
              {isUserMenuOpen && (
                <div className="absolute right-0 top-full mt-2 w-64 bg-white rounded-2xl shadow-dropdown border border-border p-2 z-50 animate-fade-in text-foreground">
                  {isAuthenticated && user ? (
                    <>
                      {/* Logged in header info */}
                      <div className="p-3 bg-primary-soft/60 rounded-xl mb-2">
                        <div className="font-bold text-xs text-navy leading-tight">{user.name}</div>
                        <div className="text-[11px] text-muted truncate">{user.email}</div>
                        <div className="mt-2 flex items-center justify-between text-[10px]">
                          <span className="px-2 py-0.5 rounded-full bg-primary/10 text-primary font-bold">
                            {user.rewardPoints} Reward Pts
                          </span>
                          <span className="text-emerald-600 font-semibold flex items-center gap-0.5">
                            <ShieldCheck size={12} /> Warranty
                          </span>
                        </div>
                      </div>

                      <div className="space-y-0.5 text-xs font-medium">
                        <Link
                          href="/account"
                          onClick={() => setIsUserMenuOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 rounded-lg hover:bg-primary-soft hover:text-primary transition-colors text-navy"
                        >
                          <User size={15} />
                          <span>My Profile & Dashboard</span>
                        </Link>
                        
                        <Link
                          href="/account?tab=builds"
                          onClick={() => setIsUserMenuOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 rounded-lg hover:bg-primary-soft hover:text-primary transition-colors text-navy"
                        >
                          <SlidersHorizontal size={15} />
                          <span>Saved Custom Builds ({user.savedBuilds?.length || 0})</span>
                        </Link>

                        <Link
                          href="/account?tab=addresses"
                          onClick={() => setIsUserMenuOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 rounded-lg hover:bg-primary-soft hover:text-primary transition-colors text-navy"
                        >
                          <MapPin size={15} />
                          <span>Delivery Addresses</span>
                        </Link>

                        <button
                          type="button"
                          onClick={() => {
                            setIsUserMenuOpen(false)
                            openTracking()
                          }}
                          className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg hover:bg-primary-soft hover:text-primary transition-colors text-navy text-left"
                        >
                          <Package size={15} />
                          <span>Track Build / Order Live</span>
                        </button>
                      </div>

                      <div className="pt-2 mt-2 border-t border-border">
                        <button
                          type="button"
                          onClick={() => {
                            logout()
                            setIsUserMenuOpen(false)
                          }}
                          className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-error hover:bg-error-light transition-colors text-xs font-semibold text-left"
                        >
                          <LogOut size={15} />
                          <span>Sign Out</span>
                        </button>
                      </div>
                    </>
                  ) : (
                    <>
                      {/* Guest prompt */}
                      <div className="p-3 text-center space-y-2">
                        <p className="text-xs font-bold text-navy">Customer Sign In</p>
                        <p className="text-[11px] text-muted">
                          Sign in to access saved custom laptop builds & 1-click checkout.
                        </p>
                        <div className="space-y-1.5 pt-1">
                          <Link
                            href="/auth/login"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="block w-full py-2 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold text-center transition-colors shadow-sm"
                          >
                            Sign In
                          </Link>
                          <Link
                            href="/auth/register"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="block w-full py-2 rounded-xl bg-primary-soft hover:bg-primary/10 text-primary text-xs font-bold text-center transition-colors"
                          >
                            Create Account
                          </Link>
                        </div>
                      </div>

                      <div className="pt-2 border-t border-border">
                        <button
                          type="button"
                          onClick={() => {
                            setIsUserMenuOpen(false)
                            openTracking()
                          }}
                          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg hover:bg-background text-xs font-medium text-muted hover:text-navy"
                        >
                          <Package size={14} />
                          <span>Track Order (Guest)</span>
                        </button>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>

            {/* Cart Trigger */}
            <button
              onClick={toggleCart}
              className="relative flex items-center gap-2 bg-primary text-white hover:bg-primary-hover px-4 py-2.5 rounded-xl shadow-sm hover:shadow-md transition-all active:scale-95"
            >
              <ShoppingCart size={20} />
              <div className="flex flex-col text-left leading-none hidden sm:block">
                <span className="text-[10px] text-blue-100 font-medium">Cart</span>
                <span className="text-xs font-extrabold">
                  {totalCartItems} {totalCartItems === 1 ? 'item' : 'items'}
                </span>
              </div>
              {totalCartItems > 0 && (
                <span className="sm:hidden w-5 h-5 bg-white text-primary text-[11px] font-extrabold rounded-full flex items-center justify-center">
                  {totalCartItems}
                </span>
              )}
            </button>
          </div>

        </div>

        {/* Mobile Search input */}
        <div className="pb-3 sm:hidden">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value)
                if (onSearchChange) onSearchChange(e.target.value)
              }}
              placeholder="Search laptops, RTX, RAM, SSD..."
              className="w-full h-10 pl-10 pr-4 rounded-full border border-border bg-background text-sm text-foreground focus:border-primary focus:bg-white focus:outline-none"
            />
            <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
          </div>
        </div>

      </div>
    </header>
  )
}
