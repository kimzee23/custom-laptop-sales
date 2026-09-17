import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatPrice(amount: number, currencySymbol: string = '₦'): string {
  if (isNaN(amount) || amount === null || amount === undefined) {
    return `${currencySymbol}0`
  }
  return `${currencySymbol}${Math.round(amount).toLocaleString('en-NG')}`
}

export function calculateDiscount(originalPrice?: number, currentPrice?: number): number {
  if (!originalPrice || !currentPrice || originalPrice <= currentPrice) return 0
  return Math.round(((originalPrice - currentPrice) / originalPrice) * 100)
}
