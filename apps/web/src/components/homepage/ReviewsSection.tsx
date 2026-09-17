import React from 'react'
import { RatingStars } from '@/components/ui/RatingStars'
import { CheckCircle2, Quote } from 'lucide-react'

const REVIEWS = [
  {
    author: 'Emeka O.',
    location: 'Lagos, Nigeria',
    role: 'Lead 3D Animator & Game Dev',
    product: 'TitanForge Predator 16 (Configured with 64GB RAM & RTX 4080)',
    rating: 5.0,
    date: '3 days ago',
    comment:
      'Configuring the laptop with 64GB DDR5 and custom lid artwork was seamless. Seeing the price update instantly before adding to cart gave me total transparency. The machine runs Blender renders like a desktop powerhouse!',
  },
  {
    author: 'Amina B.',
    location: 'Abuja, Nigeria',
    role: 'Senior Software Architect',
    product: 'AeroCraft StudioMaster 16 OLED',
    rating: 5.0,
    date: '1 week ago',
    comment:
      'The OLED screen is gorgeous for frontend color testing. Fast delivery to Abuja in 48 hours and packaging was fortress-grade. RealTech is easily the best tech store in the country.',
  },
  {
    author: 'Tunde A.',
    location: 'Port Harcourt, Nigeria',
    role: 'Data Science Researcher',
    product: 'Zenith CampusBook Slim 14',
    rating: 4.9,
    date: '2 weeks ago',
    comment:
      'Battery lasts my full workday without touching the charger. Keyboard tactile feedback is top tier. Upgraded to 1TB NVMe during the build step with zero hassle.',
  },
]

export const ReviewsSection: React.FC = () => {
  return (
    <section className="py-14 bg-white border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10">
          <div>
            <div className="text-xs font-bold text-primary tracking-wider uppercase mb-1">
              Verified Buyer Feedback
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-navy font-display tracking-tight">
              Customer Reviews & Experiences
            </h2>
          </div>
          <div className="flex items-center gap-2 mt-2 sm:mt-0">
            <RatingStars rating={4.9} reviewCount={2400} />
            <span className="text-xs font-bold text-success bg-success-light px-2 py-0.5 rounded-full">
              99.2% Satisfaction Rate
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {REVIEWS.map((rev, idx) => (
            <div
              key={idx}
              className="bg-background rounded-card border border-border p-6 shadow-sm hover:shadow-card transition-all flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex justify-between items-start">
                  <RatingStars rating={rev.rating} showCount={false} />
                  <Quote size={20} className="text-primary/30" />
                </div>

                <p className="text-xs text-foreground leading-relaxed italic">
                  &ldquo;{rev.comment}&rdquo;
                </p>
              </div>

              <div className="pt-4 mt-4 border-t border-border space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-navy">{rev.author}</span>
                  <span className="flex items-center gap-1 text-[11px] text-success font-medium">
                    <CheckCircle2 size={12} />
                    Verified Purchase
                  </span>
                </div>
                <div className="text-[11px] text-muted">{rev.role} • {rev.location}</div>
                <div className="text-[10px] text-primary font-semibold truncate">
                  {rev.product}
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  )
}
