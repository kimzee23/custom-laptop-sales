'use client'

import React, { useState } from 'react'
import { MessageCircle, X, ShieldCheck, Sparkles } from 'lucide-react'
import { WHATSAPP_PHONE_DISPLAY, getWhatsAppQuoteUrl } from '@/lib/whatsapp'

export const WhatsAppFloatingButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [isDismissed, setIsDismissed] = useState(false)

  if (isDismissed) return null

  return (
    <div className="fixed bottom-20 md:bottom-6 right-4 md:right-6 z-40 flex flex-col items-end gap-2.5 select-none pointer-events-auto">
      
      {/* Expanded Quick Dialogue Box on Click */}
      {isOpen && (
        <div className="w-[calc(100vw-2rem)] max-w-xs sm:w-80 bg-white rounded-2xl shadow-2xl border border-border p-4 mb-1 animate-fade-in text-slate-800">
          <div className="flex items-center justify-between border-b border-border pb-3 mb-3">
            <div className="flex items-center gap-2.5">
              <div className="relative w-9 h-9 rounded-full bg-[#25D366] text-white flex items-center justify-center shadow-md flex-shrink-0">
                <MessageCircle size={20} />
                <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-400 border-2 border-white rounded-full"></span>
              </div>
              <div>
                <h4 className="text-xs font-black text-navy leading-none">RealTech Direct Sales Desk</h4>
                <p className="text-[10px] text-emerald-600 font-semibold mt-0.5 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping inline-block"></span>
                  Customer Care Online
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
              aria-label="Close dialogue"
            >
              <X size={16} />
            </button>
          </div>

          <div className="bg-slate-50 rounded-xl p-3 text-xs text-slate-600 mb-3 space-y-1.5 border border-slate-100">
            <p className="font-semibold text-navy flex items-center gap-1.5">
              <Sparkles size={14} className="text-primary" />
              Need a Custom Laptop Quote?
            </p>
            <p className="text-[11px] leading-relaxed">
              Chat directly with our hardware engineering desk on WhatsApp at <strong className="text-navy">{WHATSAPP_PHONE_DISPLAY}</strong> for customized quotes, bulk orders, and priority dispatch.
            </p>
            <div className="pt-1 flex items-center gap-1 text-[10px] text-emerald-700 font-medium">
              <ShieldCheck size={12} />
              <span>Official Care & Direct Deal: 0708 425 6460</span>
            </div>
          </div>

          <a
            href={getWhatsAppQuoteUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className="w-full py-2.5 px-4 rounded-xl bg-[#25D366] hover:bg-[#20bd5a] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-md hover:shadow-lg transition-all"
          >
            <MessageCircle size={16} />
            <span>Chat on WhatsApp ({WHATSAPP_PHONE_DISPLAY})</span>
          </a>
        </div>
      )}

      {/* Main Floating Button - Compact Circle on Mobile, Full Pill on Desktop */}
      <div className="relative group flex items-center gap-1.5">
        
        {/* Optional dismiss button on hover/tap */}
        <button
          onClick={(e) => {
            e.stopPropagation()
            setIsDismissed(true)
          }}
          className="hidden group-hover:flex items-center justify-center w-5 h-5 rounded-full bg-navy/60 hover:bg-navy text-white text-[10px] shadow-sm transition-all"
          title="Dismiss quote button"
          aria-label="Dismiss quote button"
        >
          <X size={10} />
        </button>

        {/* Glow effect */}
        <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-[#25D366] to-emerald-400 opacity-50 blur-sm group-hover:opacity-80 transition-opacity animate-pulse"></div>

        <button
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Get WhatsApp Quote & Direct Deal"
          className="relative flex items-center bg-[#25D366] hover:bg-[#20bd5a] text-white shadow-xl transition-all duration-300 transform active:scale-95 group-hover:scale-105 rounded-full p-3 md:px-4 md:py-2.5 gap-2.5"
        >
          {/* WhatsApp Icon */}
          <div className="relative flex items-center justify-center">
            <MessageCircle size={22} className="text-white fill-white" />
            <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-white"></span>
            </span>
          </div>

          {/* Text: Hidden on mobile to avoid covering buttons; visible on tablet/desktop */}
          <div className="hidden md:flex flex-col text-left pr-1 leading-tight">
            <span className="text-[9px] uppercase tracking-wider font-extrabold text-emerald-100">
              Get Quote / Direct Deal
            </span>
            <span className="text-xs font-black tracking-wide text-white">
              {WHATSAPP_PHONE_DISPLAY}
            </span>
          </div>

          {/* Mini mobile text tag */}
          <span className="md:hidden text-[10px] font-extrabold text-white pr-1">
            Quote
          </span>
        </button>
      </div>

    </div>
  )
}
