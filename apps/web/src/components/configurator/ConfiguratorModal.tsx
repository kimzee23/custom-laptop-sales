'use client'

import React, { useState } from 'react'
import Image from 'next/image'
import { 
  X, 
  Sparkles, 
  Palette, 
  Cpu, 
  HardDrive, 
  Tv, 
  Keyboard, 
  Image as ImageIcon, 
  Plus, 
  Check, 
  ShoppingBag, 
  Save, 
  SlidersHorizontal,
  Info,
  ShieldCheck,
  MessageCircle
} from 'lucide-react'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { useCartStore } from '@/stores/cartStore'
import { formatPrice } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { WHATSAPP_PHONE_DISPLAY, getWhatsAppQuoteUrl } from '@/lib/whatsapp'

const COLOR_OPTIONS = [
  { id: 'opt-color-arctic', name: 'Arctic Blue', hex: '#1769FF', price: 20000, description: 'Metallic anodized tech blue' },
  { id: 'opt-color-cloud', name: 'Cloud White', hex: '#FFFFFF', price: 15000, description: 'Ceramic matte pearl white' },
  { id: 'opt-color-silver', name: 'Pure Silver', hex: '#DCE6F5', price: 0, description: 'Standard aerospace aluminium' },
  { id: 'opt-color-midnight', name: 'Midnight Navy', hex: '#0B1F3A', price: 25000, description: 'Deep stealth matte navy' },
  { id: 'opt-color-crimson', name: 'Cyber Crimson', hex: '#D92D20', price: 30000, description: 'Bold metallic red accent' },
]

const RAM_OPTIONS = [
  { id: 'opt-ram-16', name: '16GB DDR5 5600MHz', price: 0, desc: 'Dual-channel base memory' },
  { id: 'opt-ram-32', name: '32GB DDR5 5600MHz', price: 90000, desc: 'Recommended for video editing & multitasking', badge: 'Popular' },
  { id: 'opt-ram-64', name: '64GB DDR5 6000MHz', price: 210000, desc: 'Extreme workstation & 3D render capability', badge: 'Pro' },
]

const SSD_OPTIONS = [
  { id: 'opt-ssd-1tb', name: '1TB PCIe 4.0 NVMe SSD', price: 0, desc: 'Up to 5000MB/s high-speed read' },
  { id: 'opt-ssd-2tb', name: '2TB PCIe 4.0 NVMe Pro SSD', price: 130000, desc: 'Up to 7400MB/s extreme read/write', badge: 'Recommended' },
  { id: 'opt-ssd-4tb', name: '4TB Dual NVMe Gen4 Array', price: 280000, desc: 'Maximum storage for large game libraries & footage' },
]

const GPU_OPTIONS = [
  { id: 'opt-gpu-rtx4060', name: 'NVIDIA GeForce RTX 4060 8GB', price: 0, desc: '140W Max TGP with DLSS 3.5' },
  { id: 'opt-gpu-rtx4070', name: 'NVIDIA GeForce RTX 4070 8GB', price: 320000, desc: '20% faster frame rates + AI Acceleration', badge: 'Top Pick' },
  { id: 'opt-gpu-rtx4080', name: 'NVIDIA GeForce RTX 4080 12GB', price: 680000, desc: 'Studio Max 4K gaming and hardware ray tracing' },
]

const DISPLAY_OPTIONS = [
  { id: 'opt-disp-ips', name: '16.0" QHD+ (2560x1600) 165Hz IPS', price: 0, desc: '100% sRGB anti-glare display' },
  { id: 'opt-disp-oled', name: '16.0" 3.2K (3200x2000) 120Hz OLED', price: 160000, desc: '100% DCI-P3, 500 nits HDR, Delta E < 1', badge: 'Creator Pick' },
]

const KEYBOARD_OPTIONS = [
  { id: 'opt-kb-backlit', name: 'Clean White Backlit Island Keyboard', price: 0, desc: 'Ergonomic 1.5mm key travel' },
  { id: 'opt-kb-rgb', name: 'Per-Key RGB Mechanical Switch Deck', price: 45000, desc: 'Tactile mechanical switches with customizable lighting' },
]

