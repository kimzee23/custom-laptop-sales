'use client'

import React from 'react'
import Link from 'next/link'
import { 
  Sparkles, 
  ShieldCheck, 
  Truck, 
  RotateCcw, 
  Headphones, 
  CreditCard, 
  Lock,
  Mail,
  Phone,
  MapPin
} from 'lucide-react'
import { useOrderTrackingStore } from '@/stores/orderTrackingStore'

export const StoreFooter: React.FC = () => {
  const { openTracking } = useOrderTrackingStore()

  return (
    <footer className="bg-navy text-white pt-12 pb-8 border-t border-navy-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Value Propositions / Trust Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pb-12 border-b border-navy-light/60">
          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-xl bg-navy-light text-primary-sky flex-shrink-0">
              <Truck size={22} />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">Fast Nationwide Delivery</h4>
              <p className="text-xs text-muted-light mt-0.5">Tracked door-to-door delivery with live updates.</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-xl bg-navy-light text-success flex-shrink-0">
              <ShieldCheck size={22} />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">2-Year Official Warranty</h4>
              <p className="text-xs text-muted-light mt-0.5">Full hardware coverage and priority repair service.</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-xl bg-navy-light text-primary-sky flex-shrink-0">
              <RotateCcw size={22} />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">7-Day Free Returns</h4>
              <p className="text-xs text-muted-light mt-0.5">Hassle-free return policy if you are not fully satisfied.</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="p-2.5 rounded-xl bg-navy-light text-warning flex-shrink-0">
              <Headphones size={22} />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">24/7 Expert Support</h4>
              <p className="text-xs text-muted-light mt-0.5">Talk with certified laptop hardware specialists anytime.</p>
            </div>
          </div>
        </div>

        {/* Main Footer Links */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 py-12 border-b border-navy-light/60 text-xs">
          
          {/* Brand & Contact */}
          <div className="col-span-2 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white">
                <Sparkles size={18} />
              </div>
              <span className="text-lg font-black tracking-tight text-white font-display">
                REAL<span className="text-primary-sky">TECH</span>
              </span>
            </div>
            <p className="text-muted-light max-w-sm leading-relaxed">
              Nigeria&apos;s premier custom laptop e-commerce platform. Buy ready-to-ship machines or tailor RAM, SSD, GPU, chassis color, and lid artwork with instant price feedback.
            </p>
            <div className="space-y-2 text-muted-light">
              <div className="flex items-center gap-2">
                <MapPin size={14} className="text-primary-sky" />
                <span>Victoria Island / Ikeja Tech Corridor, Lagos, Nigeria</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone size={14} className="text-primary-sky" />
                <span>+234 800 REAL TECH (0800 7325 8324)</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail size={14} className="text-primary-sky" />
                <span>support@realtechlaptops.com</span>
              </div>
            </div>
          </div>

          {/* Categories */}
          <div className="space-y-3">
            <h5 className="text-sm font-bold text-white">Shop Laptops</h5>
            <ul className="space-y-2 text-muted-light">
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Gaming Laptops</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Business & Creator</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Student Laptops</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Everyday Workhorses</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">MacBook Tier Ultrabooks</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Laptop Docks & Accessories</Link></li>
            </ul>
          </div>

          {/* Custom Builder */}
          <div className="space-y-3">
            <h5 className="text-sm font-bold text-white">Custom Configurator</h5>
            <ul className="space-y-2 text-muted-light">
              <li><Link href="#builder-section" className="hover:text-primary-sky transition-colors">Design Your Machine</Link></li>
              <li><Link href="#builder-section" className="hover:text-primary-sky transition-colors">DDR5 RAM Upgrades</Link></li>
              <li><Link href="#builder-section" className="hover:text-primary-sky transition-colors">PCIe 4.0 SSD Upgrades</Link></li>
              <li><Link href="#builder-section" className="hover:text-primary-sky transition-colors">RTX 40-Series GPU Builder</Link></li>
              <li><Link href="#builder-section" className="hover:text-primary-sky transition-colors">Custom Artwork & Laser Engraving</Link></li>
              <li><Link href="#builder-section" className="hover:text-primary-sky transition-colors">Chassis Color Finishes</Link></li>
            </ul>
          </div>

          {/* Customer Care & Legal */}
          <div className="space-y-3">
            <h5 className="text-sm font-bold text-white">Customer Support</h5>
            <ul className="space-y-2 text-muted-light">
              <li>
                <button onClick={() => openTracking()} className="hover:text-primary-sky transition-colors text-left">
                  Track Your Order
                </button>
              </li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Delivery Timelines</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Warranty & Repairs</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Returns & Refunds</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Corporate / Bulk Inquiries</Link></li>
              <li><Link href="#products-section" className="hover:text-primary-sky transition-colors">Privacy & Security Policy</Link></li>
            </ul>
          </div>

        </div>

        {/* Bottom Payment & Copyright */}
        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-muted-light">
          <div className="flex items-center gap-2">
            <Lock size={14} className="text-success" />
            <span>Bank-Grade 256-Bit SSL Encryption. Authoritative Payment Verification.</span>
          </div>

          <div className="flex items-center gap-3">
            <span className="font-semibold text-white">Verified Payments:</span>
            <span className="px-2 py-1 bg-navy-light rounded font-bold text-[11px] text-white">PAYSTACK</span>
            <span className="px-2 py-1 bg-navy-light rounded font-bold text-[11px] text-white">FLUTTERWAVE</span>
            <span className="px-2 py-1 bg-navy-light rounded font-bold text-[11px] text-white">OPAY</span>
            <span className="px-2 py-1 bg-navy-light rounded font-bold text-[11px] text-white">CARDS</span>
          </div>

          <p>© {new Date().getFullYear()} RealTech Laptops Nigeria. All rights reserved.</p>
        </div>

      </div>
    </footer>
  )
}
