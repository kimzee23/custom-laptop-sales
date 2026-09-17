'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  Mail, ArrowRight, ArrowLeft, CheckCircle2, AlertCircle, 
  KeyRound, Lock, Eye, EyeOff, Loader2, RefreshCw, Sparkles 
} from 'lucide-react'

type Step = 'REQUEST' | 'VERIFY_CODE' | 'NEW_PASSWORD' | 'SUCCESS'

export default function ForgotPasswordPage() {
  const router = useRouter()
  const [step, setStep] = useState<Step>('REQUEST')
  const [email, setEmail] = useState('')
  const [code, setCode] = useState(['', '', '', '', '', ''])
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [resendCountdown, setResendCountdown] = useState(45)
  const [canResend, setCanResend] = useState(false)

  // Countdown timer for code resend
  useEffect(() => {
    let timer: NodeJS.Timeout
    if (step === 'VERIFY_CODE' && resendCountdown > 0) {
      timer = setTimeout(() => setResendCountdown(prev => prev - 1), 1000)
    } else if (resendCountdown === 0) {
      setCanResend(true)
    }
    return () => clearTimeout(timer)
  }, [step, resendCountdown])

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorMessage(null)

    if (!email || !email.includes('@')) {
      setErrorMessage('Please enter a valid registered email address.')
      return
    }

    setIsLoading(true)
    await new Promise(r => setTimeout(r, 600))
    setIsLoading(false)
    setStep('VERIFY_CODE')
    setResendCountdown(45)
    setCanResend(false)
  }

  const handleCodeChange = (index: number, val: string) => {
    if (val.length > 1) val = val[val.length - 1]
    const updated = [...code]
    updated[index] = val
    setCode(updated)

    if (val && index < 5) {
      const nextInput = document.getElementById(`otp-input-${index + 1}`)
      if (nextInput) nextInput.focus()
    }
  }

  const handleVerifyCode = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorMessage(null)

    const fullCode = code.join('')
    if (fullCode.length < 6) {
      setErrorMessage('Please enter the complete 6-digit verification code.')
      return
    }

    setIsLoading(true)
    await new Promise(r => setTimeout(r, 600))
    setIsLoading(false)
    setStep('NEW_PASSWORD')
  }

  const handleSetNewPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorMessage(null)

    if (newPassword.length < 6) {
      setErrorMessage('Password must be at least 6 characters long.')
      return
    }
    if (newPassword !== confirmPassword) {
      setErrorMessage('Passwords do not match.')
      return
    }

    setIsLoading(true)
    await new Promise(r => setTimeout(r, 700))
    setIsLoading(false)
    setStep('SUCCESS')
  }

  const handleResend = async () => {
    if (!canResend) return
    setIsLoading(true)
    await new Promise(r => setTimeout(r, 500))
    setIsLoading(false)
    setResendCountdown(45)
    setCanResend(false)
  }

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb Back */}
      <Link
        href="/auth/login"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-navy transition-colors"
      >
        <ArrowLeft size={14} />
        <span>Back to login</span>
      </Link>

      {/* Step 1: Request Email */}
      {step === 'REQUEST' && (
        <div className="space-y-5 animate-fade-in">
          <div className="space-y-1">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-primary flex items-center justify-center mb-3 border border-blue-100">
              <KeyRound size={20} />
            </div>
            <h1 className="text-2xl font-black tracking-tight text-navy font-display">
              Reset your password
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
              Enter your registered email address and we&apos;ll send a 6-digit recovery code.
            </p>
          </div>

          {errorMessage && (
            <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
              <AlertCircle size={15} className="text-red-600 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleRequestReset} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700">
                Registered Email Address
              </label>
              <div className="relative">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. emeka.adeleke@example.com"
                  className="w-full h-11 pl-10 pr-4 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 shadow-sm"
                  required
                />
                <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-11 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.99] transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Sending code...</span>
                </>
              ) : (
                <>
                  <span>Send Recovery Code</span>
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>
        </div>
      )}

      {/* Step 2: Verify 6-digit OTP Code */}
      {step === 'VERIFY_CODE' && (
        <div className="space-y-5 animate-fade-in">
          <div className="space-y-1">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-primary flex items-center justify-center mb-3 border border-blue-100">
              <Mail size={20} />
            </div>
            <h1 className="text-2xl font-black tracking-tight text-navy font-display">
              Check your email
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
              We have sent a 6-digit verification code to <strong className="text-slate-800">{email}</strong>.
            </p>
          </div>

          {errorMessage && (
            <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
              <AlertCircle size={15} className="text-red-600 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleVerifyCode} className="space-y-4">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700 text-center block">
                Enter 6-Digit Code
              </label>
              <div className="flex justify-between gap-2">
                {code.map((digit, idx) => (
                  <input
                    key={idx}
                    id={`otp-input-${idx}`}
                    type="text"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleCodeChange(idx, e.target.value)}
                    className="w-11 h-12 text-center text-lg font-bold rounded-xl bg-slate-50 border border-slate-200 text-slate-900 focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm"
                  />
                ))}
              </div>
            </div>

            {/* Quick Demo Autofill Hint */}
            <div className="p-2.5 rounded-xl bg-blue-50/70 border border-blue-100 flex items-center justify-between text-[11px] text-slate-600">
              <span>Demo OTP: <strong className="text-primary font-mono">729401</strong></span>
              <button
                type="button"
                onClick={() => setCode(['7', '2', '9', '4', '0', '1'])}
                className="text-primary hover:underline font-bold"
              >
                Auto-fill
              </button>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-11 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.99] transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Verifying...</span>
                </>
              ) : (
                <>
                  <span>Verify Code</span>
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          <div className="text-center text-xs text-slate-500">
            Didn&apos;t receive the code?{' '}
            {canResend ? (
              <button
                type="button"
                onClick={handleResend}
                className="text-primary hover:underline font-bold"
              >
                Resend code
              </button>
            ) : (
              <span className="text-slate-400">Resend in {resendCountdown}s</span>
            )}
          </div>
        </div>
      )}

      {/* Step 3: New Password */}
      {step === 'NEW_PASSWORD' && (
        <div className="space-y-5 animate-fade-in">
          <div className="space-y-1">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-3 border border-emerald-100">
              <Lock size={20} />
            </div>
            <h1 className="text-2xl font-black tracking-tight text-navy font-display">
              Set new password
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
              Choose a secure password to protect your customer account.
            </p>
          </div>

          {errorMessage && (
            <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
              <AlertCircle size={15} className="text-red-600 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleSetNewPassword} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700">
                New Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Minimum 8 characters"
                  className="w-full h-11 pl-10 pr-11 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 shadow-sm"
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

            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-700">
                Confirm New Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Re-enter new password"
                  className="w-full h-11 pl-10 pr-11 rounded-xl bg-slate-50/70 border border-slate-200 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 shadow-sm"
                  required
                />
                <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-11 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.99] transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  <span>Updating password...</span>
                </>
              ) : (
                <>
                  <span>Update Password</span>
                  <CheckCircle2 size={16} />
                </>
              )}
            </button>
          </form>
        </div>
      )}

      {/* Step 4: Success */}
      {step === 'SUCCESS' && (
        <div className="space-y-6 text-center animate-fade-in py-4">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto border border-emerald-100 shadow-sm">
            <CheckCircle2 size={32} />
          </div>
          <div className="space-y-1.5">
            <h2 className="text-2xl font-black text-navy font-display">
              Password reset complete!
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto">
              Your password has been changed. You can now log in with your updated credentials.
            </p>
          </div>

          <button
            type="button"
            onClick={() => router.push('/auth/login')}
            className="w-full h-11 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg transition-all"
          >
            <span>Proceed to Login</span>
            <ArrowRight size={16} />
          </button>
        </div>
      )}
    </div>
  )
}
