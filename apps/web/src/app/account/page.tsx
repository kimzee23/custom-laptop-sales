'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { 
  User, Mail, Phone, MapPin, Package, SlidersHorizontal, ShieldCheck, 
  KeyRound, LogOut, Plus, Trash2, Edit3, CheckCircle2, AlertCircle, 
  ArrowRight, ExternalLink, Sparkles, Star, Cpu, HardDrive, ShoppingBag, 
  Clock, ShieldAlert, Award, RefreshCw
} from 'lucide-react'
import { useAuthStore, DEMO_ACCOUNTS } from '@/stores/authStore'
import { useCartStore } from '@/stores/cartStore'
import { useConfiguratorStore } from '@/stores/configuratorStore'
import { useOrderTrackingStore } from '@/stores/orderTrackingStore'
import { StoreHeader } from '@/components/layout/StoreHeader'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { formatPrice } from '@/lib/utils'

type AccountTab = 'profile' | 'builds' | 'addresses' | 'orders' | 'security'

export default function AccountPage() {
  const router = useRouter()
  const { 
    user, isAuthenticated, logout, updateProfile, 
    addAddress, deleteAddress, setDefaultAddress, removeSavedBuild 
  } = useAuthStore()
  
  const { addItem, setIsOpen: setCartOpen } = useCartStore()
  const { openConfigurator } = useConfiguratorStore()
  const { openTracking } = useOrderTrackingStore()

  const [activeTab, setActiveTab] = useState<AccountTab>('profile')
  
  // Profile Form state
  const [profileName, setProfileName] = useState(user?.name || '')
  const [profilePhone, setProfilePhone] = useState(user?.phone || '')
  const [profileSavedFeedback, setProfileSavedFeedback] = useState(false)

  // Address Modal state
  const [showAddAddressModal, setShowAddAddressModal] = useState(false)
  const [newAddress, setNewAddress] = useState({
    title: 'Home',
    fullName: user?.name || '',
    phone: user?.phone || '08031234567',
    street: '',
    city: 'Lagos',
    state: 'Lagos State',
    isDefault: true
  })

  // Security Form state
  const [currentPassword, setCurrentPassword] = useState('')
  const [newSecurityPassword, setNewSecurityPassword] = useState('')
  const [confirmSecurityPassword, setConfirmSecurityPassword] = useState('')
  const [securitySuccess, setSecuritySuccess] = useState<string | null>(null)
  const [securityError, setSecurityError] = useState<string | null>(null)

  // If user is not logged in, show polished sign-in prompt
  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-[80vh] flex flex-col">
        <StoreHeader />
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="max-w-md w-full bg-white rounded-3xl p-8 border border-border shadow-card text-center space-y-6">
            <div className="w-16 h-16 rounded-2xl bg-primary-soft text-primary flex items-center justify-center mx-auto shadow-sm">
              <User size={32} />
            </div>
            <div className="space-y-2">
              <h2 className="text-2xl font-black text-navy font-display">
                Sign in to your account
              </h2>
              <p className="text-xs sm:text-sm text-muted leading-relaxed">
                Access your saved 3D custom laptop configurations, order tracking history, addresses, and 2-Year warranty status.
              </p>
            </div>

            <div className="space-y-3">
              <Link href="/auth/login?callbackUrl=/account">
                <Button variant="primary" size="lg" className="w-full font-bold gap-2">
                  <span>Sign In as Customer</span>
                  <ArrowRight size={16} />
                </Button>
              </Link>

              <Link href="/auth/register">
                <Button variant="secondary" size="md" className="w-full font-bold">
                  Create Free Account
                </Button>
              </Link>
            </div>

            {/* Quick Demo Login Option */}
            <div className="pt-4 border-t border-border">
              <span className="text-[11px] font-bold text-muted uppercase tracking-wider block mb-2">
                Or One-Click Demo Customer:
              </span>
              <div className="flex flex-col gap-2">
                {DEMO_ACCOUNTS.map((demo) => (
                  <button
                    key={demo.email}
                    onClick={async () => {
                      await useAuthStore.getState().login({
                        email: demo.email,
                        password: demo.pass,
                        rememberMe: true
                      })
                    }}
                    className="p-2.5 rounded-xl bg-primary-soft hover:bg-primary/10 border border-primary/20 text-xs font-semibold text-navy flex items-center justify-between transition-colors"
                  >
                    <span>{demo.user.name}</span>
                    <span className="text-primary font-bold">Sign In &rarr;</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const handleUpdateProfile = (e: React.FormEvent) => {
    e.preventDefault()
    updateProfile({
      name: profileName,
      phone: profilePhone
    })
    setProfileSavedFeedback(true)
    setTimeout(() => setProfileSavedFeedback(false), 3000)
  }

  const handleCreateAddress = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newAddress.street.trim()) return
    addAddress(newAddress)
    setShowAddAddressModal(false)
    setNewAddress({
      title: 'Home',
      fullName: user.name,
      phone: user.phone || '',
      street: '',
      city: 'Lagos',
      state: 'Lagos State',
      isDefault: false
    })
  }

  const handleUpdateSecurity = (e: React.FormEvent) => {
    e.preventDefault()
    setSecurityError(null)
    setSecuritySuccess(null)

    if (newSecurityPassword.length < 6) {
      setSecurityError('New password must be at least 6 characters.')
      return
    }
    if (newSecurityPassword !== confirmSecurityPassword) {
      setSecurityError('Passwords do not match.')
      return
    }

    setSecuritySuccess('Password successfully updated!')
    setCurrentPassword('')
    setNewSecurityPassword('')
    setConfirmSecurityPassword('')
    setTimeout(() => setSecuritySuccess(null), 4000)
  }

  const handleAddSavedBuildToCart = (build: any) => {
    addItem({
      productId: build.productId,
      productTitle: build.title || build.productTitle,
      imageUrl: build.imageUrl,
      unitPrice: build.totalPrice,
      quantity: 1,
      configuration: build.configuration,
      configurationSummary: {
        color: build.specsSummary?.color,
        ram: build.specsSummary?.ram,
        storage: build.specsSummary?.storage,
        gpu: build.specsSummary?.gpu,
      }
    })
    setCartOpen(true)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <StoreHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
        {/* User Hero Banner */}
        <div className="bg-gradient-to-r from-navy via-navy-light to-primary rounded-3xl p-6 sm:p-8 text-white shadow-card mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-80 h-80 bg-primary-sky/20 rounded-full blur-3xl pointer-events-none" />
          
          <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="relative w-16 h-16 rounded-2xl bg-white/10 border-2 border-white/20 p-1 flex-shrink-0 flex items-center justify-center font-bold text-2xl text-primary-sky overflow-hidden">
                {user.avatarUrl ? (
                  <Image src={user.avatarUrl} alt={user.name} fill className="object-cover" />
                ) : (
                  <span>{user.name.charAt(0)}</span>
                )}
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <h1 className="text-xl sm:text-2xl font-black tracking-tight font-display">
                    {user.name}
                  </h1>
                  <Badge variant="primary" size="sm" className="bg-primary text-white border-0">
                    Verified Customer
                  </Badge>
                  <Badge variant="success" size="sm" className="bg-emerald-500/20 text-emerald-300 border-emerald-500/30">
                    2-Yr Warranty Active
                  </Badge>
                </div>
                <div className="flex items-center gap-4 text-xs text-slate-300 flex-wrap">
                  <span className="flex items-center gap-1.5">
                    <Mail size={13} /> {user.email}
                  </span>
                  {user.phone && (
                    <span className="flex items-center gap-1.5">
                      <Phone size={13} /> {user.phone}
                    </span>
                  )}
                  <span>Member since {user.joinedAt}</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  logout()
                  router.push('/')
                }}
                className="border-white/30 text-white hover:bg-white/10 gap-1.5"
              >
                <LogOut size={14} />
                <span>Sign Out</span>
              </Button>
            </div>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-white/10">
            <div className="bg-white/5 rounded-xl p-3 border border-white/10">
              <div className="text-[11px] text-slate-300">Reward Points</div>
              <div className="text-lg font-black text-primary-sky">{user.rewardPoints} pts</div>
            </div>
            <div className="bg-white/5 rounded-xl p-3 border border-white/10">
              <div className="text-[11px] text-slate-300">Saved Custom Builds</div>
              <div className="text-lg font-black text-white">{user.savedBuilds?.length || 0} Builds</div>
            </div>
            <div className="bg-white/5 rounded-xl p-3 border border-white/10">
              <div className="text-[11px] text-slate-300">Saved Addresses</div>
              <div className="text-lg font-black text-white">{user.addresses.length} Locations</div>
            </div>
            <div className="bg-white/5 rounded-xl p-3 border border-white/10">
              <div className="text-[11px] text-slate-300">VIP Priority Support</div>
              <div className="text-lg font-black text-emerald-400">Included</div>
            </div>
          </div>
        </div>

        {/* Account Tabs & Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Navigation Sidebar */}
          <div className="lg:col-span-3 bg-white rounded-2xl border border-border p-3 shadow-card space-y-1">
            <button
              onClick={() => setActiveTab('profile')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-bold transition-all text-left ${
                activeTab === 'profile'
                  ? 'bg-primary text-white shadow-md'
                  : 'text-navy hover:bg-primary-soft hover:text-primary'
              }`}
            >
              <User size={16} />
              <span>Profile Information</span>
            </button>

            <button
              onClick={() => setActiveTab('builds')}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl text-xs font-bold transition-all text-left ${
                activeTab === 'builds'
                  ? 'bg-primary text-white shadow-md'
                  : 'text-navy hover:bg-primary-soft hover:text-primary'
              }`}
            >
              <div className="flex items-center gap-3">
                <SlidersHorizontal size={16} />
                <span>Saved Custom Builds</span>
              </div>
              <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                activeTab === 'builds' ? 'bg-white/20 text-white' : 'bg-primary-soft text-primary'
              }`}>
                {user.savedBuilds?.length || 0}
              </span>
            </button>

            <button
              onClick={() => setActiveTab('addresses')}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-xl text-xs font-bold transition-all text-left ${
                activeTab === 'addresses'
                  ? 'bg-primary text-white shadow-md'
                  : 'text-navy hover:bg-primary-soft hover:text-primary'
              }`}
            >
              <div className="flex items-center gap-3">
                <MapPin size={16} />
                <span>Delivery Addresses</span>
              </div>
              <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                activeTab === 'addresses' ? 'bg-white/20 text-white' : 'bg-primary-soft text-primary'
              }`}>
                {user.addresses.length}
              </span>
            </button>

            <button
              onClick={() => setActiveTab('orders')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-bold transition-all text-left ${
                activeTab === 'orders'
                  ? 'bg-primary text-white shadow-md'
                  : 'text-navy hover:bg-primary-soft hover:text-primary'
              }`}
            >
              <Package size={16} />
              <span>Orders & Tracking</span>
            </button>

            <button
              onClick={() => setActiveTab('security')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-bold transition-all text-left ${
                activeTab === 'security'
                  ? 'bg-primary text-white shadow-md'
                  : 'text-navy hover:bg-primary-soft hover:text-primary'
              }`}
            >
              <KeyRound size={16} />
              <span>Security & Password</span>
            </button>
          </div>

          {/* Main Tab Content */}
          <div className="lg:col-span-9 bg-white rounded-2xl border border-border p-6 sm:p-8 shadow-card">
            
            {/* TAB 1: Profile Info */}
            {activeTab === 'profile' && (
              <div className="space-y-6 animate-fade-in">
                <div className="flex items-center justify-between pb-4 border-b border-border">
                  <div>
                    <h2 className="text-lg font-black text-navy">Personal Profile</h2>
                    <p className="text-xs text-muted">Update your contact details for deliveries and order updates.</p>
                  </div>
                  <Badge variant="navy" size="sm">Customer ID: {user.id}</Badge>
                </div>

                {profileSavedFeedback && (
                  <div className="p-3 rounded-xl bg-success-light border border-success/30 text-success text-xs flex items-center gap-2 animate-fade-in">
                    <CheckCircle2 size={16} />
                    <span>Your profile information has been saved successfully!</span>
                  </div>
                )}

                <form onSubmit={handleUpdateProfile} className="space-y-4 max-w-xl">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-navy">Full Name</label>
                    <input
                      type="text"
                      value={profileName}
                      onChange={(e) => setProfileName(e.target.value)}
                      className="w-full h-11 px-4 rounded-xl border border-border bg-background text-sm text-foreground focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-navy">Email Address</label>
                    <input
                      type="email"
                      value={user.email}
                      disabled
                      className="w-full h-11 px-4 rounded-xl border border-border bg-slate-100 text-sm text-muted cursor-not-allowed"
                    />
                    <span className="text-[11px] text-muted">Email is linked to your order receipts and cannot be modified directly.</span>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-navy">Phone Number (for Courier Calls)</label>
                    <input
                      type="tel"
                      value={profilePhone}
                      onChange={(e) => setProfilePhone(e.target.value)}
                      placeholder="e.g. 0803 123 4567"
                      className="w-full h-11 px-4 rounded-xl border border-border bg-background text-sm text-foreground focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
                    />
                  </div>

                  <div className="pt-2">
                    <Button type="submit" variant="primary" size="md" className="font-bold">
                      Save Profile Changes
                    </Button>
                  </div>
                </form>
              </div>
            )}

            {/* TAB 2: Saved Custom Builds */}
            {activeTab === 'builds' && (
              <div className="space-y-6 animate-fade-in">
                <div className="flex items-center justify-between pb-4 border-b border-border">
                  <div>
                    <h2 className="text-lg font-black text-navy">Saved Custom Builds</h2>
                    <p className="text-xs text-muted">Your custom configured laptops ready for instant 3D customization or checkout.</p>
                  </div>
                  <Link href="#builder-section">
                    <Button 
                      variant="secondary" 
                      size="sm" 
                      className="gap-1.5 font-bold"
                      onClick={() => openConfigurator({
                        id: 'prod-titanforge-predator-16',
                        title: 'TitanForge Predator 16 Pro Gaming Laptop',
                        slug: 'titanforge-predator-16-pro',
                        base_price: 1450000,
                        image_url: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80',
                        gallery_images: [],
                        rating: 4.9,
                        review_count: 48,
                        stock: 18,
                        is_featured: true,
                        is_flash_deal: true,
                        is_best_seller: true,
                        is_customizable: true,
                        specs: {
                          processor: 'Intel Core i9-14900HX',
                          ram: '32GB DDR5',
                          storage: '1TB NVMe',
                          gpu: 'RTX 4070 8GB',
                        }
                      })}
                    >
                      <Plus size={14} />
                      <span>New Custom Build</span>
                    </Button>
                  </Link>
                </div>

                {(!user.savedBuilds || user.savedBuilds.length === 0) ? (
                  <div className="text-center py-12 space-y-4">
                    <div className="w-14 h-14 rounded-2xl bg-primary-soft text-primary flex items-center justify-center mx-auto">
                      <SlidersHorizontal size={28} />
                    </div>
                    <div className="space-y-1">
                      <h3 className="text-base font-bold text-navy">No saved configurations yet</h3>
                      <p className="text-xs text-muted max-w-sm mx-auto">
                        Use our real-time 3D Configurator to customize RAM, GPU, SSD, color finish, and custom artwork!
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {user.savedBuilds.map((build) => (
                      <div
                        key={build.id}
                        className="rounded-2xl border border-border p-4 bg-background hover:border-primary/40 transition-all space-y-3 relative group"
                      >
                        <div className="flex gap-4">
                          <div className="relative w-24 h-20 bg-white rounded-xl border border-border p-1 flex-shrink-0">
                            <Image
                              src={build.imageUrl || 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=400&q=80'}
                              alt={build.title}
                              fill
                              className="object-contain"
                            />
                          </div>
                          <div className="space-y-1 min-w-0 flex-1">
                            <h4 className="text-sm font-bold text-navy truncate">
                              {build.title}
                            </h4>
                            <p className="text-xs text-primary font-black">
                              {formatPrice(build.totalPrice)}
                            </p>
                            <span className="text-[10px] text-muted block">
                              Saved on {build.savedAt}
                            </span>
                          </div>
                        </div>

                        {/* Specs badges */}
                        <div className="flex flex-wrap gap-1 text-[10px] text-slate-700 pt-1">
                          {build.specsSummary?.cpu && (
                            <span className="px-2 py-0.5 rounded-md bg-white border border-border font-medium">
                              {build.specsSummary.cpu}
                            </span>
                          )}
                          {build.specsSummary?.ram && (
                            <span className="px-2 py-0.5 rounded-md bg-white border border-border font-medium">
                              {build.specsSummary.ram}
                            </span>
                          )}
                          {build.specsSummary?.storage && (
                            <span className="px-2 py-0.5 rounded-md bg-white border border-border font-medium">
                              {build.specsSummary.storage}
                            </span>
                          )}
                          {build.specsSummary?.gpu && (
                            <span className="px-2 py-0.5 rounded-md bg-white border border-border font-medium">
                              {build.specsSummary.gpu}
                            </span>
                          )}
                        </div>

                        <div className="flex items-center justify-between pt-2 border-t border-border">
                          <button
                            onClick={() => removeSavedBuild(build.id)}
                            className="text-xs text-error hover:underline flex items-center gap-1"
                          >
                            <Trash2 size={13} />
                            <span>Remove</span>
                          </button>

                          <Button
                            variant="primary"
                            size="sm"
                            onClick={() => handleAddSavedBuildToCart(build)}
                            className="font-bold gap-1 text-xs"
                          >
                            <ShoppingBag size={13} />
                            <span>Add to Cart</span>
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: Delivery Addresses */}
            {activeTab === 'addresses' && (
              <div className="space-y-6 animate-fade-in">
                <div className="flex items-center justify-between pb-4 border-b border-border">
                  <div>
                    <h2 className="text-lg font-black text-navy">Delivery Address Book</h2>
                    <p className="text-xs text-muted">Manage your delivery locations for fast 1-click checkout.</p>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => setShowAddAddressModal(true)}
                    className="gap-1.5 font-bold"
                  >
                    <Plus size={14} />
                    <span>Add Address</span>
                  </Button>
                </div>

                {user.addresses.length === 0 ? (
                  <div className="text-center py-12 space-y-3">
                    <div className="w-12 h-12 rounded-2xl bg-primary-soft text-primary flex items-center justify-center mx-auto">
                      <MapPin size={24} />
                    </div>
                    <p className="text-xs text-muted">You have not added any delivery addresses yet.</p>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => setShowAddAddressModal(true)}
                    >
                      Add Your First Address
                    </Button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {user.addresses.map((addr) => (
                      <div
                        key={addr.id}
                        className={`rounded-2xl border p-4 transition-all relative ${
                          addr.isDefault
                            ? 'bg-primary-soft/40 border-primary shadow-sm'
                            : 'bg-white border-border'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-bold text-navy flex items-center gap-1.5">
                            <MapPin size={14} className="text-primary" />
                            {addr.title}
                          </span>
                          {addr.isDefault ? (
                            <Badge variant="primary" size="sm">Default Address</Badge>
                          ) : (
                            <button
                              onClick={() => setDefaultAddress(addr.id)}
                              className="text-[11px] text-primary hover:underline font-semibold"
                            >
                              Set as Default
                            </button>
                          )}
                        </div>

                        <div className="space-y-0.5 text-xs text-slate-700">
                          <p className="font-bold text-navy">{addr.fullName}</p>
                          <p>{addr.street}</p>
                          <p>{addr.city}, {addr.state}</p>
                          <p className="text-muted pt-1">Phone: {addr.phone}</p>
                        </div>

                        <div className="pt-3 mt-3 border-t border-border flex justify-end gap-2">
                          <button
                            onClick={() => deleteAddress(addr.id)}
                            className="text-xs text-error hover:underline flex items-center gap-1"
                          >
                            <Trash2 size={13} /> Delete
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Add Address Modal */}
                {showAddAddressModal && (
                  <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
                    <div className="bg-white rounded-3xl p-6 max-w-lg w-full shadow-2xl border border-border space-y-4 animate-fade-in">
                      <div className="flex items-center justify-between pb-3 border-b border-border">
                        <h3 className="text-base font-bold text-navy">Add New Delivery Address</h3>
                        <button
                          onClick={() => setShowAddAddressModal(false)}
                          className="text-muted hover:text-navy"
                        >
                          ✕
                        </button>
                      </div>

                      <form onSubmit={handleCreateAddress} className="space-y-3">
                        <div className="space-y-1">
                          <label className="text-xs font-semibold text-navy">Address Label</label>
                          <input
                            type="text"
                            value={newAddress.title}
                            onChange={(e) => setNewAddress({ ...newAddress, title: e.target.value })}
                            placeholder="e.g. Home, Lekki Studio, Office"
                            className="w-full h-10 px-3.5 rounded-xl border border-border text-sm"
                            required
                          />
                        </div>

                        <div className="grid grid-cols-2 gap-2">
                          <div className="space-y-1">
                            <label className="text-xs font-semibold text-navy">Recipient Name</label>
                            <input
                              type="text"
                              value={newAddress.fullName}
                              onChange={(e) => setNewAddress({ ...newAddress, fullName: e.target.value })}
                              className="w-full h-10 px-3.5 rounded-xl border border-border text-sm"
                              required
                            />
                          </div>
                          <div className="space-y-1">
                            <label className="text-xs font-semibold text-navy">Phone Number</label>
                            <input
                              type="tel"
                              value={newAddress.phone}
                              onChange={(e) => setNewAddress({ ...newAddress, phone: e.target.value })}
                              className="w-full h-10 px-3.5 rounded-xl border border-border text-sm"
                              required
                            />
                          </div>
                        </div>

                        <div className="space-y-1">
                          <label className="text-xs font-semibold text-navy">Street & House Number</label>
                          <input
                            type="text"
                            value={newAddress.street}
                            onChange={(e) => setNewAddress({ ...newAddress, street: e.target.value })}
                            placeholder="e.g. Plot 14B, Admiralty Way, Lekki Phase 1"
                            className="w-full h-10 px-3.5 rounded-xl border border-border text-sm"
                            required
                          />
                        </div>

                        <div className="grid grid-cols-2 gap-2">
                          <div className="space-y-1">
                            <label className="text-xs font-semibold text-navy">City / Area</label>
                            <input
                              type="text"
                              value={newAddress.city}
                              onChange={(e) => setNewAddress({ ...newAddress, city: e.target.value })}
                              className="w-full h-10 px-3.5 rounded-xl border border-border text-sm"
                              required
                            />
                          </div>
                          <div className="space-y-1">
                            <label className="text-xs font-semibold text-navy">State</label>
                            <input
                              type="text"
                              value={newAddress.state}
                              onChange={(e) => setNewAddress({ ...newAddress, state: e.target.value })}
                              className="w-full h-10 px-3.5 rounded-xl border border-border text-sm"
                              required
                            />
                          </div>
                        </div>

                        <div className="pt-2 flex items-center justify-end gap-2">
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={() => setShowAddAddressModal(false)}
                          >
                            Cancel
                          </Button>
                          <Button type="submit" variant="primary" size="sm" className="font-bold">
                            Save Address
                          </Button>
                        </div>
                      </form>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* TAB 4: Orders & Tracking */}
            {activeTab === 'orders' && (
              <div className="space-y-6 animate-fade-in">
                <div className="flex items-center justify-between pb-4 border-b border-border">
                  <div>
                    <h2 className="text-lg font-black text-navy">Order History & Tracking</h2>
                    <p className="text-xs text-muted">Track custom builds in real-time or view past invoices.</p>
                  </div>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => openTracking('ORD-20260908-1001')}
                    className="gap-1.5 font-bold"
                  >
                    <Package size={14} />
                    <span>Track Order Live</span>
                  </Button>
                </div>

                {/* Sample Orders for customer */}
                <div className="space-y-4">
                  <div className="rounded-2xl border border-border p-5 bg-background space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border">
                      <div className="space-y-0.5">
                        <span className="text-xs font-mono font-bold text-navy">#ORD-20260908-1001</span>
                        <p className="text-[11px] text-muted">Placed on September 8, 2026</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant="navy" size="sm">CUSTOM_BUILD</Badge>
                        <span className="text-sm font-black text-navy">₦1,450,000</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="relative w-16 h-14 bg-white rounded-xl border border-border p-1 flex-shrink-0">
                        <Image
                          src="https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=200&q=80"
                          alt="TitanForge Predator 16"
                          fill
                          className="object-contain"
                        />
                      </div>
                      <div className="space-y-0.5 flex-1">
                        <h4 className="text-xs font-bold text-navy">TitanForge Predator 16 Pro Gaming Laptop</h4>
                        <p className="text-[11px] text-muted">64GB DDR5 • 2TB PCIe SSD • Custom Laser Engraving</p>
                        <p className="text-[11px] text-emerald-600 font-semibold flex items-center gap-1">
                          <Clock size={12} /> Laser Engraving in Progress — Estimated Delivery: 2 Days
                        </p>
                      </div>
                    </div>

                    <div className="pt-2 flex justify-end gap-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => openTracking('ORD-20260908-1001')}
                        className="text-xs font-bold gap-1"
                      >
                        <ExternalLink size={13} /> View Build Progress
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 5: Security */}
            {activeTab === 'security' && (
              <div className="space-y-6 animate-fade-in">
                <div className="pb-4 border-b border-border">
                  <h2 className="text-lg font-black text-navy">Security Settings</h2>
                  <p className="text-xs text-muted">Manage your password and customer account protection.</p>
                </div>

                {securitySuccess && (
                  <div className="p-3 rounded-xl bg-success-light border border-success/30 text-success text-xs flex items-center gap-2 animate-fade-in">
                    <CheckCircle2 size={16} />
                    <span>{securitySuccess}</span>
                  </div>
                )}

                {securityError && (
                  <div className="p-3 rounded-xl bg-error-light border border-error/30 text-error text-xs flex items-center gap-2 animate-fade-in">
                    <AlertCircle size={16} />
                    <span>{securityError}</span>
                  </div>
                )}

                <form onSubmit={handleUpdateSecurity} className="space-y-4 max-w-xl">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-navy">Current Password</label>
                    <input
                      type="password"
                      value={currentPassword}
                      onChange={(e) => setCurrentPassword(e.target.value)}
                      placeholder="Enter current password"
                      className="w-full h-11 px-4 rounded-xl border border-border bg-background text-sm text-foreground focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-navy">New Password</label>
                    <input
                      type="password"
                      value={newSecurityPassword}
                      onChange={(e) => setNewSecurityPassword(e.target.value)}
                      placeholder="Minimum 8 characters"
                      className="w-full h-11 px-4 rounded-xl border border-border bg-background text-sm text-foreground focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-navy">Confirm New Password</label>
                    <input
                      type="password"
                      value={confirmSecurityPassword}
                      onChange={(e) => setConfirmSecurityPassword(e.target.value)}
                      placeholder="Re-enter new password"
                      className="w-full h-11 px-4 rounded-xl border border-border bg-background text-sm text-foreground focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
                      required
                    />
                  </div>

                  <div className="pt-2">
                    <Button type="submit" variant="primary" size="md" className="font-bold">
                      Update Password
                    </Button>
                  </div>
                </form>
              </div>
            )}

          </div>

        </div>
      </main>
    </div>
  )
}
