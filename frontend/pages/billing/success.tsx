import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { CheckCircle2, ArrowLeft } from 'lucide-react'
import { useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useTranslation } from 'react-i18next'

export default function BillingSuccess() {
  const { refreshUser } = useAuth()
  const { t } = useTranslation()

  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  return (
    <>
      <Head><title>{t('billing.successTitle')}</title></Head>
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass-panel p-12 text-center max-w-md">
          <div className="w-20 h-20 rounded-full bg-emerald-500/20 flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 className="w-10 h-10 text-emerald-400" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-3">{t('billing.successHeading')}</h1>
          <p className="text-slate-400 mb-8">{t('billing.successDesc')}</p>
          <Link href="/dashboard" className="btn-primary inline-flex items-center gap-2">
            {t('billing.successCTA')} <ArrowLeft className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>
    </>
  )
}
