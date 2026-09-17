'use client'

import React from 'react'
import Image from 'next/image'
import { Plus, ShoppingBag, Check } from 'lucide-react'
import { formatPrice } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { useCartStore } from '@/stores/cartStore'

const ACCESSORIES = [
  {
    id: 'acc-dock-thunderbolt',
    title: 'AeroCraft 14-in-1 Dual 4K Thunderbolt Dock',
    price: 145000,
    originalPrice: 180000,
    image: 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=400&q=80',
    tag: '100W PD Charge',
  },
  {
    id: 'acc-gan-charger',
    title: '140W Dual USB-C GaN Ultra Fast Charger',
    price: 48000,
    originalPrice: 60000,
    image: 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=400&q=80',
    tag: 'GaN III Tech',
  },
  {
    id: 'acc-cooling-stand',
    title: 'Ergonomic Aluminium RGB Laptop Cooling Stand',
    price: 35000,
    originalPrice: 42000,
    image: 'https://images.unsplash.com/photo-1616440347437-b1c73416efc2?auto=format&fit=crop&w=400&q=80',
    tag: 'Silent Fans',
  },
  {
    id: 'acc-sleeve-leather',
    title: 'Waterproof Felt & Leather Protective Laptop Sleeve',
    price: 24000,
    originalPrice: 30000,
    image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=400&q=80',
    tag: 'Drop Proof',
  },
]

export const AccessoriesSection: React.FC = () => {
  const { addItem } = useCartStore()

  return (
    <section className="py-12 bg-white border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8">
          <div>
            <div className="text-xs font-bold text-primary tracking-wider uppercase mb-1">
              Add to Your Setup
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-navy font-display tracking-tight">
              Popular Laptop Accessories
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-muted mt-2 sm:mt-0">
            Docks, chargers, and protection tested for maximum compatibility
          </p>
        </div>

        {/* Accessories Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {ACCESSORIES.map((item) => (
            <div
              key={item.id}
              className="bg-background rounded-card border border-border p-4 hover:border-primary hover:shadow-card transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                <div className="relative h-40 w-full rounded-lg bg-white p-2 mb-3">
                  <Image
                    src={item.image}
                    alt={item.title}
                    fill
                    className="object-contain"
                  />
                  <span className="absolute top-2 left-2 px-2 py-0.5 text-[10px] font-bold bg-navy text-white rounded">
                    {item.tag}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-navy line-clamp-2 mb-2">
                  {item.title}
                </h4>
              </div>

              <div className="pt-3 border-t border-border flex items-center justify-between">
                <div>
                  <span className="text-sm font-extrabold text-navy block">
                    {formatPrice(item.price)}
                  </span>
                  <span className="text-[11px] text-muted line-through">
                    {formatPrice(item.originalPrice)}
                  </span>
                </div>

                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() =>
                    addItem({
                      productId: item.id,
                      productTitle: item.title,
                      imageUrl: item.image,
                      quantity: 1,
                      unitPrice: item.price,
                    })
                  }
                  className="px-2.5 h-8 gap-1 text-xs"
                >
                  <Plus size={14} />
                  <span>Add</span>
                </Button>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  )
}
