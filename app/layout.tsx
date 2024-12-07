import './globals.css'
import { cn } from "@/lib/utils";
import { Inter } from 'next/font/google'
import NavBar from '@/components/navBar';
import Footer from '@/components/footer';
import { Analytics } from "@vercel/analytics/react"

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Middlesex ID Generator',
  description: 'For Middlesex School',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
        <body
        className={
          "flex flex-col min-h-screen bg-tan font-sans antialiased" + 
          inter.className
        }
      >
        <NavBar />
        <main className="flex-grow">
        {children}
        </main>
        <Footer />
        <Analytics />
      </body>
    </html>
  )
}
