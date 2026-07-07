import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { User, Crown, Upload, Download, Mail, Calendar, ArrowLeft } from 'lucide-react'
import { ProtectedRoute, useAuth } from '../../context/AuthContext'
import { useTranslation } from 'react-i18next'

function AccountContent() {
  const { user, refreshUser } = useAuth()
  const { t, i18n } = useTranslation()

  if (!user) return null

  const usage = user.usage
  const uploadPct = usage.uploads_limit ? Math.min(100, (usage.uploads_used / usage.uploads_limit) * 100) : 0
  const exportPct = usage.exports_limit ? Math.min(100, (usage.exports_used / usage.exports_limit) * 100) : 0

  return (
    <>
      <Head><title>{t('account.title')}</title></Head>

      <div className="max-w-3xl mx-auto py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold text-white mb-2">{t('account.heading')}</h1>
          <p className="text-slate-400 mb-8">{t('account.subtitle')}</p>

          <div className="glass-panel p-8 mb-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 rounded-2xl bg-primary-500/20 flex items-center justify-center">
                <User className="w-8 h-8 text-primary-400" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">{user.email}</h2>
                <div className="flex items-center gap-2 mt-1">
                  <Crown className="w-4 h-4 text-amber-400" />
                  <span className="text-primary-300 font-medium">{i18n.language === 'en' ? usage.plan_name_en : usage.plan_name}</span>
                  {user.subscription_status && (
                    <span className="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full">{user.subscription_status}</span>
                  )}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              <div className="flex items-center gap-2 text-slate-400">
                <Mail className="w-4 h-4" /> {user.email}
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Calendar className="w-4 h-4" /> {t('account.plan')}: {usage.plan_name_en}
              </div>
            </div>
          </div>

          <div className="glass-panel p-8 mb-6 space-y-6">
            <h3 className="text-lg font-bold text-white">{t('account.monthlyUsage')}</h3>

            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-400 flex items-center gap-2"><Upload className="w-4 h-4" /> {t('account.upload')}</span>
                <span className="text-white">{usage.uploads_used} / {usage.uploads_limit ?? '∞'}</span>
              </div>
              {usage.uploads_limit && (
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="bg-primary-500 h-2 rounded-full transition-all" style={{ width: `${uploadPct}%` }} />
                </div>
              )}
            </div>

            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-400 flex items-center gap-2"><Download className="w-4 h-4" /> {t('account.export')}</span>
                <span className="text-white">{usage.exports_used} / {usage.exports_limit ?? '∞'}</span>
              </div>
              {usage.exports_limit && (
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="bg-indigo-500 h-2 rounded-full transition-all" style={{ width: `${exportPct}%` }} />
                </div>
              )}
            </div>

            <p className="text-xs text-slate-500">{t('account.maxFileSize', { size: usage.max_file_size_mb })}</p>
          </div>

          <div className="glass-panel p-8 mb-6">
            <h3 className="text-lg font-bold text-white mb-4">{t('account.allowedFormats')}</h3>
            <div className="flex flex-wrap gap-2">
              {usage.formats.map((f: string) => (
                <span key={f} className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-lg text-sm uppercase">{f}</span>
              ))}
            </div>
          </div>

          {user.plan === 'free' && (
            <Link href="/pricing" className="btn-primary inline-flex items-center gap-2">
              {t('account.upgrade')} <ArrowLeft className="w-4 h-4" />
            </Link>
          )}
        </motion.div>
      </div>
    </>
  )
}

export default function Account() {
  return (
    <ProtectedRoute>
      <AccountContent />
    </ProtectedRoute>
  )
}
