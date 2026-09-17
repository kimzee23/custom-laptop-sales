'use client'

import React from 'react'
import Link from 'next/link'
import { 
  Laptop, 
  Gamepad2, 
  Briefcase, 
  GraduationCap, 
  Sparkles, 
  Headphones, 
  Tag, 
  SlidersHorizontal,
  Layers
} from 'lucide-react'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { Badge } from '@/components/ui/Badge'

interface CategoryNavProps {
  activeCategory?: string
  onSelectCategory?: (categoryId: string) => void
}

const NAV_ITEMS = [
  { id: 'all', name: 'All Laptops', icon: Layers },
  { id: 'cat-gaming', name: 'Gaming Laptops', icon: Gamepad2, badge: 'Hot' },
  { id: 'cat-professional', name: 'Business & Creator', icon: Briefcase },
  { id: 'cat-student', name: 'Student Laptops', icon: GraduationCap },
  { id: 'cat-everyday', name: 'Everyday Slim', icon: Laptop },
  { id: 'cat-macbooks', name: 'MacBook Tier', icon: Sparkles },
  { id: 'cat-accessories', name: 'Accessories', icon: Headphones },
  { id: 'deals', name: 'Deals & Clearance', icon: Tag, isDiscount: true },
]

export const CategoryNav: React.FC<CategoryNavProps> = ({ activeCategory = 'all', onSelectCategory }) => {
  const { openConfigurator } = useConfiguratorStore()

  const handleStartCustomBuild = () => {
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
    <nav className="bg-primary-soft border-b border-border text-navy select-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between overflow-x-auto no-scrollbar py-2 gap-1 sm:gap-2">
          
          <div className="flex items-center gap-1 sm:gap-2 min-w-max">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon
              const isActive = activeCategory === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => onSelectCategory && onSelectCategory(item.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-primary text-white shadow-sm'
                      : 'text-navy hover:bg-white hover:text-primary'
                  } ${item.isDiscount ? 'text-discount hover:text-discount' : ''}`}
                >
                  <Icon size={15} className={isActive ? 'text-white' : item.isDiscount ? 'text-discount' : 'text-primary'} />
                  <span>{item.name}</span>
                  {item.badge && !isActive && (
                    <span className="px-1.5 py-0.2 text-[10px] font-extrabold bg-discount text-white rounded-full">
                      {item.badge}
                    </span>
                  )}
                </button>
              )
            })}
          </div>

          {/* Differentiating Configurator Highlight CTA */}
          <div className="pl-4 min-w-max">
            <button
              onClick={handleStartCustomBuild}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold bg-navy text-white hover:bg-navy-light shadow-sm transition-all group"
            >
              <SlidersHorizontal size={14} className="text-primary-sky group-hover:rotate-45 transition-transform" />
              <span>BUILD YOUR LAPTOP</span>
              <span className="w-2 h-2 rounded-full bg-primary-sky animate-ping" />
            </button>
          </div>

        </div>
      </div>
    </nav>
  )
}
