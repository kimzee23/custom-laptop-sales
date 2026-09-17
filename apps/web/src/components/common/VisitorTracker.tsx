'use client'

import { useEffect, useRef } from 'react'
import { usePathname } from 'next/navigation'
import { api } from '@/lib/api'

export function VisitorTracker() {
  const pathname = usePathname()
  const lastTrackedPath = useRef<string | null>(null)

  useEffect(() => {
    if (typeof window === 'undefined') return

    // Get or create session ID in sessionStorage
    let sessionId = sessionStorage.getItem('visitor_session_id')
    if (!sessionId) {
      sessionId = `sess_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
      try {
        sessionStorage.setItem('visitor_session_id', sessionId)
      } catch {
        // Private mode safety
      }
    }

    if (pathname && lastTrackedPath.current !== pathname) {
      lastTrackedPath.current = pathname
      api.trackVisit(pathname, sessionId)
    }
  }, [pathname])

  return null
}
