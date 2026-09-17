'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { 
  Mail, Lock, Eye, EyeOff, ArrowRight, Loader2, Sparkles, 
  AlertCircle, CheckCircle2, UserCheck
} from 'lucide-react'
import { useAuthStore, DEMO_ACCOUNTS } from '@/stores/authStore'

function LoginFormContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get('callbackUrl') || '/account'

  const { login, socialLogin, isLoading, error, clearError } = useAuthStore()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(true)
  const [formError, setFormError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)
    clearError()

    if (!email) {
      setFormError('Please enter your email address.')
      return
    }
    if (!password) {
      setFormError('Please enter your password.')
      return
    }

    const res = await login({ email, password, rememberMe })
    if (res.success) {
      setSuccessMessage('Successfully signed in! Redirecting...')
      setTimeout(() => {
        router.push(callbackUrl)
      }, 700)
    } else {
      setFormError(res.error || 'Invalid credentials.')
    }
  }

  const handleDemoLogin = async (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail)
    setPassword(demoPass)
    setFormError(null)
    clearError()
    
    const res = await login({ email: demoEmail, password: demoPass, rememberMe: true })
    if (res.success) {
      setSuccessMessage('Signed in with demo customer account! Redirecting...')
      setTimeout(() => {
        router.push(callbackUrl)
      }, 700)
    }
  }

  const handleSocialLogin = async (provider: 'google' | 'github' | 'apple') => {
    setFormError(null)
    const res = await socialLogin(provider)
    if (res.success) {
      setSuccessMessage(`Signed in via ${provider}! Redirecting...`)
      setTimeout(() => {
        router.push(callbackUrl)
      }, 700)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-1 text-center sm:text-left">
        <h1 className="text-2xl font-black tracking-tight text-navy font-display">
          Welcome back
        </h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Sign in to access your saved custom builds and orders.
        </p>
      </div>

      {/* Demo Fast Login Pills */}
      <div className="p-3.5 rounded-2xl bg-blue-50/70 border border-blue-100 space-y-2.5">
        <div className="flex items-center justify-between text-[11px] font-bold text-primary">
          <span className="flex items-center gap-1.5">
            <Sparkles size={13} /> Quick One-Click Demo Login
          </span>
          <span className="text-slate-400 font-normal">Reviewer Fast-track</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {DEMO_ACCOUNTS.map((demo) => (
            <button
              key={demo.email}
              type="button"
              onClick={() => handleDemoLogin(demo.email, demo.pass)}
              className="text-left p-2.5 rounded-xl bg-white hover:bg-blue-50/80 border border-slate-200/80 hover:border-primary/40 transition-all text-xs group shadow-sm"
            >
              <div className="font-bold text-slate-800 group-hover:text-primary truncate">
                {demo.user.name}
              </div>
              <div className="text-[10px] text-slate-500 truncate">
                {demo.email}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Feedback Alerts */}
      {(formError || error) && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2.5 animate-fade-in">
          <AlertCircle size={16} className="text-red-600 flex-shrink-0" />
          <span>{formError || error}</span>
        </div>
      )}

      {successMessage && (
        <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2.5 animate-fade-in">
          <CheckCircle2 size={16} className="text-emerald-600 flex-shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      {/* Main Login Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email */}
        <div className="space-y-1.5">
          <label className="text-xs font-bold text-slate-700">
            Email Address
          </label>
          <div className="relative">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. name@example.com"
              className="w-full h-11 pl-10 pr-4 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
              required
            />
            <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          </div>
        </div>

        {/* Password */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-700">
              Password
            </label>
            <Link
              href="/auth/forgot-password"
              className="text-xs text-primary hover:underline font-semibold"
            >
              Forgot password?
            </Link>
          </div>
          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              className="w-full h-11 pl-10 pr-11 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all shadow-sm"
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
        </div>

        {/* Remember me */}
        <div className="flex items-center justify-between pt-1">
          <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-600">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="w-4 h-4 rounded border-slate-300 text-primary focus:ring-primary/20 cursor-pointer"
            />
            <span>Remember this device</span>
          </label>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full h-11 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.99] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              <span>Signing in...</span>
            </>
          ) : (
            <>
              <span>Sign In</span>
              <ArrowRight size={16} />
            </>
          )}
        </button>
      </form>

      {/* Social Sign In Divider */}
      <div className="relative flex items-center justify-center my-4">
        <div className="border-t border-slate-200 w-full" />
        <span className="bg-white px-3 text-[11px] text-slate-400 uppercase tracking-wider font-bold absolute">
          Or continue with
        </span>
      </div>

      {/* Social Buttons */}
      <div className="grid grid-cols-3 gap-2.5">
        <button
          type="button"
          onClick={() => handleSocialLogin('google')}
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
          onClick={() => handleSocialLogin('github')}
          className="flex items-center justify-center gap-2 h-10 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700 transition-all shadow-sm hover:border-slate-300"
        >
          <svg className="w-4 h-4 fill-current text-slate-800" viewBox="0 0 24 24">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
          </svg>
          <span>GitHub</span>
        </button>

        <button
          type="button"
          onClick={() => handleSocialLogin('apple')}
          className="flex items-center justify-center gap-2 h-10 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700 transition-all shadow-sm hover:border-slate-300"
        >
          <svg className="w-4 h-4 fill-current text-slate-800" viewBox="0 0 24 24">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.85c.62-.75 1.04-1.8 0.92-2.85-.9.04-1.99.6-2.63 1.35-.57.66-.99 1.73-.85 2.76 1 .08 2.03-.54 2.56-1.26z" />
          </svg>
          <span>Apple</span>
        </button>
      </div>

      {/* Switch to Register */}
      <div className="pt-2 text-center text-xs text-slate-500">
        Don&apos;t have an account?{' '}
        <Link
          href="/auth/register"
          className="text-primary hover:underline font-bold"
        >
          Create a free account
        </Link>
      </div>
    </div>
  )
}

export default function LoginPage() {
  return (
    <React.Suspense fallback={<div className="p-8 text-center text-sm text-slate-500">Loading sign in...</div>}>
      <LoginFormContent />
    </React.Suspense>
  )
}
