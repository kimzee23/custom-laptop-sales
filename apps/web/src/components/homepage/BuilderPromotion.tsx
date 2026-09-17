'use client'

import React from 'react'
import Image from 'next/image'
import { SlidersHorizontal, Sparkles, CheckCircle2, ArrowRight, Cpu, Palette, HardDrive, Shield } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { Product } from '@/types'

interface BuilderPromotionProps {
  sampleProduct?: Product
}

export const BuilderPromotion: React.FC<BuilderPromotionProps> = ({ sampleProduct }) => {
  const { openConfigurator } = useConfiguratorStore()

  const handleStartBuilding = () => {
    if (sampleProduct) {
      openConfigurator(sampleProduct)
    } else {
      // Default fallback product
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
  }

  return (
    <section id="builder-section" className="py-16 bg-gradient-to-r from-navy via-navy-light to-navy text-white relative overflow-hidden border-b border-border">
      
      {/* Background Decorative Rings */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-primary-sky/15 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          
          {/* Left Content */}
          <div className="lg:col-span-7 space-y-6">
            
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-navy-light border border-primary/40 text-primary-sky text-xs font-bold shadow-sm">
              <Sparkles size={14} className="text-primary-sky" />
              <span>THE ULTIMATE LAPTOP CONFIGURATOR</span>
            </div>

            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight font-display text-white leading-tight">
              Build your machine to match your exact standards.
            </h2>

            <p className="text-base sm:text-lg text-muted-light max-w-xl leading-relaxed">
              Choose your performance, RAM, storage, GPU, chassis finish, and upload custom lid artwork. Watch your laptop update visually with instant authoritative pricing.
            </p>

            {/* Feature Checklist */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div className="flex items-center gap-2.5 text-xs text-white">
                <Palette size={16} className="text-primary-sky flex-shrink-0" />
                <span>5 Metallic & Ceramic Chassis Colors</span>
              </div>
              <div className="flex items-center gap-2.5 text-xs text-white">
                <Cpu size={16} className="text-primary-sky flex-shrink-0" />
                <span>DDR5 RAM Configurable to 64GB</span>
              </div>
              <div className="flex items-center gap-2.5 text-xs text-white">
                <HardDrive size={16} className="text-primary-sky flex-shrink-0" />
                <span>PCIe 4.0 NVMe SSD Up to 4TB</span>
              </div>
              <div className="flex items-center gap-2.5 text-xs text-white">
                <Sparkles size={16} className="text-primary-sky flex-shrink-0" />
                <span>Custom UV Artwork & Laser Engraving</span>
              </div>
            </div>

            {/* Launch CTA */}
            <div className="pt-4 flex flex-wrap items-center gap-4">
              <Button
                variant="primary"
                size="lg"
                onClick={handleStartBuilding}
                className="bg-primary hover:bg-primary-hover shadow-glow text-white font-bold gap-2 px-8"
              >
                <SlidersHorizontal size={20} />
                <span>START BUILDING YOUR LAPTOP</span>
                <ArrowRight size={18} />
              </Button>

              <span className="text-xs text-muted-light font-medium">
                No commitment • Save builds anytime
              </span>
            </div>

          </div>

          {/* Right Visual Configurator Mockup / Showcase */}
          <div className="lg:col-span-5">
            <div className="relative rounded-2xl bg-navy-deep border border-navy-light/80 p-6 shadow-2xl space-y-4">
              
              {/* Header */}
              <div className="flex items-center justify-between border-b border-navy-light/60 pb-3">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-error" />
                  <span className="w-3 h-3 rounded-full bg-warning" />
                  <span className="w-3 h-3 rounded-full bg-success" />
                </div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-primary-sky">
                  Live Visual Configurator
                </span>
              </div>

              {/* Laptop Visual Preview */}
              <div className="relative h-56 w-full rounded-xl bg-gradient-to-b from-navy-light/50 to-navy-deep p-4 flex items-center justify-center border border-navy-light/40">
                <Image
                  src="https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80"
                  alt="Configured Laptop Visual Preview"
                  fill
                  className="object-contain"
                />
                
                {/* Live Swatch Badge */}
                <div className="absolute bottom-3 left-3 bg-navy/90 backdrop-blur-sm border border-navy-light px-2.5 py-1 rounded-lg text-[11px] flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-primary" />
                  <span className="text-white font-medium">Arctic Blue Finish</span>
                </div>
              </div>

              {/* Live Option Matrix Mini Grid */}
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2.5 rounded-lg bg-navy-light/50 border border-navy-light/40">
                  <span className="text-[10px] text-muted-light block">RAM Choice</span>
                  <span className="font-bold text-white">32GB DDR5 5600MHz</span>
                </div>
                <div className="p-2.5 rounded-lg bg-navy-light/50 border border-navy-light/40">
                  <span className="text-[10px] text-muted-light block">Storage Choice</span>
                  <span className="font-bold text-white">2TB Gen4 Pro NVMe</span>
                </div>
              </div>

              {/* Live Price Tag Bar */}
              <div className="flex items-center justify-between pt-2 border-t border-navy-light/60">
                <div>
                  <span className="text-[11px] text-muted-light block">Instant Live Estimate</span>
                  <span className="text-xl font-extrabold text-white">₦1,670,000</span>
                </div>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleStartBuilding}
                  className="font-bold text-xs"
                >
                  Configure
                </Button>
              </div>

            </div>
          </div>

        </div>
      </div>
    </section>
  )
}
