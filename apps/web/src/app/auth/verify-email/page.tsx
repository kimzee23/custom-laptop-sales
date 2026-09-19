'use client'

import React, { useState, useEffect, useRef, Suspense } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { 
  Mail, ShieldCheck, ArrowRight, Loader2, CheckCircle2, 
  AlertCircle, RefreshCw, KeyRound 
} from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'

function VerifyEmailContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const initialEmail = searchParams.get('email') || ''

  const { verifyOtp, resendOtp, isLoading, error } = useAuthStore()

  const [email, setEmail] = useState(initialEmail)
  const [digits, setDigits] = useState<string[]>(['', '', '', '', '', ''])
  const [cooldown, setCooldown] = useState(60)
  const [canResend, setCanResend] = useState(false)
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null)
  const [isVerifying, setIsVerifying] = useState(false)
  const [isResending, setIsResending] = useState(false)

  const inputRefs = useRef<Array<HTMLInputElement | null>>([])

  // Keep query email in sync
  useEffect(() => {
    if (initialEmail && !email) {
      setEmail(initialEmail)
    }
  }, [initialEmail, email])

  // Focus first input on mount
  useEffect(() => {
    if (inputRefs.current[0]) {
      inputRefs.current[0].focus()
    }
  }, [])

  // 60-second cooldown timer for resend
  useEffect(() => {
    if (cooldown > 0) {
      const timer = setTimeout(() => setCooldown(cooldown - 1), 1000)
      return () => clearTimeout(timer)
    } else {
      setCanResend(true)
    }
  }, [cooldown])

  const handleDigitChange = (index: number, val: string) => {
    // Only accept numbers
    const cleanVal = val.replace(/[^0-9]/g, '')
    if (!cleanVal) {
      const newDigits = [...digits]
      newDigits[index] = ''
      setDigits(newDigits)
      return
    }

    // If pasted multiple digits
    if (cleanVal.length > 1) {
      const pastedChars = cleanVal.slice(0, 6).split('')
      const newDigits = [...digits]
      pastedChars.forEach((ch, i) => {
        if (index + i < 6) {
          newDigits[index + i] = ch
        }
      })
      setDigits(newDigits)
      const nextIdx = Math.min(index + pastedChars.length, 5)
      inputRefs.current[nextIdx]?.focus()
      return
    }

    const newDigits = [...digits]
    newDigits[index] = cleanVal
    setDigits(newDigits)

    // Advance focus
    if (index < 5 && cleanVal) {
      inputRefs.current[index + 1]?.focus()
    }
  }

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !digits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus()
    }
  }

  const handlePaste = (e: React.ClipboardEvent<HTMLInputElement>) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData('text').replace(/[^0-9]/g, '').slice(0, 6)
    if (!pastedData) return

    const newDigits = [...digits]
    pastedData.split('').forEach((ch, idx) => {
      newDigits[idx] = ch
    })
    setDigits(newDigits)

    const nextIdx = Math.min(pastedData.length, 5)
    inputRefs.current[nextIdx]?.focus()
  }

  const fullCode = digits.join('')

  const handleVerify = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    setFeedback(null)

    if (!email || !email.includes('@')) {
      setFeedback({ type: 'error', message: 'Please enter a valid email address.' })
      return
    }

    if (fullCode.length !== 6) {
      setFeedback({ type: 'error', message: 'Please enter the complete 6-digit confirmation code.' })
      return
    }

    setIsVerifying(true)
    const res = await verifyOtp(email, fullCode)
    setIsVerifying(false)

    if (res.success) {
      setFeedback({
        type: 'success',
        message: 'Your email has been verified successfully! Redirecting to your account dashboard...'
      })
      setTimeout(() => {
        router.push('/account')
      }, 1000)
    } else {
      setFeedback({
        type: 'error',
        message: res.error || 'The code entered is invalid or expired. Please check and try again.'
      })
    }
  }

  const handleResend = async () => {
    if (!canResend || isResending) return
    if (!email) {
      setFeedback({ type: 'error', message: 'Please enter your email to receive a new code.' })
      return
    }

    setIsResending(true)
    setFeedback(null)
    const res = await resendOtp(email)
    setIsResending(false)

    if (res.success) {
      setFeedback({
        type: 'success',
        message: 'A fresh 6-digit code has been dispatched to your email.'
      })
      setCooldown(60)
      setCanResend(false)
    } else {
      setFeedback({
        type: 'error',
        message: res.error || 'Failed to resend code. Please try again.'
      })
    }
  }

  return (
    <div className="space-y-6">
      {/* Top Badge & Icon */}
      <div className="text-center space-y-3">
        <div className="w-16 h-16 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-primary mx-auto shadow-sm">
          <KeyRound size={32} className="animate-pulse" />
        </div>
        <div>
          <h1 className="text-2xl font-black tracking-tight text-navy">
            Verify Your Email
          </h1>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            We have sent a 6-digit verification code to your email. Enter it below to activate your account.
          </p>
        </div>
      </div>

      {/* Recipient Email Chip */}
      <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-3 flex items-center justify-between text-xs">
        <div className="flex items-center gap-2 text-slate-600 truncate">
          <Mail size={16} className="text-primary flex-shrink-0" />
          <span className="font-semibold text-slate-800 truncate">{email || 'your email'}</span>
        </div>
        <button
          type="button"
          onClick={() => {
            const newEmail = prompt('Enter your registered email address:', email)
            if (newEmail) setEmail(newEmail.trim())
          }}
          className="text-[11px] font-bold text-primary hover:underline flex-shrink-0 ml-2"
        >
          Change
        </button>
      </div>

      {/* Feedback Alerts */}
      {feedback && (
        <div
          className={`p-3.5 rounded-2xl text-xs flex items-start gap-2.5 animate-fadeIn ${
            feedback.type === 'success'
              ? 'bg-emerald-50 border border-emerald-200 text-emerald-800'
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}
        >
          {feedback.type === 'success' ? (
            <CheckCircle2 size={16} className="text-emerald-600 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertCircle size={16} className="text-red-600 flex-shrink-0 mt-0.5" />
          )}
          <span className="leading-relaxed font-medium">{feedback.message}</span>
        </div>
      )}

      {/* 6-Digit OTP Form */}
      <form onSubmit={handleVerify} className="space-y-6">
        <div className="flex justify-between items-center gap-2 max-w-xs mx-auto">
          {digits.map((digit, idx) => (
            <input
              key={idx}
              ref={(el) => { inputRefs.current[idx] = el }}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleDigitChange(idx, e.target.value)}
              onKeyDown={(e) => handleKeyDown(idx, e)}
              onPaste={handlePaste}
              className="w-11 h-14 text-center text-2xl font-mono font-bold bg-white border-2 border-slate-200 rounded-xl focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all outline-none text-slate-900 shadow-sm"
              aria-label={`Digit ${idx + 1}`}
            />
          ))}
        </div>

        {/* Action Button */}
        <button
          type="submit"
          disabled={isVerifying || fullCode.length !== 6}
          className="w-full bg-primary hover:bg-primary-hover disabled:bg-slate-200 disabled:cursor-not-allowed text-white font-bold py-3.5 rounded-xl shadow-md transition-all flex items-center justify-center gap-2 text-sm group"
        >
          {isVerifying ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              <span>Verifying Code...</span>
            </>
          ) : (
            <>
              <span>Confirm & Activate Account</span>
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </>
          )}
        </button>
      </form>

      {/* Resend Cooldown Section */}
      <div className="text-center pt-2 border-t border-slate-100">
        <p className="text-xs text-slate-500">
          Didn't receive the email? Check your spam folder or
        </p>
        <button
          type="button"
          onClick={handleResend}
          disabled={!canResend || isResending}
          className="mt-2 inline-flex items-center gap-1.5 text-xs font-bold text-primary disabled:text-slate-400 hover:underline transition-colors"
        >
          <RefreshCw size={13} className={isResending ? 'animate-spin' : ''} />
          <span>
            {isResending
              ? 'Sending fresh code...'
              : canResend
              ? 'Resend Verification Code'
              : `Resend code in ${cooldown}s`}
          </span>
        </button>
      </div>

      {/* Security & Login Backlink */}
      <div className="flex items-center justify-between text-[11px] text-slate-400 pt-3">
        <div className="flex items-center gap-1">
          <ShieldCheck size={14} className="text-emerald-500" />
          <span>Encrypted Verification</span>
        </div>
        <Link href="/auth/login" className="text-primary hover:underline font-semibold">
          Back to Sign In
        </Link>
      </div>
    </div>
  )
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={
      <div className="py-12 flex flex-col items-center justify-center text-slate-400 space-y-3">
        <Loader2 size={28} className="animate-spin text-primary" />
        <p className="text-xs">Loading verification portal...</p>
      </div>
    }>
      <VerifyEmailContent />
    </Suspense>
  )
}
