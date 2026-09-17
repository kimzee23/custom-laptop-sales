'use client'

import React from 'react'
import Image from 'next/image'
import { X, Trash2, Heart, ShoppingBag, ArrowRight, SlidersHorizontal } from 'lucide-react'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useCartStore } from '@/stores/cartStore'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { formatPrice } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'

export const WishlistDrawer: React.FC = () => {
  const { items, isOpen, setIsOpen, removeItem } = useWishlistStore()
  const { addItem } = useCartStore()
  const { openConfigurator } = useConfiguratorStore()

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-hidden animate-fade-in">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-navy/60 backdrop-blur-sm transition-opacity"
        onClick={() => setIsOpen(false)}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col">
          
          {/* Header */}
          <div className="p-5 border-b border-border flex items-center justify-between bg-primary-soft">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-error/10 flex items-center justify-center text-error">
                <Heart size={20} className="fill-error" />
              </div>
              <div>
                <h2 className="text-base font-bold text-navy">Saved Builds & Wishlist</h2>
                <p className="text-xs text-muted">
                  {items.length} {items.length === 1 ? 'laptop' : 'laptops'} saved for later
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-2 rounded-lg text-muted hover:text-navy hover:bg-white transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          {/* Items List */}
          <div className="flex-1 overflow-y-auto p-5 divide-y divide-border space-y-4">
            {items.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
                <div className="w-16 h-16 rounded-full bg-primary-soft flex items-center justify-center text-primary">
                  <Heart size={32} />
                </div>
                <h3 className="text-base font-bold text-navy">Your wishlist is empty</h3>
                <p className="text-xs text-muted max-w-xs">
                  Save laptops or customized machine specs you want to keep an eye on while browsing.
                </p>
                <Button 
                  variant="primary" 
                  size="md" 
                  className="mt-2"
                  onClick={() => setIsOpen(false)}
                >
                  Explore Laptops
                </Button>
              </div>
            ) : (
              items.map((product) => (
                <div key={product.id} className="pt-4 first:pt-0 flex gap-4">
                  {/* Thumbnail */}
                  <div className="relative w-20 h-20 rounded-lg bg-muted-bg border border-border overflow-hidden flex-shrink-0">
                    <Image
                      src={product.image_url}
                      alt={product.title}
                      fill
                      className="object-cover"
                    />
                  </div>

                  {/* Details */}
                  <div className="flex-1 min-w-0 space-y-1">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="text-xs font-bold text-navy line-clamp-2">{product.title}</h4>
                      <button
                        onClick={() => removeItem(product.id)}
                        className="text-muted hover:text-error transition-colors p-1"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>

                    <p className="text-xs font-bold text-primary">
                      {formatPrice(product.base_price)}
                    </p>

                    <div className="flex items-center gap-2 pt-2">
                      <Button
                        variant="primary"
                        size="sm"
                        className="text-[11px] h-8 px-2.5"
                        onClick={() => {
                          addItem({
                            productId: product.id,
                            productTitle: product.title,
                            unitPrice: product.base_price,
                            quantity: 1,
                            imageUrl: product.image_url,
                          })
                        }}
                      >
                        <ShoppingBag size={12} className="mr-1" />
                        Add to Cart
                      </Button>

                      <Button
                        variant="outline"
                        size="sm"
                        className="text-[11px] h-8 px-2"
                        onClick={() => {
                          setIsOpen(false)
                          openConfigurator(product)
                        }}
                      >
                        <SlidersHorizontal size={12} className="mr-1" />
                        Configure
                      </Button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          {items.length > 0 && (
            <div className="p-4 border-t border-border bg-background">
              <Button
                variant="outline"
                size="md"
                className="w-full justify-center"
                onClick={() => setIsOpen(false)}
              >
                Continue Shopping
              </Button>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}
