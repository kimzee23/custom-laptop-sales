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

        <div className="flex items-center gap-6 text-[11px] text-gray-300">
          <div className="flex items-center gap-1.5">
            <Cpu size={13} className="text-primary-sky" />
            <span>Instant Custom Laptop Pricing Engine</span>
          </div>
          <div className="hidden md:flex items-center gap-1.5">
            <ShieldCheck size={13} className="text-success" />
            <span>2-Year Official Manufacturer Warranty</span>
          </div>
        </div>
      </div>
    </div>
  )
}
