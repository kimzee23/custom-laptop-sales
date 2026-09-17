import React from 'react'
import { cn } from '@/lib/utils'

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'secondary' | 'discount' | 'success' | 'warning' | 'outline' | 'navy'
  size?: 'sm' | 'md'
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = 'primary',
  size = 'md',
  children,
  ...props
}) => {
  const base = "inline-flex items-center font-medium rounded-full select-none"

  const variants = {
    primary: "bg-primary-light text-primary border border-blue-200",
    secondary: "bg-muted-bg text-muted border border-border",
    discount: "bg-discount text-white font-bold tracking-tight shadow-sm",
    success: "bg-success-light text-success border border-green-200",
    warning: "bg-warning-light text-warning border border-yellow-200",
    outline: "border border-border text-foreground bg-white",
    navy: "bg-navy text-white font-semibold",
  }

  const sizes = {
    sm: "px-2 py-0.5 text-[11px]",
    md: "px-2.5 py-1 text-xs",
  }

  return (
    <span className={cn(base, variants[variant], sizes[size], className)} {...props}>
      {children}
    </span>
  )
}
