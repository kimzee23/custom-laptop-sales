import React from 'react'
import { ShieldCheck, Truck, Cpu, Award, RefreshCw, Headphones } from 'lucide-react'

export const TrustSection: React.FC = () => {
  const TRUST_ITEMS = [
    {
      icon: ShieldCheck,
      title: '100% Genuine & Verified Hardware',
      description: 'Factory-sealed original chips, authentic Intel/AMD CPUs, and NVIDIA GPUs.',
    },
    {
      icon: Cpu,
      title: 'Precision Benchmarked & Tested',
      description: 'Every custom laptop undergoes 24-hour stress and thermal quality control before delivery.',
    },
    {
      icon: Truck,
      title: 'Insured Tracked Delivery',
      description: 'Nationwide expedited logistics with door-to-door insurance and real-time status.',
    },
    {
      icon: Award,
      title: '2-Year Direct Warranty',
      description: 'Comprehensive hardware and component support backed by certified technical teams.',
    },
    {
      icon: RefreshCw,
      title: '7-Day Return Guarantee',
      description: 'Transparent return policy if hardware specifications do not match your exact order.',
    },
    {
      icon: Headphones,
      title: 'Dedicated Engineering Support',
      description: 'Direct phone & chat access to hardware specialists to assist your build decisions.',
    },
  ]

  return (
    <section className="py-14 bg-background border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-2xl mx-auto mb-10">
          <div className="text-xs font-bold text-primary tracking-wider uppercase mb-1">
            Why Shop With RealTech
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-navy font-display tracking-tight">
            Built on Trust, Performance & Peace of Mind
          </h2>
          <p className="text-xs sm:text-sm text-muted mt-2">
            The standard in high-performance laptops and custom machine builds across Nigeria
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {TRUST_ITEMS.map((item, idx) => {
            const Icon = item.icon
            return (
              <div
                key={idx}
                className="bg-white rounded-card border border-border p-6 shadow-sm hover:border-primary transition-all flex gap-4 items-start"
              >
                <div className="p-3 rounded-xl bg-primary-soft text-primary flex-shrink-0">
                  <Icon size={24} />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-navy mb-1">{item.title}</h3>
                  <p className="text-xs text-muted leading-relaxed">{item.description}</p>
                </div>
              </div>
            )
          })}
        </div>

      </div>
    </section>
  )
}
