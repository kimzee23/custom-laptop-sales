'use client'

import React, { useState } from 'react'
import { Product } from '@/types'
import { ProductCard } from '@/components/product/ProductCard'
import { SlidersHorizontal, Layers, Check } from 'lucide-react'

interface FeaturedProductsProps {
  products: Product[]
  selectedCategory?: string
  searchQuery?: string
}

const TABS = [
  { id: 'all', label: 'All Laptops' },
  { id: 'cat-gaming', label: 'Gaming' },
  { id: 'cat-professional', label: 'Creator & Pro' },
  { id: 'cat-student', label: 'Student' },
  { id: 'cat-everyday', label: 'Everyday' },
  { id: 'cat-macbooks', label: 'MacBook Tier' },
]

export const FeaturedProducts: React.FC<FeaturedProductsProps> = ({
  products,
  selectedCategory = 'all',
  searchQuery = '',
}) => {
  const [activeTab, setActiveTab] = useState(selectedCategory)
  const [sortBy, setSortBy] = useState<'featured' | 'price_asc' | 'price_desc' | 'rating'>('featured')

  // Filter products by category & search query
  let filtered = products.filter((p) => {
    const matchesCategory = activeTab === 'all' || p.category_id === activeTab
    const matchesSearch =
      !searchQuery ||
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.short_description && p.short_description.toLowerCase().includes(searchQuery.toLowerCase()))
    return matchesCategory && matchesSearch
  })

  // Sort
  if (sortBy === 'price_asc') {
    filtered = [...filtered].sort((a, b) => a.base_price - b.base_price)
  } else if (sortBy === 'price_desc') {
    filtered = [...filtered].sort((a, b) => b.base_price - a.base_price)
  } else if (sortBy === 'rating') {
    filtered = [...filtered].sort((a, b) => b.rating - a.rating)
  }

  return (
    <section id="products-section" className="py-12 bg-background border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header & Tabs */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
          <div>
            <div className="text-xs font-bold text-primary tracking-wider uppercase mb-1">
              Top Rated Hardware
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-navy font-display tracking-tight">
              Featured Laptops & Workstations
            </h2>
          </div>

          {/* Sorting Dropdown */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted font-medium">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="h-9 px-3 text-xs font-semibold text-navy bg-white border border-border rounded-lg focus:outline-none focus:border-primary shadow-sm"
            >
              <option value="featured">Featured / Newest</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="rating">Highest Rated</option>
            </select>
          </div>
        </div>

        {/* Filter Category Pills */}
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-4 mb-6">
          {TABS.map((tab) => {
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-full text-xs font-bold transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-primary text-white shadow-sm'
                    : 'bg-white text-navy border border-border hover:border-primary hover:text-primary'
                }`}
              >
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Product Cards Grid */}
        {filtered.length === 0 ? (
          <div className="bg-white rounded-card border border-border p-12 text-center space-y-3">
            <Layers size={36} className="mx-auto text-muted" />
            <h3 className="text-base font-bold text-navy">No products match your criteria</h3>
            <p className="text-xs text-muted max-w-sm mx-auto">
              Try adjusting your search keywords or switching category filters.
            </p>
            <button
              onClick={() => {
                setActiveTab('all')
              }}
              className="text-xs font-bold text-primary hover:underline"
            >
              View All Products
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filtered.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

      </div>
    </section>
  )
}
