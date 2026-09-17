import React from 'react'
import { Truck, Cpu, ShieldCheck } from 'lucide-react'

export const AnnouncementBar: React.FC = () => {
  return (
    <div className="bg-navy text-white text-xs py-2 px-4 border-b border-navy-light select-none">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-center sm:text-left">
        <div className="flex items-center gap-2">
          <Truck size={14} className="text-primary-sky" />
          <span className="font-medium">
            Free Nationwide Delivery on orders over ₦500,000
          </span>
        </div>

        <div className="flex items-center gap-4 text-[11px] text-gray-300">
          <a
            href="https://wa.me/2347084256460?text=Hello%20RealTech!%20I%20would%20like%20to%20get%20a%20quote%20for%20a%20custom%20laptop%20or%20make%20a%20direct%20deal."
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 hover:text-white hover:bg-emerald-500/30 transition-colors font-semibold"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Customer Care & Direct Deal: <strong>0708 425 6460</strong></span>
          </a>
          <div className="hidden lg:flex items-center gap-1.5">
            <Cpu size={13} className="text-primary-sky" />
            <span>Instant Custom Laptop Pricing Engine</span>
          </div>
          <div className="hidden md:flex items-center gap-1.5">
            <ShieldCheck size={13} className="text-success" />
            <span>2-Year Warranty</span>
          </div>
        </div>
      </div>
    </div>
  )
}
