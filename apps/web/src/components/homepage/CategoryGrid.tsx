'use client'

import React from 'react'
import Image from 'next/image'
import { ArrowRight } from 'lucide-react'

interface CategoryGridProps {
  onSelectCategory?: (categoryId: string) => void
}

const CATEGORIES = [
  {
    id: 'cat-gaming',
    name: 'Gaming Laptops',
    description: 'High-refresh QHD displays, RTX GPUs, liquid cooling.',
    priceStart: '₦1,450,000',
    itemCount: '12 Models',
    image: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80',
    badge: 'Popular'
  },
  {
    id: 'cat-professional',
    name: 'Professional & Creator',
    description: 'Calibrated 3.2K OLED, Ryzen 9 / Intel i9, long battery.',
    priceStart: '₦1,280,000',
    itemCount: '8 Models',
    image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80',
    badge: 'Creator Pick'
  },
  {
    id: 'cat-student',
    name: 'Student Laptops',
    description: 'Lightweight, durable, 14-hour battery for campus.',
    priceStart: '₦540,000',
    itemCount: '15 Models',
    image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80',
    badge: 'Best Value'
  },
  {
    id: 'cat-everyday',
    name: 'Everyday Slim Laptops',
    description: 'Crisp screens, ergonomic keyboard, home and office.',
    priceStart: '₦620,000',
    itemCount: '10 Models',
    image: 'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=600&q=80',
    badge: null
  },
  {
    id: 'cat-macbooks',
    name: 'MacBook Tier Ultrabooks',
    description: 'CNC Aluminium unibody, edge-to-edge Retina displays.',
    priceStart: '₦980,000',
    itemCount: '6 Models',
    image: 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=600&q=80',
    badge: 'Premium'
  },
  {
    id: 'cat-accessories',
    name: 'Accessories & Docks',
    description: '100W GaN chargers, Thunderbolt 4 docks, cooling stands.',
    priceStart: '₦45,000',
    itemCount: '24 Items',
    image: 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80',
    badge: null
  }
]

export const CategoryGrid: React.FC<CategoryGridProps> = ({ onSelectCategory }) => {
  return (
    <section className="py-12 bg-white border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8">
          <div>
            <div className="text-xs font-bold text-primary tracking-wider uppercase mb-1">
              Explore Our Collection
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-navy font-display tracking-tight">
              Shop by Category
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-muted mt-2 sm:mt-0">
            Find the right system tailored for your specific workflow
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {CATEGORIES.map((cat) => (
            <div
              key={cat.id}
              onClick={() => onSelectCategory && onSelectCategory(cat.id)}
              className="group relative bg-background rounded-card border border-border p-5 hover:border-primary hover:shadow-card-hover transition-all duration-200 cursor-pointer overflow-hidden flex flex-col justify-between"
            >
              {cat.badge && (
                <span className="absolute top-4 right-4 px-2 py-0.5 text-[10px] font-extrabold uppercase bg-primary text-white rounded-md shadow-sm z-10">
                  {cat.badge}
                </span>
              )}

              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="space-y-1">
                  <h3 className="text-base font-bold text-navy group-hover:text-primary transition-colors">
                    {cat.name}
                  </h3>
                  <p className="text-xs text-muted line-clamp-2 max-w-[200px]">
                    {cat.description}
                  </p>
                </div>

                <div className="relative w-24 h-24 rounded-lg bg-white p-1 border border-border flex-shrink-0 group-hover:scale-105 transition-transform">
                  <Image
                    src={cat.image}
                    alt={cat.name}
                    fill
                    className="object-cover rounded-md"
                  />
                </div>
              </div>

              <div className="pt-3 border-t border-border flex items-center justify-between text-xs">
                <div>
                  <span className="text-[11px] text-muted block">Starting from</span>
                  <span className="font-extrabold text-navy">{cat.priceStart}</span>
                </div>
                <div className="flex items-center gap-1 font-bold text-primary group-hover:translate-x-1 transition-transform">
                  <span>Explore</span>
                  <ArrowRight size={14} />
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  )
}
