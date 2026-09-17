'use client'

import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import { Zap, Clock, ArrowRight, SlidersHorizontal, ShoppingBag } from 'lucide-react'
import { Product } from '@/types'
import { formatPrice } from '@/lib/utils'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { useCartStore } from '@/stores/cartStore'
import { useConfiguratorStore } from '@/stores/configuratorStore'

interface FlashDealsProps {
  products: Product[]
}

export const FlashDeals: React.FC<FlashDealsProps> = ({ products }) => {
  const { addItem } = useCartStore()
  const { openConfigurator } = useConfiguratorStore()

  // Countdown timer state
  const [timeLeft, setTimeLeft] = useState({ hours: 7, minutes: 34, seconds: 18 })

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev.seconds > 0) return { ...prev, seconds: prev.seconds - 1 }
        if (prev.minutes > 0) return { ...prev, minutes: 59, seconds: 59 }
        if (prev.hours > 0) return { hours: prev.hours - 1, minutes: 59, seconds: 59 }
        return { hours: 12, minutes: 0, seconds: 0 }
      })
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const flashProducts = products.filter((p) => p.is_flash_deal || (p.discount_percentage && p.discount_percentage > 10)).slice(0, 3)

  if (flashProducts.length === 0) return null

  return (
    <section className="py-10 bg-primary-soft/50 border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header with Countdown */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 bg-white p-4 sm:p-5 rounded-card border border-border shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-discount text-white flex items-center justify-center shadow-md animate-pulse">
              <Zap size={22} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl sm:text-2xl font-black text-navy font-display tracking-tight">
                  Flash Deals
                </h2>
                <Badge variant="discount" size="sm">LIMITED TIME</Badge>
              </div>
              <p className="text-xs text-muted">Special discounted prices on high-spec models</p>
            </div>
          </div>

          {/* Countdown Clock */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 text-xs font-bold text-navy mr-1">
              <Clock size={16} className="text-discount" />
              <span>Ends in:</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="px-2.5 py-1 bg-navy text-white text-xs font-bold rounded-md">
                {String(timeLeft.hours).padStart(2, '0')}h
              </span>
              <span className="font-bold text-navy">:</span>
              <span className="px-2.5 py-1 bg-navy text-white text-xs font-bold rounded-md">
                {String(timeLeft.minutes).padStart(2, '0')}m
              </span>
              <span className="font-bold text-navy">:</span>
              <span className="px-2.5 py-1 bg-discount text-white text-xs font-bold rounded-md">
                {String(timeLeft.seconds).padStart(2, '0')}s
              </span>
            </div>
          </div>
        </div>

        {/* Flash Deals Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {flashProducts.map((product, idx) => {
            const soldPercent = idx === 0 ? 84 : idx === 1 ? 67 : 91
            const unitsLeft = idx === 0 ? 3 : idx === 1 ? 5 : 2

            return (
              <div
                key={product.id}
                className="bg-white rounded-card border border-border p-5 shadow-sm hover:shadow-card-hover transition-all flex flex-col justify-between"
              >
                <div className="relative">
                  <div className="flex justify-between items-center mb-2">
                    <Badge variant="discount" size="sm">-{product.discount_percentage || 15}% OFF</Badge>
                    <span className="text-xs font-bold text-discount">{unitsLeft} Units Left!</span>
                  </div>

                  <div className="relative h-44 w-full my-2 bg-background rounded-lg p-2">
                    <Image
                      src={product.image_url}
                      alt={product.title}
                      fill
                      className="object-contain hover:scale-105 transition-transform"
                    />
                  </div>
                </div>

                <div className="space-y-2 mt-2">
                  <h3 className="text-sm font-bold text-navy line-clamp-1">{product.title}</h3>
                  <p className="text-xs text-muted line-clamp-1">{product.short_description}</p>

                  <div className="flex items-baseline gap-2 pt-1">
                    <span className="text-lg font-extrabold text-navy">{formatPrice(product.base_price)}</span>
                    {product.original_price && (
                      <span className="text-xs text-muted line-through">{formatPrice(product.original_price)}</span>
                    )}
                  </div>

                  {/* Stock Progress Bar */}
                  <div className="space-y-1 pt-1">
                    <div className="w-full bg-border rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-warning to-discount h-2 rounded-full"
                        style={{ width: `${soldPercent}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-[11px] text-muted">
                      <span>Claimed: {soldPercent}%</span>
                      <span className="font-semibold text-navy">{unitsLeft} in stock</span>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="grid grid-cols-2 gap-2 pt-3">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() =>
                        addItem({
                          productId: product.id,
                          productTitle: product.title,
                          imageUrl: product.image_url,
                          quantity: 1,
                          unitPrice: product.base_price,
                        })
                      }
                      className="text-xs"
                    >
                      <ShoppingBag size={14} />
                      <span>Buy Now</span>
                    </Button>

                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => openConfigurator(product)}
                      className="text-xs font-bold"
                    >
                      <SlidersHorizontal size={14} />
                      <span>Customize</span>
                    </Button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

      </div>
    </section>
  )
}
