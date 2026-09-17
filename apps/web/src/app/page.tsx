'use client'

import React, { useState, useEffect } from 'react'
import { Product } from '@/types'
import { StoreHeader } from '@/components/layout/StoreHeader'
import { CategoryNav } from '@/components/layout/CategoryNav'
import { HeroBanner } from '@/components/homepage/HeroBanner'
import { CategoryGrid } from '@/components/homepage/CategoryGrid'
import { FlashDeals } from '@/components/homepage/FlashDeals'
import { FeaturedProducts } from '@/components/homepage/FeaturedProducts'
import { BuilderPromotion } from '@/components/homepage/BuilderPromotion'
import { AccessoriesSection } from '@/components/homepage/AccessoriesSection'
import { TrustSection } from '@/components/homepage/TrustSection'
import { ReviewsSection } from '@/components/homepage/ReviewsSection'
import { NewsletterSection } from '@/components/homepage/NewsletterSection'
import { api } from '@/lib/api'

const INITIAL_PRODUCTS: Product[] = [
  {
    id: 'prod-titanforge-predator-16',
    title: 'TitanForge Predator 16 Pro Gaming Laptop',
    slug: 'titanforge-predator-16-pro',
    description: 'Crafted for intense esports and compute workloads. Features state-of-the-art dual liquid-metal cooling and per-key RGB lighting.',
    short_description: 'Intel Core i9 14th Gen, RTX 4070/4080, 240Hz QHD+ Display',
    category_id: 'cat-gaming',
    brand_id: 'brand-titanforge',
    base_price: 1450000,
    original_price: 1680000,
    discount_percentage: 14,
    is_featured: true,
    is_flash_deal: true,
    is_best_seller: true,
    is_customizable: true,
    stock: 18,
    rating: 4.9,
    review_count: 48,
    image_url: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    specs: {
      processor: 'Intel Core i9-14900HX',
      ram: '32GB DDR5 5600MHz',
      storage: '1TB Gen4 NVMe SSD',
      gpu: 'NVIDIA GeForce RTX 4070 8GB',
      display: '16.0" QHD+ 240Hz 500-nit',
    },
  },
  {
    id: 'prod-aerocraft-studiomaster-16',
    title: 'AeroCraft StudioMaster 16 OLED Creator Laptop',
    slug: 'aerocraft-studiomaster-16-oled',
    description: 'Engineered for designers, video editors, and 3D animators with calibrated Delta E < 1 OLED display.',
    short_description: 'AMD Ryzen 9 7945HX, RTX 4060/4070, 3.2K 120Hz OLED',
    category_id: 'cat-professional',
    brand_id: 'brand-aerocraft',
    base_price: 1280000,
    original_price: 1420000,
    discount_percentage: 10,
    is_featured: true,
    is_flash_deal: false,
    is_best_seller: true,
    is_customizable: true,
    stock: 14,
    rating: 4.8,
    review_count: 36,
    image_url: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    specs: {
      processor: 'AMD Ryzen 9 7945HX',
      ram: '32GB DDR5 Dual Channel',
      storage: '1TB Pro PCIe 4.0 SSD',
      gpu: 'RTX 4060 Studio Edition',
      display: '16.0" 3.2K OLED 120Hz 100% DCI-P3',
    },
  },
  {
    id: 'prod-zenith-campusbook-14',
    title: 'Zenith CampusBook Slim 14 Student Edition',
    slug: 'zenith-campusbook-slim-14',
    description: 'Ultraportable featherweight laptop designed for students and mobile productivity with 14-hour battery.',
    short_description: 'Intel Core i5 13th Gen, 16GB RAM, 512GB NVMe SSD, 14" FHD+',
    category_id: 'cat-student',
    brand_id: 'brand-zenith',
    base_price: 540000,
    original_price: 620000,
    discount_percentage: 13,
    is_featured: true,
    is_flash_deal: true,
    is_best_seller: false,
    is_customizable: true,
    stock: 25,
    rating: 4.7,
    review_count: 62,
    image_url: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    specs: {
      processor: 'Intel Core i5-13420H',
      ram: '16GB LPDDR5',
      storage: '512GB PCIe NVMe SSD',
      gpu: 'Intel Iris Xe Graphics',
      display: '14.0" FHD+ IPS Anti-Glare',
    },
  },
  {
    id: 'prod-aerocraft-real-air-15',
    title: 'AeroCraft Real Air 15 Unibody Ultrabook',
    slug: 'aerocraft-real-air-15',
    description: 'Aerospace-grade aluminium unibody with Liquid Retina style display and 18-hour battery.',
    short_description: 'Intel Core Ultra 7 155H, 32GB RAM, 1TB SSD, 18hr Battery',
    category_id: 'cat-macbooks',
    brand_id: 'brand-aerocraft',
    base_price: 980000,
    original_price: 1150000,
    discount_percentage: 15,
    is_featured: true,
    is_flash_deal: false,
    is_best_seller: true,
    is_customizable: true,
    stock: 19,
    rating: 4.9,
    review_count: 89,
    image_url: 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    specs: {
      processor: 'Intel Core Ultra 7 with NPU AI',
      ram: '32GB LPDDR5X 7467MHz',
      storage: '1TB Gen4 SSD',
      gpu: 'Intel Arc Graphics',
      display: '15.3" 2.8K 120Hz IPS',
    },
  },
  {
    id: 'prod-novablade-fusion-15',
    title: 'NovaBlade Fusion 15 Everyday Workhorse',
    slug: 'novablade-fusion-15',
    description: 'Everyday high-productivity laptop with AMD Ryzen 7, numeric keypad, and long battery life.',
    short_description: 'AMD Ryzen 7 7730U, 16GB RAM, 1TB SSD, 15.6" IPS Display',
    category_id: 'cat-everyday',
    brand_id: 'brand-novablade',
    base_price: 620000,
    original_price: 700000,
    discount_percentage: 11,
    is_featured: false,
    is_flash_deal: true,
    is_best_seller: false,
    is_customizable: true,
    stock: 30,
    rating: 4.6,
    review_count: 27,
    image_url: 'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    specs: {
      processor: 'AMD Ryzen 7 7730U',
      ram: '16GB DDR4 3200MHz',
      storage: '1TB NVMe SSD',
      gpu: 'AMD Radeon Graphics',
      display: '15.6" FHD IPS Anti-Glare',
    },
  },
]

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>(INITIAL_PRODUCTS)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  useEffect(() => {
    // Fetch latest products from backend
    api.getProducts()
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setProducts(data)
        }
      })
      .catch(() => {
        // Quietly fallback to initial products
      })
  }, [])

  const handleCategorySelect = (categoryId: string) => {
    setSelectedCategory(categoryId)
    const element = document.getElementById('products-section')
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <div className="flex flex-col min-h-screen">
      {/* 1. Main Header */}
      <StoreHeader onSearchChange={setSearchQuery} />

      {/* 2. Category Navigation */}
      <CategoryNav
        activeCategory={selectedCategory}
        onSelectCategory={handleCategorySelect}
      />

      {/* 3. Promotional Hero Banner */}
      <HeroBanner />

      {/* 4. Shop by Category Cards */}
      <CategoryGrid onSelectCategory={handleCategorySelect} />

      {/* 5. Flash Deals with Countdown */}
      <FlashDeals products={products} />

      {/* 6. Featured Laptops & Workstations */}
      <FeaturedProducts
        products={products}
        selectedCategory={selectedCategory}
        searchQuery={searchQuery}
      />

      {/* 7. Dedicated Custom Builder Promotion Section */}
      <BuilderPromotion sampleProduct={products[0]} />

      {/* 8. Popular Accessories */}
      <AccessoriesSection />

      {/* 9. Trust & Peace of Mind Section */}
      <TrustSection />

      {/* 10. Customer Reviews & Ratings */}
      <ReviewsSection />

      {/* 11. Newsletter & Promo Code Section */}
      <NewsletterSection />
    </div>
  )
}
