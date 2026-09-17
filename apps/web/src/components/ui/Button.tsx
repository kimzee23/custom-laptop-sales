import React from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'navy' | 'accent'
  size?: 'sm' | 'md' | 'lg' | 'icon'
  isLoading?: boolean
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading, children, disabled, ...props }, ref) => {
    const baseStyles = "inline-flex items-center justify-center font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98] select-none"
    
    const variants = {
      primary: "bg-primary text-white hover:bg-primary-hover shadow-sm hover:shadow-md",
      secondary: "bg-primary-light text-primary hover:bg-blue-100 font-semibold",
      outline: "border border-border bg-white text-navy hover:bg-primary-soft hover:border-primary",
      ghost: "text-muted hover:text-navy hover:bg-primary-soft",
      navy: "bg-navy text-white hover:bg-navy-light shadow-sm",
      accent: "bg-accent text-white hover:bg-blue-400 font-semibold shadow-sm",
    }

    const sizes = {
      sm: "h-8 px-3 text-xs rounded-lg gap-1.5",
      md: "h-10 px-4 text-sm rounded-button gap-2",
      lg: "h-12 px-6 text-base rounded-button gap-2.5 font-semibold",
      icon: "h-10 w-10 rounded-button p-0",
    }

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        {...props}
      >
        {isLoading ? (
          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
        ) : null}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