export const ConfiguratorModal: React.FC = () => {
  const { 
    isOpen, 
    closeConfigurator, 
    selectedProduct, 
    config, 
    breakdown, 
    setColor, 
    setRam, 
    setStorage, 
    setGpu, 
    setDisplay, 
    setKeyboard, 
    setArtwork 
  } = useConfiguratorStore()

  const { addItem } = useCartStore()

  const [activeCategoryTab, setActiveCategoryTab] = useState<'color' | 'ram' | 'storage' | 'gpu' | 'display' | 'keyboard' | 'artwork'>('color')
  const [customText, setCustomText] = useState('')
  const [artworkPosition, setArtworkPosition] = useState<'center' | 'top-right' | 'bottom-right'>('center')

  if (!isOpen || !selectedProduct) return null

  // Find active color
  const activeColor = COLOR_OPTIONS.find((c) => c.id === config.colorId) || COLOR_OPTIONS[0]

  const handleApplyArtwork = () => {
    if (customText) {
      setArtwork({
        custom_text: customText,
        position_x: artworkPosition === 'center' ? 0 : 50,
        position_y: artworkPosition === 'top-right' ? -40 : 40,
        scale: 1,
        rotation: 0,
      })
    } else {
      setArtwork(undefined)
    }
  }

  const handleAddToCart = () => {
    addItem({
      productId: selectedProduct.id,
      productTitle: `${selectedProduct.title} (Custom Build)`,
      imageUrl: selectedProduct.image_url,
      quantity: 1,
      unitPrice: breakdown.total,
      configuration: config,
      configurationSummary: {
        color: activeColor.name,
        ram: RAM_OPTIONS.find((r) => r.id === config.ramId)?.name.split(' ')[0],
        storage: SSD_OPTIONS.find((s) => s.id === config.storageId)?.name.split(' ')[0],
        gpu: GPU_OPTIONS.find((g) => g.id === config.gpuId)?.name.split('GeForce ')[1] || 'RTX 4060',
        display: DISPLAY_OPTIONS.find((d) => d.id === config.displayId)?.name.split(' ')[1],
        hasArtwork: !!config.artwork?.custom_text,
      }
    })
    closeConfigurator()
  }

  return (
    <div className="fixed inset-0 z-50 overflow-hidden flex items-center justify-center p-2 sm:p-4 lg:p-6">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-navy/70 backdrop-blur-md transition-opacity"
        onClick={closeConfigurator}
      />

      {/* Main Modal Shell */}
      <div className="relative w-full max-w-6xl max-h-[92vh] bg-white rounded-2xl shadow-2xl border border-border flex flex-col z-10 overflow-hidden">
        
        {/* Modal Top Header */}
        <div className="px-6 py-4 border-b border-border bg-primary-soft flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-primary text-white flex items-center justify-center shadow-sm">
              <SlidersHorizontal size={20} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-black text-navy font-display">
                  Custom Laptop Builder
                </h2>
                <Badge variant="primary" size="sm">LIVE PREVIEW</Badge>
              </div>
              <p className="text-xs text-muted">
                Configuring: <span className="font-bold text-navy">{selectedProduct.title}</span>
              </p>
            </div>
          </div>

          <button
            onClick={closeConfigurator}
            className="p-2 rounded-xl text-muted hover:text-navy hover:bg-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Modal Body: Split Screen */}
        <div className="flex-1 overflow-y-auto grid grid-cols-1 lg:grid-cols-12 min-h-[460px]">
          
          {/* LEFT: Dynamic Visual Laptop Preview */}
          <div className="lg:col-span-6 bg-gradient-to-b from-background to-white p-6 border-b lg:border-b-0 lg:border-r border-border flex flex-col justify-between relative">
            
            {/* Visual Header / State Badges */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span 
                  className="w-3.5 h-3.5 rounded-full border border-border shadow-sm"
                  style={{ backgroundColor: activeColor.hex }}
                />
                <span className="text-xs font-bold text-navy">{activeColor.name} Chassis</span>
              </div>
              <Badge variant="outline" size="sm">
                360° Visual Engine
              </Badge>
            </div>

            {/* Visual Canvas Display */}
            <div className="relative h-64 sm:h-80 w-full my-4 rounded-xl flex items-center justify-center bg-white border border-border shadow-inner p-4 overflow-hidden">
              
              {/* Dynamic Color Hue Tint on Laptop Frame */}
              <div 
                className="relative w-full h-full transition-all duration-500 flex items-center justify-center"
                style={{
                  filter: activeColor.id === 'opt-color-arctic' 
                    ? 'drop-shadow(0 10px 20px rgba(23, 105, 255, 0.25)) hue-rotate(0deg)'
                    : activeColor.id === 'opt-color-crimson'
                    ? 'drop-shadow(0 10px 20px rgba(217, 45, 32, 0.25)) hue-rotate(140deg)'
                    : activeColor.id === 'opt-color-midnight'
                    ? 'drop-shadow(0 10px 20px rgba(11, 31, 58, 0.35)) brightness(0.85)'
                    : activeColor.id === 'opt-color-cloud'
                    ? 'drop-shadow(0 10px 20px rgba(0,0,0,0.1)) brightness(1.15) contrast(0.95)'
                    : 'drop-shadow(0 10px 20px rgba(0,0,0,0.15))'
                }}
              >
                <Image
                  src={selectedProduct.image_url}
                  alt={selectedProduct.title}
                  fill
                  className="object-contain"
                  priority
                />
              </div>

              {/* Custom Artwork / Laser Engraving Live Overlay */}
              {config.artwork?.custom_text && (
                <div 
                  className={`absolute z-20 px-3 py-1 bg-black/60 backdrop-blur-sm text-white border border-white/40 rounded text-xs font-mono font-bold tracking-widest uppercase transition-all ${
                    artworkPosition === 'top-right' ? 'top-8 right-8' : artworkPosition === 'bottom-right' ? 'bottom-8 right-8' : 'top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'
                  }`}
                >
                  {config.artwork.custom_text}
                </div>
              )}
            </div>

            {/* Visual Control Presets & Quick Specs Bar */}
            <div className="space-y-2">
              <div className="flex flex-wrap items-center justify-between text-xs text-muted bg-white p-3 rounded-xl border border-border">
                <div className="flex items-center gap-1.5">
                  <ShieldCheck size={16} className="text-success" />
                  <span>Factory Calibrated & Tested</span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="font-bold text-navy">Base:</span>
                  <span>{formatPrice(selectedProduct.base_price)}</span>
                </div>
              </div>
            </div>

          </div>

          {/* RIGHT: Configuration Step Navigation & Options */}
          <div className="lg:col-span-6 p-6 flex flex-col justify-between bg-white overflow-y-auto">
            
            <div className="space-y-6">
              {/* Category Pills Navigation */}
              <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-2 border-b border-border">
                {[
                  { id: 'color', label: 'Color', icon: Palette },
                  { id: 'ram', label: 'RAM', icon: Cpu },
                  { id: 'storage', label: 'Storage', icon: HardDrive },
                  { id: 'gpu', label: 'GPU', icon: Sparkles },
                  { id: 'display', label: 'Display', icon: Tv },
                  { id: 'keyboard', label: 'Keyboard', icon: Keyboard },
                  { id: 'artwork', label: 'Artwork', icon: ImageIcon },
                ].map((tab) => {
                  const Icon = tab.icon
                  const isActive = activeCategoryTab === tab.id
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveCategoryTab(tab.id as any)}
                      className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-bold transition-all whitespace-nowrap ${
                        isActive
                          ? 'bg-primary text-white shadow-sm'
                          : 'bg-primary-soft text-navy hover:bg-primary-light hover:text-primary'
                      }`}
                    >
                      <Icon size={14} />
                      <span>{tab.label}</span>
                    </button>
                  )
                })}
              </div>

              {/* 1. COLOR OPTIONS */}
              {activeCategoryTab === 'color' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Select Chassis Finish</h3>
                    <p className="text-xs text-muted">Premium metallic and ceramic powder-coated exterior</p>
                  </div>
                  <div className="space-y-2.5">
                    {COLOR_OPTIONS.map((c) => {
                      const isSelected = config.colorId === c.id
                      return (
                        <div
                          key={c.id}
                          onClick={() => setColor(c.id)}
                          className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer flex items-center justify-between ${
                            isSelected
                              ? 'border-primary bg-primary-soft/40 shadow-sm'
                              : 'border-border hover:border-primary/40 bg-white'
                          }`}
                        >
                          <div className="flex items-center gap-3">
                            <span
                              className="w-6 h-6 rounded-full border border-border shadow-sm flex items-center justify-center"
                              style={{ backgroundColor: c.hex }}
                            >
                              {isSelected && <Check size={12} className={c.hex === '#FFFFFF' ? 'text-navy' : 'text-white'} />}
                            </span>
                            <div>
                              <span className="text-xs font-bold text-navy block">{c.name}</span>
                              <span className="text-[11px] text-muted">{c.description}</span>
                            </div>
                          </div>
                          <span className="text-xs font-bold text-navy">
                            {c.price === 0 ? 'Included' : `+${formatPrice(c.price)}`}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* 2. RAM OPTIONS */}
              {activeCategoryTab === 'ram' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Select Memory (RAM)</h3>
                    <p className="text-xs text-muted">High-bandwidth DDR5 dual-channel architecture</p>
                  </div>
                  <div className="space-y-2.5">
                    {RAM_OPTIONS.map((r) => {
                      const isSelected = config.ramId === r.id
                      return (
                        <div
                          key={r.id}
                          onClick={() => setRam(r.id)}
                          className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer flex items-center justify-between ${
                            isSelected
                              ? 'border-primary bg-primary-soft/40 shadow-sm'
                              : 'border-border hover:border-primary/40 bg-white'
                          }`}
                        >
                          <div className="space-y-0.5">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-navy">{r.name}</span>
                              {r.badge && <Badge variant="primary" size="sm">{r.badge}</Badge>}
                            </div>
                            <span className="text-[11px] text-muted block">{r.desc}</span>
                          </div>
                          <span className="text-xs font-bold text-navy">
                            {r.price === 0 ? 'Included' : `+${formatPrice(r.price)}`}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* 3. STORAGE OPTIONS */}
              {activeCategoryTab === 'storage' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Select Solid State Drive (NVMe)</h3>
                    <p className="text-xs text-muted">PCIe 4.0 ultra fast NVMe storage for games and files</p>
                  </div>
                  <div className="space-y-2.5">
                    {SSD_OPTIONS.map((s) => {
                      const isSelected = config.storageId === s.id
                      return (
                        <div
                          key={s.id}
                          onClick={() => setStorage(s.id)}
                          className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer flex items-center justify-between ${
                            isSelected
                              ? 'border-primary bg-primary-soft/40 shadow-sm'
                              : 'border-border hover:border-primary/40 bg-white'
                          }`}
                        >
                          <div className="space-y-0.5">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-navy">{s.name}</span>
                              {s.badge && <Badge variant="primary" size="sm">{s.badge}</Badge>}
                            </div>
                            <span className="text-[11px] text-muted block">{s.desc}</span>
                          </div>
                          <span className="text-xs font-bold text-navy">
                            {s.price === 0 ? 'Included' : `+${formatPrice(s.price)}`}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* 4. GPU OPTIONS */}
              {activeCategoryTab === 'gpu' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Select Dedicated Graphics</h3>
                    <p className="text-xs text-muted">NVIDIA RTX 40-Series with DLSS 3.5 frame generation</p>
                  </div>
                  <div className="space-y-2.5">
                    {GPU_OPTIONS.map((g) => {
                      const isSelected = config.gpuId === g.id
                      return (
                        <div
                          key={g.id}
                          onClick={() => setGpu(g.id)}
                          className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer flex items-center justify-between ${
                            isSelected
                              ? 'border-primary bg-primary-soft/40 shadow-sm'
                              : 'border-border hover:border-primary/40 bg-white'
                          }`}
                        >
                          <div className="space-y-0.5">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-navy">{g.name}</span>
                              {g.badge && <Badge variant="discount" size="sm">{g.badge}</Badge>}
                            </div>
                            <span className="text-[11px] text-muted block">{g.desc}</span>
                          </div>
                          <span className="text-xs font-bold text-navy">
                            {g.price === 0 ? 'Included' : `+${formatPrice(g.price)}`}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* 5. DISPLAY OPTIONS */}
              {activeCategoryTab === 'display' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Select Display Panel</h3>
                    <p className="text-xs text-muted">Smooth 165Hz esports IPS or Color-Accurate 3.2K OLED</p>
                  </div>
                  <div className="space-y-2.5">
                    {DISPLAY_OPTIONS.map((d) => {
                      const isSelected = config.displayId === d.id
                      return (
                        <div
                          key={d.id}
                          onClick={() => setDisplay(d.id)}
                          className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer flex items-center justify-between ${
                            isSelected
                              ? 'border-primary bg-primary-soft/40 shadow-sm'
                              : 'border-border hover:border-primary/40 bg-white'
                          }`}
                        >
                          <div className="space-y-0.5">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-navy">{d.name}</span>
                              {d.badge && <Badge variant="primary" size="sm">{d.badge}</Badge>}
                            </div>
                            <span className="text-[11px] text-muted block">{d.desc}</span>
                          </div>
                          <span className="text-xs font-bold text-navy">
                            {d.price === 0 ? 'Included' : `+${formatPrice(d.price)}`}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* 6. KEYBOARD OPTIONS */}
              {activeCategoryTab === 'keyboard' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Select Keyboard Lighting & Deck</h3>
                    <p className="text-xs text-muted">Ergonomic key travel with custom RGB lighting options</p>
                  </div>
                  <div className="space-y-2.5">
                    {KEYBOARD_OPTIONS.map((k) => {
                      const isSelected = config.keyboardId === k.id
                      return (
                        <div
                          key={k.id}
                          onClick={() => setKeyboard(k.id)}
                          className={`p-3.5 rounded-xl border-2 transition-all cursor-pointer flex items-center justify-between ${
                            isSelected
                              ? 'border-primary bg-primary-soft/40 shadow-sm'
                              : 'border-border hover:border-primary/40 bg-white'
                          }`}
                        >
                          <div className="space-y-0.5">
                            <span className="text-xs font-bold text-navy">{k.name}</span>
                            <span className="text-[11px] text-muted block">{k.desc}</span>
                          </div>
                          <span className="text-xs font-bold text-navy">
                            {k.price === 0 ? 'Included' : `+${formatPrice(k.price)}`}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* 7. CUSTOM ARTWORK / ENGRAVING */}
              {activeCategoryTab === 'artwork' && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <h3 className="text-sm font-bold text-navy">Customize Lid Artwork & Laser Engraving</h3>
                    <p className="text-xs text-muted">Add custom text or your personal logo (+₦35,000)</p>
                  </div>

                  <div className="space-y-3 bg-primary-soft/40 p-4 rounded-xl border border-border">
                    <div>
                      <label className="text-xs font-bold text-navy block mb-1">
                        Laser Engraved Text / Gamertag
                      </label>
                      <input
                        type="text"
                        maxLength={24}
                        value={customText}
                        onChange={(e) => setCustomText(e.target.value)}
                        placeholder="e.g. REAL-CYBER-99"
                        className="w-full h-10 px-3 rounded-lg border border-border text-xs text-navy focus:border-primary focus:outline-none bg-white uppercase font-mono"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-navy block mb-1">
                        Position on Laptop Lid
                      </label>
                      <div className="grid grid-cols-3 gap-2">
                        {['center', 'top-right', 'bottom-right'].map((pos) => (
                          <button
                            key={pos}
                            type="button"
                            onClick={() => setArtworkPosition(pos as any)}
                            className={`py-1.5 text-[11px] font-bold rounded-lg border capitalize ${
                              artworkPosition === pos
                                ? 'bg-primary text-white border-primary'
                                : 'bg-white text-navy border-border hover:border-primary'
                            }`}
                          >
                            {pos.replace('-', ' ')}
                          </button>
                        ))}
                      </div>
                    </div>

                    <Button
                      variant="primary"
                      size="sm"
                      onClick={handleApplyArtwork}
                      className="w-full text-xs font-bold"
                    >
                      {customText ? 'Apply Custom Engraving (+₦35,000)' : 'Clear Custom Engraving'}
                    </Button>
                  </div>
                </div>
              )}
            </div>

            {/* Dynamic Authoritative Price Breakdown & Actions */}
            <div className="pt-6 mt-6 border-t border-border space-y-4">
              
              {/* Dynamic Price Breakdown Summary */}
              <div className="bg-background p-3.5 rounded-xl border border-border space-y-1.5 text-xs">
                <div className="flex justify-between text-muted">
                  <span>Base Laptop Price</span>
                  <span className="font-semibold text-navy">{formatPrice(breakdown.basePrice)}</span>
                </div>
                {breakdown.items.map((item, idx) => (
                  <div key={idx} className="flex justify-between text-muted">
                    <span>{item.name}</span>
                    <span className="font-semibold text-primary">+{formatPrice(item.modifier)}</span>
                  </div>
                ))}
                <div className="flex justify-between text-sm font-extrabold text-navy pt-2 border-t border-border">
                  <span>Total Calculated Price</span>
                  <span className="text-lg text-primary">{formatPrice(breakdown.total)}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-2 gap-3">
                <Button
                  variant="outline"
                  size="md"
                  onClick={() => alert('Configuration build saved to your account!')}
                  className="gap-1.5 text-xs font-bold"
                >
                  <Save size={16} />
                  <span>Save Build</span>
                </Button>

                <Button
                  variant="primary"
                  size="md"
                  onClick={handleAddToCart}
                  className="gap-1.5 text-xs font-extrabold bg-primary hover:bg-primary-hover shadow-md"
                >
                  <ShoppingBag size={16} />
                  <span>ADD TO CART</span>
                </Button>
              </div>

              {/* Direct Deal WhatsApp Quote Button */}
              <a
                href={getWhatsAppQuoteUrl({
                  productTitle: selectedProduct?.title,
                  price: breakdown.total,
                  specsSummary: breakdown.items.map(i => i.name).join(', ')
                })}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-2.5 px-4 rounded-xl bg-[#25D366] hover:bg-[#20bd5a] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm hover:shadow-md transition-all"
              >
                <MessageCircle size={16} className="fill-white" />
                <span>Get Instant Quote on WhatsApp ({WHATSAPP_PHONE_DISPLAY})</span>
              </a>

            </div>

          </div>

        </div>

      </div>
    </div>
  )
}
