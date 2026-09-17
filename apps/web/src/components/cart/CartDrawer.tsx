'use client'

import React from 'react'
import Image from 'next/image'
import { X, Trash2, ShoppingBag, ArrowRight, Plus, Minus, Cpu, HardDrive, ShieldCheck } from 'lucide-react'
import { useCartStore } from '@/stores/cartStore'
import { formatPrice } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'

export const CartDrawer: React.FC = () => {
  const { items, isOpen, setIsOpen, setIsCheckoutOpen, removeItem, updateQuantity, getSubtotal } = useCartStore()
  const subtotal = getSubtotal()

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-navy/60 backdrop-blur-sm transition-opacity animate-fade-in"
        onClick={() => setIsOpen(false)}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col">
          {/* Header */}
          <div className="p-5 border-b border-border flex items-center justify-between bg-primary-soft">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-primary-light flex items-center justify-center text-primary">
                <ShoppingBag size={20} />
              </div>
              <div>
                <h2 className="text-base font-bold text-navy">Your Shopping Cart</h2>
                <p className="text-xs text-muted">
                  {items.length} {items.length === 1 ? 'item' : 'items'} in your cart
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

          {/* Cart Items List */}
          <div className="flex-1 overflow-y-auto p-5 divide-y divide-border space-y-4">
            {items.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
                <div className="w-16 h-16 rounded-full bg-primary-soft flex items-center justify-center text-primary">
                  <ShoppingBag size={32} />
                </div>
                <h3 className="text-base font-bold text-navy">Your cart is empty</h3>
                <p className="text-xs text-muted max-w-xs">
                  Browse our high-performance laptops or design a custom machine tailored to your exact needs.
                </p>
                <Button 
                  variant="primary" 
                  size="md" 
                  className="mt-2"
                  onClick={() => setIsOpen(false)}
                >
                  Start Shopping
                </Button>
              </div>
            ) : (
              items.map((item) => (
                <div key={item.id} className="pt-4 first:pt-0 flex gap-4">
                  {/* Thumbnail */}
                  <div className="relative w-20 h-20 rounded-lg bg-muted-bg border border-border overflow-hidden flex-shrink-0">
                    <Image
                      src={item.imageUrl}
                      alt={item.productTitle}
                      fill
                      className="object-cover"
                    />
                  </div>

                  {/* Details */}
                  <div className="flex-1 min-w-0 space-y-1">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="text-sm font-bold text-navy line-clamp-1">{item.productTitle}</h4>
                      <button
                        onClick={() => removeItem(item.id)}
                        className="text-muted hover:text-error transition-colors p-1"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>

                    {/* Configuration Summary Badges */}
                    {item.configurationSummary && (
                      <div className="flex flex-wrap gap-1 py-1">
                        {item.configurationSummary.color && (
                          <Badge variant="outline" size="sm">
                            {item.configurationSummary.color}
                          </Badge>
                        )}
                        {item.configurationSummary.ram && (
                          <Badge variant="outline" size="sm">
                            <Cpu size={10} className="mr-1 inline" />
                            {item.configurationSummary.ram}
                          </Badge>
                        )}
                        {item.configurationSummary.storage && (
                          <Badge variant="outline" size="sm">
                            <HardDrive size={10} className="mr-1 inline" />
                            {item.configurationSummary.storage}
                          </Badge>
                        )}
                        {item.configurationSummary.hasArtwork && (
                          <Badge variant="primary" size="sm">
                            Custom Artwork
                          </Badge>
                        )}
                      </div>
                    )}

                    {/* Price & Quantity Controls */}
                    <div className="flex items-center justify-between pt-2">
                      <span className="text-sm font-bold text-navy">
                        {formatPrice(item.totalPrice)}
                      </span>
                      <div className="flex items-center border border-border rounded-lg bg-white overflow-hidden">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="px-2 py-1 text-muted hover:bg-primary-soft hover:text-navy transition-colors"
                        >
                          <Minus size={14} />
                        </button>
                        <span className="px-2 text-xs font-bold text-navy min-w-6 text-center">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="px-2 py-1 text-muted hover:bg-primary-soft hover:text-navy transition-colors"
                        >
                          <Plus size={14} />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer Checkout Summary */}
          {items.length > 0 && (
            <div className="p-5 border-t border-border bg-background space-y-4">
              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between text-muted">
                  <span>Subtotal</span>
                  <span className="font-semibold text-foreground">{formatPrice(subtotal)}</span>
                </div>
                <div className="flex justify-between text-muted">
                  <span>Estimated Delivery</span>
                  <span className="font-semibold text-success">FREE</span>
                </div>
                <div className="flex justify-between text-base font-extrabold text-navy pt-2 border-t border-border">
                  <span>Total</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
              </div>

              <div className="flex items-center gap-2 text-[11px] text-muted bg-white p-2 rounded-lg border border-border">
                <ShieldCheck size={16} className="text-success flex-shrink-0" />
                <span>Paystack, Flutterwave & OPay SSL Encrypted Checkout</span>
              </div>

              <Button
                variant="primary"
                size="lg"
                className="w-full justify-between"
                onClick={() => {
                  setIsOpen(false)
                  setIsCheckoutOpen(true)
                }}
              >
                <span>PROCEED TO CHECKOUT</span>
                <ArrowRight size={18} />
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
