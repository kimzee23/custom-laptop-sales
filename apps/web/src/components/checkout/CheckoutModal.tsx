'use client'

import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import { 
  X, ShieldCheck, CreditCard, ArrowRight, ArrowLeft, CheckCircle2, 
  Lock, RefreshCw, Smartphone, Building, Zap, AlertCircle, Laptop
} from 'lucide-react'
import { useCartStore } from '@/stores/cartStore'
import { useAuthStore } from '@/stores/authStore'
import { formatPrice } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { api } from '@/lib/api'

interface CheckoutModalProps {
  isOpen: boolean
  onClose: () => void
}

type GatewayType = 'PAYSTACK' | 'FLUTTERWAVE' | 'OPAY'
type CheckoutStep = 'address' | 'review' | 'payment' | 'processing'

export const CheckoutModal: React.FC<CheckoutModalProps> = ({ isOpen, onClose }) => {
  const { items, getSubtotal, clearCart } = useCartStore()
  const { user, isAuthenticated } = useAuthStore()
  const subtotal = getSubtotal()

  const defaultAddr = user?.addresses?.find(a => a.isDefault) || user?.addresses?.[0]

  const [step, setStep] = useState<CheckoutStep>('address')
  const [selectedGateway, setSelectedGateway] = useState<GatewayType>('PAYSTACK')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  
  // Client-side unique idempotency key generated per checkout attempt
  const [idempotencyKey, setIdempotencyKey] = useState<string>('')

  // Form Fields - Auto-populated if customer is logged in
  const [formData, setFormData] = useState({
    fullName: user?.name || 'Emeka Adeleke',
    email: user?.email || 'emeka.adeleke@example.com',
    phone: user?.phone || '08031234567',
    street: defaultAddr?.street || 'Plot 14B, Admiralty Way, Lekki Phase 1',
    city: defaultAddr?.city || 'Lekki / Lagos Island',
    state: defaultAddr?.state || 'Lagos State',
    notes: 'Please call on delivery. Building has security gate.'
  })

  // Sync with auth user on login changes
  useEffect(() => {
    if (user) {
      const activeDefault = user.addresses?.find(a => a.isDefault) || user.addresses?.[0]
      setFormData(prev => ({
        ...prev,
        fullName: user.name || prev.fullName,
        email: user.email || prev.email,
        phone: user.phone || prev.phone,
        street: activeDefault?.street || prev.street,
        city: activeDefault?.city || prev.city,
        state: activeDefault?.state || prev.state,
      }))
    }
  }, [user])

  useEffect(() => {
    if (isOpen && !idempotencyKey) {
      // Generate unique UUID/timestamp idempotency key
      const key = `idemp_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
      setIdempotencyKey(key)
    }
  }, [isOpen, idempotencyKey])

  if (!isOpen) return null

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleProceedToPayment = async () => {
    setIsSubmitting(true)
    setErrorMessage(null)

    try {
      // 1. Create order on backend
      const checkoutPayload = {
        customer_name: formData.fullName,
        customer_email: formData.email,
        customer_phone: formData.phone,
        shipping_address: {
          full_name: formData.fullName,
          phone_number: formData.phone,
          email: formData.email,
          street: formData.street,
          city: formData.city,
          state: formData.state,
          country: 'Nigeria',
          additional_notes: formData.notes
        },
        items: items.map(i => ({
          product_id: i.productId,
          product_title: i.productTitle,
          quantity: i.quantity,
          unit_price: i.unitPrice,
          image_url: i.imageUrl,
          configuration_snapshot: i.configuration || {}
        })),
        shipping_fee: 0.0,
        discount_amount: 0.0,
        idempotency_key: idempotencyKey
      }

      // Step 1: Create Order
      const orderData = await api.checkoutOrder(checkoutPayload)
      const orderNumber = orderData.order_number

      // Step 2: Initialize Payment with Idempotency Key
      const initData = await api.initializePayment({
        order_number: orderNumber,
        provider: selectedGateway,
        idempotency_key: idempotencyKey,
        callback_url: `${window.location.origin}/checkout/verify?gateway=${selectedGateway}`
      })

      // Redirect customer to authorized checkout URL
      if (initData.checkout_url) {
        window.location.href = initData.checkout_url
      } else {
        // Fallback to local verify page
        window.location.href = `/checkout/verify?gateway=${selectedGateway}&reference=${initData.provider_reference}&status=success`
      }
    } catch (err: any) {
      console.error('Checkout error:', err)
      setErrorMessage(err.message || 'An unexpected error occurred during checkout.')
      setIsSubmitting(false)
    }
  }

  const nigerianStates = [
    'Lagos State', 'Abuja (FCT)', 'Rivers State', 'Oyo State', 'Kano State', 
    'Enugu State', 'Delta State', 'Ogun State', 'Kaduna State', 'Edo State', 'Anambra State'
  ]

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 bg-navy/70 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-white rounded-2xl shadow-2xl overflow-hidden border border-border flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="p-5 border-b border-border bg-primary-soft flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center font-bold shadow-md shadow-primary/20">
              <Lock size={20} />
            </div>
            <div>
              <h2 className="text-lg font-extrabold text-navy">Secure Checkout & Custom Build Setup</h2>
              <p className="text-xs text-muted flex items-center gap-1.5 mt-0.5">
                <ShieldCheck size={14} className="text-success inline" />
                256-bit SSL Encrypted & CBN Licensed Gateways
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 rounded-xl text-muted hover:text-navy hover:bg-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Multi-Step Indicator */}
        <div className="px-6 py-3 bg-muted-bg/50 border-b border-border flex items-center justify-between text-xs font-semibold">
          <button 
            onClick={() => setStep('address')}
            className={`flex items-center gap-2 ${step === 'address' ? 'text-primary font-bold' : 'text-muted'}`}
          >
            <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] ${step === 'address' ? 'bg-primary text-white' : 'bg-border text-foreground'}`}>1</span>
            Delivery Address
          </button>
          <div className="w-8 h-[1px] bg-border" />
          <button 
            onClick={() => setStep('review')}
            className={`flex items-center gap-2 ${step === 'review' ? 'text-primary font-bold' : 'text-muted'}`}
          >
            <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] ${step === 'review' ? 'bg-primary text-white' : 'bg-border text-foreground'}`}>2</span>
            Build & Items Review
          </button>
          <div className="w-8 h-[1px] bg-border" />
          <button 
            onClick={() => setStep('payment')}
            className={`flex items-center gap-2 ${step === 'payment' ? 'text-primary font-bold' : 'text-muted'}`}
          >
            <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] ${step === 'payment' ? 'bg-primary text-white' : 'bg-border text-foreground'}`}>3</span>
            Payment Gateway
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto flex-1 space-y-5">
          {errorMessage && (
            <div className="p-4 rounded-xl bg-error/10 border border-error/20 flex items-start gap-3 text-error text-xs font-medium">
              <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Checkout Notice</p>
                <p>{errorMessage}</p>
              </div>
            </div>
          )}

          {/* STEP 1: DELIVERY ADDRESS */}
          {step === 'address' && (
            <div className="space-y-4 animate-fade-in">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-navy mb-1.5">Recipient Full Name *</label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                    placeholder="e.g. Babatunde Johnson"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-navy mb-1.5">Email Address *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                    placeholder="name@domain.com"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-navy mb-1.5">Phone Number (WhatsApp Active) *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                    placeholder="080 1234 5678"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-navy mb-1.5">Delivery State *</label>
                  <select
                    name="state"
                    value={formData.state}
                    onChange={handleInputChange}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary bg-white"
                  >
                    {nigerianStates.map(st => (
                      <option key={st} value={st}>{st}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-navy mb-1.5">Street Address & Landmark *</label>
                <input
                  type="text"
                  name="street"
                  value={formData.street}
                  onChange={handleInputChange}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                  placeholder="Street name, house number, nearest landmark"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-navy mb-1.5">Special Dispatch / Custom Assembly Notes</label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleInputChange}
                  rows={2}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary resize-none"
                  placeholder="Add any building entry code or specific dispatch instructions..."
                />
              </div>
            </div>
          )}

          {/* STEP 2: REVIEW ITEMS & CUSTOM HARDWARE */}
          {step === 'review' && (
            <div className="space-y-4 animate-fade-in">
              <h3 className="text-sm font-bold text-navy">Order Summary ({items.length} {items.length === 1 ? 'Item' : 'Items'})</h3>
              <div className="divide-y divide-border border border-border rounded-xl p-3 bg-muted-bg/30 max-h-60 overflow-y-auto space-y-3">
                {items.map((item) => (
                  <div key={item.id} className="pt-3 first:pt-0 flex items-center gap-3">
                    <div className="relative w-12 h-12 rounded-lg bg-white border border-border overflow-hidden flex-shrink-0">
                      <Image src={item.imageUrl} alt={item.productTitle} fill className="object-cover" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-bold text-navy truncate">{item.productTitle}</p>
                      <p className="text-[11px] text-muted">
                        Qty: {item.quantity} × {formatPrice(item.unitPrice)}
                      </p>
                      {item.configurationSummary && (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {item.configurationSummary.color && (
                            <Badge variant="outline" size="sm" className="text-[9px] py-0 px-1">
                              {item.configurationSummary.color}
                            </Badge>
                          )}
                          {item.configurationSummary.ram && (
                            <Badge variant="outline" size="sm" className="text-[9px] py-0 px-1">
                              {item.configurationSummary.ram}
                            </Badge>
                          )}
                          {item.configurationSummary.storage && (
                            <Badge variant="outline" size="sm" className="text-[9px] py-0 px-1">
                              {item.configurationSummary.storage}
                            </Badge>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="text-xs font-extrabold text-navy">
                      {formatPrice(item.totalPrice)}
                    </div>
                  </div>
                ))}
              </div>

              {/* Delivery info snapshot */}
              <div className="p-3.5 rounded-xl bg-primary-soft/50 border border-primary/20 text-xs text-navy space-y-1">
                <p className="font-bold flex items-center justify-between">
                  <span>Shipping To: {formData.fullName}</span>
                  <button onClick={() => setStep('address')} className="text-primary hover:underline text-[11px]">Edit</button>
                </p>
                <p className="text-muted text-[11px]">{formData.street}, {formData.city}, {formData.state}</p>
                <p className="text-muted text-[11px]">Tel: {formData.phone}</p>
              </div>
            </div>
          )}

          {/* STEP 3: PAYMENT GATEWAY SELECTION */}
          {step === 'payment' && (
            <div className="space-y-4 animate-fade-in">
              <div>
                <h3 className="text-sm font-bold text-navy">Select Payment Rail</h3>
                <p className="text-xs text-muted">Choose your preferred verified Nigerian payment gateway:</p>
              </div>

              <div className="grid grid-cols-1 gap-3">
                {/* Paystack */}
                <div 
                  onClick={() => setSelectedGateway('PAYSTACK')}
                  className={`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-start gap-3.5 ${
                    selectedGateway === 'PAYSTACK' 
                      ? 'border-primary bg-primary-soft/40 shadow-sm' 
                      : 'border-border hover:border-muted hover:bg-white'
                  }`}
                >
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                    selectedGateway === 'PAYSTACK' ? 'border-primary bg-primary text-white' : 'border-border'
                  }`}>
                    {selectedGateway === 'PAYSTACK' && <CheckCircle2 size={12} />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold text-navy">Paystack Checkout</span>
                      <Badge variant="primary" size="sm">Instant Verification</Badge>
                    </div>
                    <p className="text-xs text-muted mt-0.5">
                      Pay with Debit/Credit Card (Mastercard, Visa, Verve), Bank Transfer, USSD, or Apple Pay.
                    </p>
                  </div>
                </div>

                {/* Flutterwave */}
                <div 
                  onClick={() => setSelectedGateway('FLUTTERWAVE')}
                  className={`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-start gap-3.5 ${
                    selectedGateway === 'FLUTTERWAVE' 
                      ? 'border-primary bg-primary-soft/40 shadow-sm' 
                      : 'border-border hover:border-muted hover:bg-white'
                  }`}
                >
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                    selectedGateway === 'FLUTTERWAVE' ? 'border-primary bg-primary text-white' : 'border-border'
                  }`}>
                    {selectedGateway === 'FLUTTERWAVE' && <CheckCircle2 size={12} />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold text-navy">Flutterwave Standard</span>
                      <Badge variant="secondary" size="sm">Pan-African</Badge>
                    </div>
                    <p className="text-xs text-muted mt-0.5">
                      Direct Bank Accounts, Cards, Mobile Money, and Barter payments across Africa.
                    </p>
                  </div>
                </div>

                {/* OPay */}
                <div 
                  onClick={() => setSelectedGateway('OPAY')}
                  className={`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-start gap-3.5 ${
                    selectedGateway === 'OPAY' 
                      ? 'border-primary bg-primary-soft/40 shadow-sm' 
                      : 'border-border hover:border-muted hover:bg-white'
                  }`}
                >
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                    selectedGateway === 'OPAY' ? 'border-primary bg-primary text-white' : 'border-border'
                  }`}>
                    {selectedGateway === 'OPAY' && <CheckCircle2 size={12} />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold text-navy">OPay Digital Services</span>
                      <Badge variant="success" size="sm">Zero Transfer Fees</Badge>
                    </div>
                    <p className="text-xs text-muted mt-0.5">
                      Pay instantly with OPay App Wallet, QR Scan, OPay Cards, or Virtual Bank Accounts.
                    </p>
                  </div>
                </div>
              </div>

              {/* Idempotency token indicator */}
              <div className="text-[10px] text-muted flex items-center justify-between px-1">
                <span>Idempotency Session: <code className="text-navy font-mono">{idempotencyKey.substring(0, 16)}...</code></span>
                <span className="text-success font-semibold">Protected against double-clicks</span>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-5 border-t border-border bg-background flex items-center justify-between gap-4">
          <div>
            <span className="text-xs text-muted block">Total Payable</span>
            <span className="text-lg font-extrabold text-navy">{formatPrice(subtotal)}</span>
          </div>

          <div className="flex items-center gap-2">
            {step !== 'address' && (
              <Button
                variant="outline"
                size="md"
                onClick={() => setStep(step === 'payment' ? 'review' : 'address')}
                disabled={isSubmitting}
              >
                <ArrowLeft size={16} className="mr-1.5" />
                Back
              </Button>
            )}

            {step === 'address' && (
              <Button
                variant="primary"
                size="md"
                onClick={() => {
                  if (!formData.fullName || !formData.email || !formData.street) {
                    setErrorMessage('Please fill in all required delivery fields.')
                    return
                  }
                  setErrorMessage(null)
                  setStep('review')
                }}
              >
                <span>Continue to Review</span>
                <ArrowRight size={16} className="ml-1.5" />
              </Button>
            )}

            {step === 'review' && (
              <Button
                variant="primary"
                size="md"
                onClick={() => setStep('payment')}
              >
                <span>Select Payment</span>
                <ArrowRight size={16} className="ml-1.5" />
              </Button>
            )}

            {step === 'payment' && (
              <Button
                variant="primary"
                size="md"
                disabled={isSubmitting}
                onClick={handleProceedToPayment}
                className="bg-success hover:bg-success/90"
              >
                {isSubmitting ? (
                  <>
                    <RefreshCw size={16} className="animate-spin mr-2" />
                    Connecting Gateway...
                  </>
                ) : (
                  <>
                    <Lock size={16} className="mr-1.5" />
                    <span>PAY {formatPrice(subtotal)}</span>
                  </>
                )}
              </Button>
            )}
          </div>
        </div>

      </div>
    </div>
  )
}
