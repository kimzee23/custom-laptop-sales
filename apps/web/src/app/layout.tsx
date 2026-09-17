import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AnnouncementBar } from '@/components/layout/AnnouncementBar'
import { StoreFooter } from '@/components/layout/StoreFooter'
import { ClientModals } from '@/components/layout/ClientModals'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })

export const metadata: Metadata = {
  title: 'RealTech Custom Laptops & Electronics Marketplace',
  description: 'Shop top brand laptops or configure your custom machine with instant DDR5 RAM, PCIe SSD, chassis finish, and lid artwork personalization.',
  keywords: 'custom laptops, gaming laptops, student laptops, RTX 4070, laptop builder, Nigeria laptop store, Jumia style marketplace',
  openGraph: {
    title: 'RealTech Custom Laptops',
    description: 'Build your custom laptop or shop ready-to-ship models with instant live pricing in Nigeria.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen flex flex-col bg-background text-foreground antialiased selection:bg-primary selection:text-white">
        <AnnouncementBar />
        <main className="flex-1">
          {children}
        </main>
        <StoreFooter />
        <ClientModals />
      </body>
    </html>
  )
}
