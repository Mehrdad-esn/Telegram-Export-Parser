import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { changeLanguage } from '../lib/i18n'

type Locale = 'fa' | 'en'

interface LocaleContextType {
  locale: Locale
  setLocale: (locale: Locale) => void
  dir: 'rtl' | 'ltr'
}

const LocaleContext = createContext<LocaleContextType>({
  locale: 'fa',
  setLocale: () => {},
  dir: 'rtl',
})

export function LocaleProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('fa')

  const setLocale = useCallback((newLocale: Locale) => {
    setLocaleState(newLocale)
    localStorage.setItem('locale', newLocale)
    changeLanguage(newLocale)
    document.documentElement.dir = newLocale === 'fa' ? 'rtl' : 'ltr'
    document.documentElement.lang = newLocale
  }, [])

  useEffect(() => {
    const saved = localStorage.getItem('locale') as Locale | null
    const initial = saved === 'en' ? 'en' : 'fa'
    setLocaleState(initial)
    changeLanguage(initial)
    document.documentElement.dir = initial === 'fa' ? 'rtl' : 'ltr'
    document.documentElement.lang = initial
  }, [])

  return (
    <LocaleContext.Provider value={{ locale, setLocale, dir: locale === 'fa' ? 'rtl' : 'ltr' }}>
      {children}
    </LocaleContext.Provider>
  )
}

export function useLocale() {
  return useContext(LocaleContext)
}
