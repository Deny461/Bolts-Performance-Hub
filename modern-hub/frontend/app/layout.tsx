import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Boston Bolts • Performance Hub',
  description: 'Modern analytics for coaches',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="max-w-7xl mx-auto px-4 py-4">
          <header className="bg-gradient-to-r from-bolts-blue to-blue-800 rounded-xl p-4 shadow-2xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src="/logo.png" alt="Bolts" className="w-10 h-10" />
              <div className="text-white font-extrabold text-xl">Boston Bolts • Performance Hub</div>
              <div className="text-emerald-200 text-xs ml-2">Modern analytics for coaches</div>
            </div>
            <div className="bg-bolts-green text-green-950 font-bold text-xs px-3 py-1 rounded-full">LIVE</div>
          </header>
          <main className="mt-6">{children}</main>
        </div>
      </body>
    </html>
  )
}
