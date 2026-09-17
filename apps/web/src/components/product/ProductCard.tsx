'use client'

import React from 'react'
import Image from 'next/image'
import { Heart, ShoppingBag, SlidersHorizontal, Cpu, HardDrive, CheckCircle2 } from 'lucide-react'
import { Product } from '@/types'
import { PriceDisplay } from '@/components/ui/PriceDisplay'
import { RatingStars } from '@/components/ui/RatingStars'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { useCartStore } from '@/stores/cartStore'
import { useWishlistStore } from '@/stores/wishlistStore'
import { useConfiguratorStore } from '@/stores/configuratorStore'

interface ProductCardProps {
  product: Product
  onQuickView?: (product: Product) => void
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onQuickView }) => {
  const { addItem } = useCartStore()
  const { toggleWishlist, isInWishlist } = useWishlistStore()
  const { openConfigurator } = useConfiguratorStore()

  const inWishlist = isInWishlist(product.id)

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation()
    addItem({
      productId: product.id,
      productTitle: product.title,
      imageUrl: product.image_url,
      quantity: 1,
      unitPrice: product.base_price,
      configurationSummary: {
        ram: product.specs.ram || '16GB DDR5',
        storage: product.specs.storage || '1TB NVMe',
        gpu: product.specs.gpu || 'Integrated',
      }
    })
  }

  const handleConfigure = (e: React.MouseEvent) => {
    e.stopPropagation()
    openConfigurator(product)
  }

  return (
    <div className="group bg-white rounded-card border border-border p-4 hover:border-primary hover:shadow-card-hover transition-all duration-200 flex flex-col justify-between relative">
      
      {/* Top Badges & Wishlist Action */}
      <div className="flex items-center justify-between z-10">
        <div className="flex flex-wrap gap-1">
          {product.is_flash_deal && (
            <Badge variant="discount" size="sm">FLASH DEAL</Badge>
          )}
          {product.is_best_seller && (
            <Badge variant="navy" size="sm">BEST SELLER</Badge>
          )}
          {product.discount_percentage && !product.is_flash_deal && (
            <Badge variant="discount" size="sm">-{product.discount_percentage}%</Badge>
          )}
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation()
            toggleWishlist(product)
          }}
          className={`p-2 rounded-full transition-colors ${
            inWishlist
              ? 'bg-error-light text-error'
              : 'bg-background text-muted hover:text-error hover:bg-error-light'
          }`}
          title={inWishlist ? 'Remove from Wishlist' : 'Add to Wishlist'}
        >
          <Heart size={16} className={inWishlist ? 'fill-error' : ''} />
        </button>
      </div>

      {/* Product Image */}
      <div 
        onClick={() => onQuickView ? onQuickView(product) : openConfigurator(product)}
        className="relative h-44 sm:h-48 w-full my-3 cursor-pointer overflow-hidden rounded-lg bg-background p-2"
      >
        <Image
          src={product.image_url}
          alt={product.title}
          fill
          className="object-contain group-hover:scale-105 transition-transform duration-300"
        />
      </div>

      {/* Product Information */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-[11px] text-muted">
          <span className="font-semibold text-primary">{product.brand?.name || 'RealTech'}</span>
          <span className="flex items-center gap-1 text-success">
            <CheckCircle2 size={12} />
            In Stock
          </span>
        </div>

        <h3 
          onClick={() => onQuickView ? onQuickView(product) : openConfigurator(product)}
          className="text-sm font-bold text-navy line-clamp-2 hover:text-primary transition-colors cursor-pointer"
        >
          {product.title}
        </h3>

        {/* Rating */}
        <RatingStars rating={product.rating} reviewCount={product.review_count} />

        {/* Key Specs Pills */}
        <div className="flex flex-wrap gap-1.5 py-1 text-[11px] text-muted">
          {product.specs.ram && (
            <span className="inline-flex items-center gap-1 bg-background px-2 py-0.5 rounded border border-border">
              <Cpu size={11} className="text-primary" />
              {product.specs.ram.split(' ')[0]} RAM
            </span>
          )}
          {product.specs.storage && (
            <span className="inline-flex items-center gap-1 bg-background px-2 py-0.5 rounded border border-border">
              <HardDrive size={11} className="text-primary" />
              {product.specs.storage.split(' ')[0]} SSD
            </span>
          )}
        </div>

        {/* Price Display */}
        <div className="pt-2 border-t border-border">
          <PriceDisplay
            price={product.base_price}
            originalPrice={product.original_price}
            discountPercentage={product.discount_percentage}
            size="md"
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-2 pt-4 mt-2">
        <Button
          variant="outline"
          size="sm"
          onClick={handleAddToCart}
          className="text-xs font-semibold"
        >
          <ShoppingBag size={14} />
          <span>Add</span>
        </Button>

        <Button
          variant="primary"
          size="sm"
          onClick={handleConfigure}
          className="text-xs font-bold gap-1.5"
        >
          <SlidersHorizontal size={14} />
          <span>Build</span>
        </Button>
      </div>

    </div>
  )
}
