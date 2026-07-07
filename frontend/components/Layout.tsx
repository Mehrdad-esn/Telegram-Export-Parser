import React from 'react'
import Header from './Header'
import Footer from './Footer'
import { useLocale } from '../context/LocaleContext'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

const Layout: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const { locale } = useLocale()

  return (
    <div className={`dark flex flex-col min-h-screen bg-dark-950 text-slate-100 ${locale === 'en' ? inter.className : ''}`}>
      <Header />
      <main className="flex-grow pt-28 pb-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
