import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { CheckCircle2, ArrowLeft } from 'lucide-react'
import { useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'

export default function BillingSuccess() {
  const { refreshUser } = useAuth()

  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  return (
    <>
      <Head><title>پرداخت موفق | Telegram Parser</title></Head>
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass-panel p-12 text-center max-w-md">
          <div className="w-20 h-20 rounded-full bg-emerald-500/20 flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 className="w-10 h-10 text-emerald-400" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-3">پرداخت موفق!</h1>
          <p className="text-slate-400 mb-8">اشتراک شما فعال شد. از تمام امکانات پلن جدید لذت ببرید.</p>
          <Link href="/dashboard" className="btn-primary inline-flex items-center gap-2">
            رفتن به داشبورد <ArrowLeft className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>
    </>
  )
}
