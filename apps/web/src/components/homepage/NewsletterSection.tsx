'use client'

import React, { useState } from 'react'
import { Mail, CheckCircle2 } from 'lucide-react'
import { Button } from '@/components/ui/Button'

export const NewsletterSection: React.FC = () => {
  const [email, setEmail] = useState('')
  const [isSubscribed, setIsSubscribed] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (email) {
      setIsSubscribed(true)
      setEmail('')
    }
  }

  return (
    <section className="py-12 bg-primary-soft border-b border-border">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
        
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-primary/20 text-primary text-xs font-bold shadow-sm">
          <Mail size={14} />
          <span>VIP ACCESS & HARDWARE DROPS</span>
        </div>

        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-black text-navy font-display tracking-tight">
            Get ₦25,000 Off Your First Custom Build
          </h2>
          <p className="text-xs sm:text-sm text-muted max-w-lg mx-auto">
            Subscribe to our weekly hardware brief for exclusive coupon codes, RTX restock alerts, and early access to limited chassis color drops.
          </p>
        </div>

        {isSubscribed ? (
          <div className="inline-flex items-center gap-2 px-4 py-3 bg-success-light text-success rounded-xl border border-success/30 font-bold text-sm">
            <CheckCircle2 size={18} />
            <span>Thank you for subscribing! Your discount code has been sent to your email.</span>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="max-w-md mx-auto flex flex-col sm:flex-row gap-2">
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email address..."
              className="flex-1 h-11 px-4 rounded-button border border-border bg-white text-sm text-navy placeholder:text-muted focus:border-primary focus:outline-none shadow-sm"
            />
            <Button variant="primary" size="md" type="submit" className="h-11 px-6 font-bold">
              Claim Discount
            </Button>
          </form>
        )}

        <div className="text-[11px] text-muted">
          We value your privacy. Unsubscribe anytime with 1 click.
        </div>

      </div>
    </section>
  )
}
