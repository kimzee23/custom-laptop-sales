import React from 'react'
import { formatPrice } from '@/lib/utils'
import { Badge } from '@/components/ui/Badge'
import { cn } from '@/lib/utils'

interface PriceDisplayProps {
  price: number
  originalPrice?: number
  discountPercentage?: number
  size?: 'sm' | 'md' | 'lg' | 'xl'
  className?: string
}

export const PriceDisplay: React.FC<PriceDisplayProps> = ({
  price,
  originalPrice,
  discountPercentage,
  size = 'md',
  className,
}) => {
  const sizeClasses = {
    sm: "text-sm font-bold text-navy",
    md: "text-base font-bold text-navy",
    lg: "text-xl font-bold text-navy",
    xl: "text-2xl lg:text-3xl font-extrabold text-navy tracking-tight",
  }

  const originalSizeClasses = {
    sm: "text-[11px] line-through text-muted",
    md: "text-xs line-through text-muted",
    lg: "text-sm line-through text-muted",
    xl: "text-base line-through text-muted",
  }

  return (
    <div className={cn("flex flex-wrap items-baseline gap-2", className)}>
      <span className={cn(sizeClasses[size])}>{formatPrice(price)}</span>
      {originalPrice && originalPrice > price && (
        <span className={cn(originalSizeClasses[size])}>{formatPrice(originalPrice)}</span>
      )}
      {discountPercentage && discountPercentage > 0 && (
        <Badge variant="discount" size="sm">
          -{discountPercentage}%
        </Badge>
      )}
    </div>
  )
}
