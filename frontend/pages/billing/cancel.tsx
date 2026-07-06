import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { XCircle, ArrowLeft } from 'lucide-react'

export default function BillingCancel() {
  return (
    <>
      <Head><title>پرداخت لغو شد | Telegram Parser</title></Head>
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass-panel p-12 text-center max-w-md">
          <div className="w-20 h-20 rounded-full bg-red-500/20 flex items-center justify-center mx-auto mb-6">
            <XCircle className="w-10 h-10 text-red-400" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-3">پرداخت لغو شد</h1>
          <p className="text-slate-400 mb-8">نگران نباشید — می‌توانید هر زمان دوباره تلاش کنید.</p>
          <div className="flex flex-col gap-3">
            <Link href="/pricing" className="btn-primary inline-flex items-center justify-center gap-2">
              بازگشت به قیمت‌ها <ArrowLeft className="w-4 h-4" />
            </Link>
            <Link href="/dashboard" className="btn-secondary text-center">داشبورد</Link>
          </div>
        </motion.div>
      </div>
    </>
  )
}
