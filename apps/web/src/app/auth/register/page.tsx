'use client'

import React, { useState, useMemo } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  User, Mail, Phone, Lock, Eye, EyeOff, ArrowRight, Loader2, 
  CheckCircle2, AlertCircle, ShieldCheck, Sparkles, Check, X
} from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'

export default function RegisterPage() {
  const router = useRouter()
  const { register, socialLogin, isLoading, error, clearError } = useAuthStore()

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    agreeTerms: true
  })

  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Real-time password strength evaluation
  const passwordStats = useMemo(() => {
    const p = formData.password
    const hasMinLength = p.length >= 8
    const hasUppercase = /[A-Z]/.test(p)
    const hasNumber = /[0-9]/.test(p)
    const hasSpecial = /[^A-Za-z0-9]/.test(p)

    let score = 0
    if (hasMinLength) score += 1
    if (hasUppercase) score += 1
    if (hasNumber) score += 1
    if (hasSpecial) score += 1

    return {
      hasMinLength,
      hasUppercase,
      hasNumber,
      hasSpecial,
      score,
      strengthLabel: score <= 1 ? 'Weak' : score <= 3 ? 'Medium' : 'Strong',
      color: score <= 1 ? 'bg-red-500' : score <= 3 ? 'bg-amber-500' : 'bg-emerald-500'
    }
  }, [formData.password])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)
    clearError()

    if (!formData.name.trim()) {
      setFormError('Please enter your full name.')
      return
    }
    if (!formData.email.includes('@')) {
      setFormError('Please enter a valid email address.')
      return
    }
    if (formData.password.length < 6) {
      setFormError('Password must be at least 6 characters long.')
      return
    }
    if (formData.password !== formData.confirmPassword) {
      setFormError('Passwords do not match.')
      return
    }
    if (!formData.agreeTerms) {
      setFormError('Please accept the Terms of Service to continue.')
      return
    }

    const res = await register({
      name: formData.name,
      email: formData.email,
      phone: formData.phone,
      password: formData.password
    })

    if (res.success) {
      setSuccessMessage('Account created successfully! Redirecting to your dashboard...')
      setTimeout(() => {
        router.push('/account')
      }, 800)
    } else {
      setFormError(res.error || 'Failed to create account.')
    }
  }

  const handleSocialRegister = async (provider: 'google' | 'github' | 'apple') => {
    setFormError(null)
    const res = await socialLogin(provider)
    if (res.success) {
      setSuccessMessage(`Registered and signed in via ${provider}! Redirecting...`)
      setTimeout(() => {
        router.push('/account')
      }, 700)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-1 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50 text-primary text-[11px] font-bold mb-1 border border-blue-100">
          <Sparkles size={12} />
          <span>JOIN REALTECH</span>
        </div>
        <h1 className="text-2xl font-black tracking-tight text-navy font-display">
          Create customer account
        </h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Save custom hardware configs, access 2-Year warranty, and track delivery.
        </p>
      </div>

      {/* Feedback Alerts */}
      {(formError || error) && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs space-y-2 animate-fade-in">
          <div className="flex items-center gap-2 font-semibold">
            <AlertCircle size={16} className="text-red-600 flex-shrink-0" />
            <span>{formError || error}</span>
          </div>
          {((formError || error)?.toLowerCase().includes('exist') || (formError || error)?.toLowerCase().includes('account with this email')) && (
            <div className="pt-2 border-t border-red-200/60 flex items-center justify-between">
              <span className="text-slate-600">Already have an account?</span>
              <Link
                href={`/auth/login?email=${encodeURIComponent(formData.email)}`}
                className="px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-bold hover:bg-primary-hover shadow-sm transition-all"
              >
                Sign In Instead
              </Link>
            </div>
          )}
        </div>
      )}

      {successMessage && (
        <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2.5 animate-fade-in">
          <CheckCircle2 size={16} className="text-emerald-600 flex-shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      {/* Registration Form */}
      <form onSubmit={handleSubmit} className="space-y-3.5">
        {/* Full Name */}
        <div className="space-y-1">
          <label className="text-xs font-bold text-slate-700">
            Full Name <span className="text-primary">*</span>
          </label>
          <div className="relative">
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Babatunde Johnson"
              className="w-full h-10 pl-10 pr-4 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
              required
            />
            <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          </div>
        </div>

        {/* Email */}
        <div className="space-y-1">
          <label className="text-xs font-bold text-slate-700">
            Email Address <span className="text-primary">*</span>
          </label>
          <div className="relative">
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="e.g. babatunde@example.com"
              className="w-full h-10 pl-10 pr-4 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
              required
            />
            <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          </div>
        </div>

        {/* Phone Number */}
        <div className="space-y-1">
          <label className="text-xs font-bold text-slate-700">
            Phone Number (for order & courier updates)
          </label>
          <div className="relative">
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="e.g. 0803 123 4567"
              className="w-full h-10 pl-10 pr-4 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
            />
            <Phone size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          </div>
        </div>

        {/* Password */}
        <div className="space-y-1">
          <label className="text-xs font-bold text-slate-700">
            Create Password <span className="text-primary">*</span>
          </label>
          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Minimum 8 characters"
              className="w-full h-10 pl-10 pr-11 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
              required
            />
            <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>

          {/* Password Strength Indicator */}
          {formData.password.length > 0 && (
            <div className="space-y-1.5 pt-1">
              <div className="flex items-center justify-between text-[11px] text-slate-500">
                <span>Strength: <strong className="text-slate-800">{passwordStats.strengthLabel}</strong></span>
                <span>{passwordStats.score}/4 requirements met</span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden flex gap-1">
                <div className={`h-full flex-1 rounded-full ${passwordStats.score >= 1 ? passwordStats.color : 'bg-slate-200'}`} />
                <div className={`h-full flex-1 rounded-full ${passwordStats.score >= 2 ? passwordStats.color : 'bg-slate-200'}`} />
                <div className={`h-full flex-1 rounded-full ${passwordStats.score >= 3 ? passwordStats.color : 'bg-slate-200'}`} />
                <div className={`h-full flex-1 rounded-full ${passwordStats.score >= 4 ? passwordStats.color : 'bg-slate-200'}`} />
              </div>
              <div className="grid grid-cols-2 gap-1 text-[10px] text-slate-500 pt-0.5">
                <span className={`flex items-center gap-1 ${passwordStats.hasMinLength ? 'text-emerald-600 font-bold' : ''}`}>
                  {passwordStats.hasMinLength ? <Check size={11} /> : <X size={11} />} 8+ Characters
                </span>
                <span className={`flex items-center gap-1 ${passwordStats.hasUppercase ? 'text-emerald-600 font-bold' : ''}`}>
                  {passwordStats.hasUppercase ? <Check size={11} /> : <X size={11} />} Uppercase letter
                </span>
                <span className={`flex items-center gap-1 ${passwordStats.hasNumber ? 'text-emerald-600 font-bold' : ''}`}>
                  {passwordStats.hasNumber ? <Check size={11} /> : <X size={11} />} Number (0-9)
                </span>
                <span className={`flex items-center gap-1 ${passwordStats.hasSpecial ? 'text-emerald-600 font-bold' : ''}`}>
                  {passwordStats.hasSpecial ? <Check size={11} /> : <X size={11} />} Special symbol
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Confirm Password */}
        <div className="space-y-1">
          <label className="text-xs font-bold text-slate-700">
            Confirm Password <span className="text-primary">*</span>
          </label>
          <div className="relative">
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Re-enter your password"
              className="w-full h-10 pl-10 pr-11 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
              required
            />
            <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>
        </div>

        {/* Agree terms */}
        <div className="pt-1">
          <label className="flex items-start gap-2.5 cursor-pointer text-xs text-slate-600">
            <input
              type="checkbox"
              name="agreeTerms"
              checked={formData.agreeTerms}
              onChange={handleChange}
              className="w-4 h-4 mt-0.5 rounded border-slate-300 text-primary focus:ring-primary/20 cursor-pointer"
            />
            <span className="leading-snug">
              I agree to the Terms of Service, Privacy Policy, and 2-Year Official Warranty coverage.
            </span>
          </label>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full h-11 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.99] transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-2"
        >
          {isLoading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              <span>Creating your account...</span>
            </>
          ) : (
            <>
              <span>Create Free Account</span>
              <ArrowRight size={16} />
            </>
          )}
        </button>
      </form>

      {/* Social Registration Divider */}
      <div className="relative flex items-center justify-center my-3">
        <div className="border-t border-slate-200 w-full" />
        <span className="bg-white px-3 text-[11px] text-slate-400 uppercase tracking-wider font-bold absolute">
          Or register with
        </span>
      </div>

      {/* Social Buttons */}
      <div className="grid grid-cols-3 gap-2.5">
        <button
          type="button"
          onClick={() => handleSocialRegister('google')}
          className="flex items-center justify-center gap-2 h-10 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700 transition-all shadow-sm hover:border-slate-300"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#EA4335"
              d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"
            />
            <path
              fill="#4285F4"
              d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"
            />
            <path
              fill="#FBBC05"
              d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8s.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.8 0 12s.7 3.3 1.9 5.7l3.7-2.9z"
            />
            <path
              fill="#34A853"
              d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16C3.7 19.7 7.5 23 12 23z"
            />
          </svg>
          <span>Google</span>
        </button>

        <button
          type="button"
          onClick={() => handleSocialRegister('github')}
          className="flex items-center justify-center gap-2 h-10 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700 transition-all shadow-sm hover:border-slate-300"
        >
          <svg className="w-4 h-4 fill-current text-slate-800" viewBox="0 0 24 24">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
          </svg>
          <span>GitHub</span>
        </button>

        <button
          type="button"
          onClick={() => handleSocialRegister('apple')}
          className="flex items-center justify-center gap-2 h-10 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700 transition-all shadow-sm hover:border-slate-300"
        >
          <svg className="w-4 h-4 fill-current text-slate-800" viewBox="0 0 24 24">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.85c.62-.75 1.04-1.8 0.92-2.85-.9.04-1.99.6-2.63 1.35-.57.66-.99 1.73-.85 2.76 1 .08 2.03-.54 2.56-1.26z" />
          </svg>
          <span>Apple</span>
        </button>
      </div>

      {/* Switch to Login */}
      <div className="pt-2 text-center text-xs text-slate-500">
        Already have an account?{' '}
        <Link
          href="/auth/login"
          className="text-primary hover:underline font-bold"
        >
          Sign in here
        </Link>
      </div>
    </div>
  )
}
