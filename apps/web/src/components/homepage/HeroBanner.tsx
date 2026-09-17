'use client'

import React from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Sparkles, ArrowRight, SlidersHorizontal, ShieldCheck, Zap } from 'lucide-react'

export const HeroBanner: React.FC = () => {
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
    <div className="relative bg-gradient-to-br from-primary-soft via-white to-background border-b border-border overflow-hidden">
      
      {/* Subtle Background Glow & Pattern */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-10 left-10 w-80 h-80 bg-accent/10 rounded-full blur-2xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-16">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Hero Content */}
          <div className="lg:col-span-7 space-y-6 text-left">
            
            {/* Promo Tag */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-primary/20 shadow-sm">
              <Badge variant="discount" size="sm">NEW SEASON SALE</Badge>
              <span className="text-xs font-bold text-navy flex items-center gap-1">
                <Sparkles size={13} className="text-primary" />
                Up to 20% Off + Free Laser Engraving
              </span>
            </div>

            {/* Headline */}
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-navy leading-[1.15] tracking-tight font-display">
              Find the right laptop for your next move.
            </h1>

            {/* Supporting Copy */}
            <p className="text-base sm:text-lg text-muted max-w-xl leading-relaxed">
              Shop ready-to-buy laptops or build one with the exact performance, DDR5 RAM, NVMe storage, color finish, and custom artwork you need.
            </p>

            {/* Action CTAs */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link href="#products-section">
                <Button variant="primary" size="lg" className="shadow-lg hover:shadow-xl gap-2 font-bold">
                  <span>SHOP READY LAPTOPS</span>
                  <ArrowRight size={18} />
                </Button>
              </Link>

              <Button 
                variant="navy" 
                size="lg" 
                className="gap-2 font-bold border border-navy-light shadow-md hover:scale-[1.02] transition-transform"
                onClick={handleStartCustomBuild}
              >
                <SlidersHorizontal size={18} className="text-primary-sky" />
                <span>BUILD YOUR LAPTOP</span>
              </Button>
            </div>

            {/* Trust Signal Highlights */}
            <div className="pt-4 flex flex-wrap items-center gap-6 text-xs text-muted font-medium border-t border-border/80">
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 rounded-full bg-success-light flex items-center justify-center text-success">
                  <ShieldCheck size={14} />
                </div>
                <span className="text-foreground">Official Warranty</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 rounded-full bg-primary-light flex items-center justify-center text-primary">
                  <Zap size={14} />
                </div>
                <span className="text-foreground">Instant Real-time Pricing</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-navy">⭐ 4.9/5</span>
                <span>(2,400+ Verified Buyers)</span>
              </div>
            </div>

          </div>

          {/* Right Hero Product Card / Showcase */}
          <div className="lg:col-span-5 relative">
            <div className="relative rounded-2xl bg-white border border-border shadow-card p-6 overflow-hidden group">
              
              {/* Floating Badge */}
              <div className="absolute top-4 left-4 z-10 flex flex-col gap-1.5">
                <Badge variant="navy" size="sm">FEATURED FLAGSHIP</Badge>
                <Badge variant="discount" size="sm">Save ₦230,000</Badge>
              </div>

              {/* Product Image */}
              <div className="relative h-64 sm:h-72 w-full my-2">
                <Image
                  src="https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80"
                  alt="TitanForge Predator 16 Pro Gaming Laptop"
                  fill
                  className="object-contain group-hover:scale-105 transition-transform duration-300"
                  priority
                />
              </div>

              {/* Product Metadata */}
              <div className="space-y-2 pt-2 border-t border-border">
                <div className="flex items-center justify-between text-xs text-muted">
                  <span className="font-semibold text-primary">TitanForge Series</span>
                  <span>In Stock (18 units)</span>
                </div>
                <h3 className="text-base font-bold text-navy line-clamp-1">
                  TitanForge Predator 16 Pro Gaming Laptop
                </h3>
                <p className="text-xs text-muted">
                  Intel Core i9-14900HX • RTX 4070 • 32GB RAM • 1TB NVMe
                </p>

                <div className="flex items-center justify-between pt-2">
                  <div>
                    <span className="text-xs text-muted line-through block">₦1,680,000</span>
                    <span className="text-xl font-extrabold text-navy">₦1,450,000</span>
                  </div>
                  <Link href="#builder-section">
                    <Button variant="secondary" size="sm" className="font-bold">
                      Customize Now
                    </Button>
                  </Link>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
