'use client'

import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Sparkles, ShieldCheck, Cpu, Star, ArrowLeft, CheckCircle2, Truck, Award } from 'lucide-react'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col justify-between text-slate-900 selection:bg-primary selection:text-white">
      {/* Top Subtle Warm Background Pattern */}
      <div className="absolute top-0 inset-x-0 h-96 bg-gradient-to-b from-blue-50/80 via-indigo-50/30 to-transparent pointer-events-none" />

      {/* Top Header Navigation */}
      <header className="relative z-10 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
            <Sparkles size={20} />
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-black tracking-tight text-navy leading-none font-display">
              REAL<span className="text-primary">TECH</span>
            </span>
            <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">
              Custom Laptops & Store
            </span>
          </div>
        </Link>

        <Link
          href="/"
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-700 hover:text-primary bg-white hover:bg-slate-50 border border-slate-200 px-4 py-2 rounded-xl transition-all shadow-sm"
        >
          <ArrowLeft size={14} />
          <span>Back to Store</span>
        </Link>
      </header>

      {/* Main Container */}
      <main className="relative z-10 flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 lg:py-10 flex items-center justify-center">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 w-full max-w-5xl items-center">
          
          {/* Left / Center Form Container */}
          <div className="lg:col-span-6 w-full max-w-md mx-auto">
            <div className="bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-xl shadow-slate-200/60 text-slate-900">
              {children}
            </div>
          </div>

          {/* Right Showcase Panel (Human & Trust Centered) */}
          <div className="hidden lg:flex lg:col-span-6 flex-col justify-center space-y-6 pl-4 text-slate-800">
            
            {/* Tag Badge */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-primary text-xs font-bold w-fit">
              <Award size={14} />
              <span>OFFICIAL STORE & CUSTOM BUILDER</span>
            </div>

            <h2 className="text-3xl sm:text-4xl font-black text-navy leading-tight tracking-tight font-display">
              Built for your work, <br />
              <span className="text-primary">customized for your ambition.</span>
            </h2>

            <p className="text-sm text-slate-600 leading-relaxed">
              Sign in to manage your custom builds, save your 3D configurations, access real-time order tracking, and enjoy our comprehensive 2-Year Official Warranty.
            </p>

            {/* Featured Laptop Showcase Card */}
            <div className="rounded-2xl bg-white border border-slate-200 p-5 shadow-md space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100 text-xs">
                <span className="font-bold text-navy flex items-center gap-1.5">
                  <Cpu size={14} className="text-primary" /> TitanForge Predator 16 Pro
                </span>
                <span className="text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-bold text-[11px]">
                  In Stock & Ready
                </span>
              </div>

              <div className="flex items-center gap-4 py-1">
                <div className="relative w-28 h-20 flex-shrink-0 bg-slate-50 rounded-xl p-1 border border-slate-100">
                  <Image
                    src="https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=400&q=80"
                    alt="TitanForge Predator 16"
                    fill
                    className="object-contain"
                  />
                </div>
                <div className="space-y-1">
                  <p className="text-xs text-slate-600 font-medium">
                    Intel Core i9-14900HX • RTX 4070 • 64GB DDR5 • 2TB NVMe
                  </p>
                  <div className="text-sm font-black text-navy">
                    ₦1,450,000 <span className="text-slate-400 font-normal line-through text-xs ml-1">₦1,680,000</span>
                  </div>
                </div>
              </div>

              {/* Guarantees */}
              <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-100 text-[11px] text-slate-700 font-semibold text-center">
                <div className="p-2 rounded-xl bg-slate-50 border border-slate-100">
                  <ShieldCheck size={15} className="mx-auto text-emerald-600 mb-0.5" />
                  <span>2-Yr Warranty</span>
                </div>
                <div className="p-2 rounded-xl bg-slate-50 border border-slate-100">
                  <Truck size={15} className="mx-auto text-primary mb-0.5" />
                  <span>Free Lagos Delivery</span>
                </div>
                <div className="p-2 rounded-xl bg-slate-50 border border-slate-100">
                  <Star size={15} className="mx-auto text-amber-500 mb-0.5" />
                  <span>4.9 / 5 Rating</span>
                </div>
              </div>
            </div>

            {/* Testimonial Quote */}
            <div className="flex items-center gap-3 p-4 rounded-2xl bg-white border border-slate-200/80 shadow-sm">
              <div className="w-10 h-10 rounded-full bg-blue-100 text-primary flex items-center justify-center font-bold text-xs flex-shrink-0">
                EA
              </div>
              <p className="text-xs text-slate-700 italic leading-snug">
                &ldquo;Configured my TitanForge laptop with 64GB RAM and custom lid artwork. Arrived in Lagos within 48 hours in flawless condition!&rdquo;
                <span className="block not-italic text-[11px] text-slate-500 font-bold mt-1">
                  — Emeka Adeleke, Verified Customer
                </span>
              </p>
            </div>

          </div>

        </div>
      </main>

      {/* Clean Footer */}
      <footer className="relative z-10 py-6 text-center text-xs text-slate-500 border-t border-slate-200 bg-white/50 backdrop-blur-sm">
        <p>&copy; {new Date().getFullYear()} REALTECH Custom Laptops & Electronics. All rights reserved.</p>
      </footer>
    </div>
  )
}
