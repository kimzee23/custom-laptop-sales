'use client'

import React, { useState } from 'react'
import { MessageCircle, Phone, X, ShieldCheck, Sparkles } from 'lucide-react'
import { WHATSAPP_PHONE_DISPLAY, getWhatsAppQuoteUrl } from '@/lib/whatsapp'

export const WhatsAppFloatingButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)

  const handleOpenWhatsApp = () => {
    window.open(getWhatsAppQuoteUrl(), '_blank', 'noopener,noreferrer')
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3 select-none">
      
      {/* Expanded Quick Dialogue Box on Click */}
      {isOpen && (
        <div className="w-80 bg-white rounded-2xl shadow-2xl border border-border p-4 mb-1 animate-fade-in text-slate-800">
          <div className="flex items-center justify-between border-b border-border pb-3 mb-3">
            <div className="flex items-center gap-2.5">
              <div className="relative w-9 h-9 rounded-full bg-[#25D366] text-white flex items-center justify-center shadow-md">
                <MessageCircle size={20} />
                <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-400 border-2 border-white rounded-full"></span>
              </div>
              <div>
                <h4 className="text-xs font-black text-navy leading-none">RealTech Customer Care</h4>
                <p className="text-[11px] text-emerald-600 font-semibold mt-0.5 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping inline-block"></span>
                  Online | Direct Deals Active
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
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
              Chat directly with our hardware engineering sales desk on WhatsApp at <strong className="text-navy">{WHATSAPP_PHONE_DISPLAY}</strong> for customized quotes, discounts, and immediate nationwide delivery.
            </p>
            <div className="pt-1 flex items-center gap-1 text-[10px] text-emerald-700 font-medium">
              <ShieldCheck size={12} />
              <span>Official Direct Deal Desk</span>
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

      {/* Main Bottom Corner Floating Button */}
      <div className="relative group">
        {/* Glowing aura effect */}
        <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-[#25D366] to-emerald-400 opacity-60 blur-sm group-hover:opacity-100 transition-opacity animate-pulse"></div>

        <button
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Get WhatsApp Quote & Direct Deal"
          className="relative flex items-center gap-2.5 bg-[#25D366] hover:bg-[#20bd5a] text-white px-4 py-3 rounded-full shadow-2xl transition-all duration-300 transform active:scale-95 group-hover:scale-105"
        >
          <div className="relative flex items-center justify-center">
            <MessageCircle size={24} className="text-white fill-white" />
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
            </span>
          </div>

          <div className="flex flex-col text-left pr-1">
            <span className="text-[10px] uppercase tracking-wider font-extrabold text-emerald-100 leading-tight">
              Get Quote / Direct Deal
            </span>
            <span className="text-xs font-black tracking-wide text-white leading-tight">
              {WHATSAPP_PHONE_DISPLAY}
            </span>
          </div>
        </button>
      </div>

    </div>
  )
}
