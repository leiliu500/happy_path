import React from 'react'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Happy Path - Mental Wellness Platform',
  description: 'Your journey to mental wellness starts here. Professional, privacy-focused mental health support.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style dangerouslySetInnerHTML={{
          __html: `
            @keyframes fade-in {
              from { opacity: 0; transform: translateY(20px); }
              to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slide-in {
              from { opacity: 0; transform: translateX(30px); }
              to { opacity: 1; transform: translateX(0); }
            }
            @keyframes bounce-in {
              0% { opacity: 0; transform: scale(0.3); }
              50% { opacity: 1; transform: scale(1.05); }
              70% { transform: scale(0.9); }
              100% { opacity: 1; transform: scale(1); }
            }
            @keyframes scale-in {
              from { opacity: 0; transform: scale(0.95); }
              to { opacity: 1; transform: scale(1); }
            }
            @keyframes float {
              0%, 100% { transform: translateY(0px) rotate(0deg); }
              50% { transform: translateY(-20px) rotate(10deg); }
            }
            @keyframes float-delayed {
              0%, 100% { transform: translateY(0px) rotate(0deg); }
              50% { transform: translateY(-15px) rotate(-8deg); }
            }
            .animate-fade-in { animation: fade-in 0.6s ease-out; }
            .animate-slide-in { animation: slide-in 0.5s ease-out; }
            .animate-bounce-in { animation: bounce-in 0.8s ease-out; }
            .animate-scale-in { animation: scale-in 0.3s ease-out; }
            .animate-float { animation: float 6s ease-in-out infinite; }
            .animate-float-delayed { animation: float-delayed 8s ease-in-out infinite; }
            .duration-4000 { transition-duration: 4000ms; }
          `
        }} />
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
