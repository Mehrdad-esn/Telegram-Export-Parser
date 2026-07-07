import Head from 'next/head'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, Crown, Building2, Sparkles, Loader2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useRouter } from 'next/router'
import Link from 'next/link'
import { useTranslation } from 'react-i18next'

const planIds = ['free', 'pro', 'business']
const planIcons = [Sparkles, Crown, Building2]

export default function Pricing() {
  const { isAuthenticated, user } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState<string | null>(null)
  const { t } = useTranslation()

  const priceIds: Record<string, string | undefined> = {
    pro: process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO || 'price_pro',
    business: process.env.NEXT_PUBLIC_STRIPE_PRICE_BUSINESS || 'price_business',
  }

  const handleCheckout = async (planId: string) => {
    if (planId === 'free') {
      router.push('/auth/signup')
      return
    }
    if (!isAuthenticated) {
      router.push('/auth/login?redirect=/pricing')
      return
    }
    if (user?.plan === planId) return

    setLoading(planId)
    try {
      const res = await fetch('/billing/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          price_id: priceIds[planId],
          plan: planId,
          success_url: `${window.location.origin}/billing/success`,
          cancel_url: `${window.location.origin}/billing/cancel`,
        }),
      })
      const data = await res.json()
      if (data.url) {
        window.location.href = data.url
      } else {
        alert(data.detail || t('pricing.errors.checkout'))
      }
    } catch (err: any) {
      alert(t('pricing.errors.generic', { message: err.message }))
    } finally {
      setLoading(null)
    }
  }

  return (
    <>
      <Head>
        <title>{t('pricing.title')}</title>
      </Head>

      <div className="max-w-6xl mx-auto py-8">
        <div className="text-center mb-16">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-extrabold text-white mb-4"
          >
            {t('pricing.headingBefore')}<span className="gradient-text">{t('pricing.headingGradient')}</span>{t('pricing.headingAfter')}
          </motion.h1>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            {t('pricing.subtitle')}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {planIds.map((planId, i) => {
            const Icon = planIcons[i]
            const plan = t(`pricing.plans.${planId}`, { returnObjects: true }) as any
            const isCurrent = user?.plan === planId
            const features = t(`pricing.plans.${planId}.features`, { returnObjects: true }) as unknown as string[]
            const isHighlight = planId === 'pro'

            return (
              <motion.div
                key={planId}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.15 }}
                className={`glass-card p-8 flex flex-col relative ${
                  isHighlight ? 'border-primary-500/50 ring-2 ring-primary-500/20 md:scale-105 z-10' : ''
                }`}
              >
                {isHighlight && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-primary-500 to-indigo-500 text-white text-xs font-bold px-4 py-1 rounded-full">
                    {t('pricing.popular')}
                  </span>
                )}

                <div className="flex items-center gap-3 mb-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${isHighlight ? 'bg-primary-500/20 text-primary-400' : 'bg-slate-700/50 text-slate-400'}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">{plan.name}</h3>
                    <p className="text-xs text-slate-500">{plan.nameEn}</p>
                  </div>
                </div>

                <p className="text-slate-400 text-sm mb-6">{plan.description}</p>

                <div className="mb-8">
                  <span className="text-4xl font-extrabold text-white">{t('pricing.freePrice')}</span>
                </div>

                <ul className="space-y-3 mb-8 flex-1">
                  {features.map((f: string, j: number) => (
                    <li key={j} className="flex items-start gap-2 text-sm text-slate-300">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                      {f}
                    </li>
                  ))}
                </ul>

                {planId === 'free' ? (
                  <Link href="/auth/signup" className="btn-secondary text-center block">{plan.cta}</Link>
                ) : isCurrent ? (
                  <button disabled className="btn-secondary opacity-60 cursor-not-allowed w-full">{t('pricing.currentPlan')}</button>
                ) : (
                  <button
                    onClick={() => handleCheckout(planId)}
                    disabled={loading === planId}
                    className={`w-full flex items-center justify-center gap-2 ${isHighlight ? 'btn-primary' : 'btn-secondary'}`}
                  >
                    {loading === planId ? <Loader2 className="w-4 h-4 animate-spin" /> : plan.cta}
                  </button>
                )}
              </motion.div>
            )
          })}
        </div>

        <p className="text-center text-slate-500 text-sm mt-12">
          {t('pricing.allFree')}
        </p>
      </div>
    </>
  )
}
