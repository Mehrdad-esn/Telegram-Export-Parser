import Link from 'next/link'
import { FileText, LogIn, LayoutDashboard, User, LogOut, Crown, Menu, X, Globe } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useLocale } from '../context/LocaleContext'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'

const Header = () => {
  const { user, isAuthenticated, logout, loading } = useAuth()
  const { locale, setLocale } = useLocale()
  const [mobileOpen, setMobileOpen] = useState(false)
  const { t } = useTranslation()

  const planBadge = user?.usage ? (locale === 'en' ? user.usage.plan_name_en : user.usage.plan_name) : t('header.free')
  const isPro = user?.plan === 'pro' || user?.plan === 'business'

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-panel mx-4 mt-4 px-6 py-4">
      <div className="flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-xl group-hover:scale-105 transition-transform">
            <FileText className="w-6 h-6 text-primary-600 dark:text-primary-400" />
          </div>
          <div>
            <span className="font-bold text-lg tracking-tight text-white block leading-tight">
              {t('header.brand')}
            </span>
            <span className="text-[10px] text-slate-500 hidden sm:block">{t('header.subtitle')}</span>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-1">
          <Link href="/dashboard" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all flex items-center gap-2">
            <LayoutDashboard className="w-4 h-4" />
            {t('header.dashboard')}
          </Link>
          <Link href="/pricing" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all flex items-center gap-2">
            <Crown className="w-4 h-4" />
            {t('header.pricing')}
          </Link>
          <button
            onClick={() => setLocale(locale === 'fa' ? 'en' : 'fa')}
            className="px-3 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all flex items-center gap-2"
            title={locale === 'fa' ? 'English' : 'فارسی'}
          >
            <Globe className="w-4 h-4" />
            <span className="uppercase font-bold text-xs">{locale === 'fa' ? 'EN' : 'FA'}</span>
          </button>
          {!loading && isAuthenticated ? (
            <>
              <Link href="/account" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all flex items-center gap-2">
                <User className="w-4 h-4" />
                {user?.email?.split('@')[0]}
                {isPro && <span className="text-[10px] bg-primary-500/30 text-primary-300 px-1.5 py-0.5 rounded-full">{planBadge}</span>}
              </Link>
              <button onClick={logout} className="px-4 py-2 text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all flex items-center gap-2">
                <LogOut className="w-4 h-4" />
                {t('header.logout')}
              </button>
            </>
          ) : (
            <>
              <Link href="/auth/login" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all flex items-center gap-2">
                <LogIn className="w-4 h-4" />
                {t('header.login')}
              </Link>
              <Link href="/auth/signup" className="btn-primary py-2 px-4 text-sm">
                {t('header.signup')}
              </Link>
            </>
          )}
        </nav>

        <div className="flex items-center gap-2 md:hidden">
          <button
            onClick={() => setLocale(locale === 'fa' ? 'en' : 'fa')}
            className="px-2 py-1 text-xs font-bold uppercase text-slate-400 hover:text-white rounded-lg hover:bg-white/5 transition-all"
          >
            {locale === 'fa' ? 'EN' : 'FA'}
          </button>
          <button className="text-slate-300" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav className="md:hidden mt-4 pt-4 border-t border-slate-700/50 flex flex-col gap-2">
          <Link href="/dashboard" className="px-4 py-3 text-sm text-slate-300 hover:bg-white/5 rounded-lg" onClick={() => setMobileOpen(false)}>{t('header.dashboard')}</Link>
          <Link href="/pricing" className="px-4 py-3 text-sm text-slate-300 hover:bg-white/5 rounded-lg" onClick={() => setMobileOpen(false)}>{t('header.pricing')}</Link>
          {isAuthenticated ? (
            <>
              <Link href="/account" className="px-4 py-3 text-sm text-slate-300 hover:bg-white/5 rounded-lg" onClick={() => setMobileOpen(false)}>{t('header.account')}</Link>
              <button onClick={() => { logout(); setMobileOpen(false); }} className="px-4 py-3 text-sm text-red-400 text-right">{t('header.logout')}</button>
            </>
          ) : (
            <>
              <Link href="/auth/login" className="px-4 py-3 text-sm text-slate-300 hover:bg-white/5 rounded-lg" onClick={() => setMobileOpen(false)}>{t('header.login')}</Link>
              <Link href="/auth/signup" className="btn-primary mx-4 text-center" onClick={() => setMobileOpen(false)}>{t('header.signupShort')}</Link>
            </>
          )}
        </nav>
      )}
    </header>
  );
};

export default Header;
