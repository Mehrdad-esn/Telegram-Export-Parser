import Head from 'next/head'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, Crown, Building2, Sparkles, Loader2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useRouter } from 'next/router'
import Link from 'next/link'

const plans = [
  {
    id: 'free',
    name: 'رایگان',
    nameEn: 'Free',
    price: 0,
    icon: Sparkles,
    description: 'تحلیل پایه و بدون محدودیت فایل',
    features: [
      'آپلود نامحدود در ماه',
      'خروجی نامحدود در ماه',
      'حداکثر ۱۰GB حجم فایل',
      'فرمت‌های CSV, TXT, JSON',
      'فیلتر پیام‌ها',
      'نمودارهای تحلیلی',
    ],
    cta: 'شروع رایگان',
    href: '/auth/signup',
  },
  {
    id: 'pro',
    name: 'حرفه‌ای',
    nameEn: 'Pro',
    price: 0,
    icon: Crown,
    description: 'برای کاربران حرفه‌ای و فریلنسرها',
    features: [
      'آپلود نامحدود در ماه',
      'خروجی نامحدود در ماه',
      'حداکثر ۱۰GB حجم فایل',
      'همه فرمت‌های خروجی (Excel, MD, HTML...)',
      'فیلتر پیشرفته (regex, media)',
      'پشتیبانی رایگان',
    ],
    highlight: true,
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO || 'price_pro',
    cta: 'فعال‌سازی رایگان Pro',
  },
  {
    id: 'business',
    name: 'سازمانی',
    nameEn: 'Business',
    price: 0,
    icon: Building2,
    description: 'برای تیم‌ها و سازمان‌ها',
    features: [
      'آپلود نامحدود در ماه',
      'خروجی نامحدود در ماه',
      'حداکثر ۱۰GB حجم فایل',
      'همه فرمت‌ها و قالب‌ها',
      'اولویت پردازش فایل',
      'پشتیبانی اختصاصی',
    ],
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_BUSINESS || 'price_business',
    cta: 'فعال‌سازی رایگان Business',
  },
]

export default function Pricing() {
  const { isAuthenticated, user } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState<string | null>(null)

  const handleCheckout = async (plan: typeof plans[0]) => {
    if (plan.id === 'free') {
      router.push('/auth/signup')
      return
    }
    if (!isAuthenticated) {
      router.push('/auth/login?redirect=/pricing')
      return
    }
    if (user?.plan === plan.id) return

    setLoading(plan.id)
    try {
      const res = await fetch('/billing/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          price_id: plan.priceId,
          plan: plan.id,
          success_url: `${window.location.origin}/billing/success`,
          cancel_url: `${window.location.origin}/billing/cancel`,
        }),
      })
      const data = await res.json()
      if (data.url) {
        window.location.href = data.url
      } else {
        alert(data.detail || 'خطا در ایجاد جلسه پرداخت')
      }
    } catch (err: any) {
      alert('خطا: ' + err.message)
    } finally {
      setLoading(null)
    }
  }

  return (
    <>
      <Head>
        <title>قیمت‌ها | Telegram Export Parser</title>
      </Head>

      <div className="max-w-6xl mx-auto py-8">
        <div className="text-center mb-16">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-extrabold text-white mb-4"
          >
            پلن مناسب <span className="gradient-text">خودتان</span> را انتخاب کنید
          </motion.h1>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            از رایگان شروع کنید. هر زمان که نیاز داشتید ارتقا دهید. بدون تعهد بلندمدت.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, i) => {
            const Icon = plan.icon
            const isCurrent = user?.plan === plan.id
            return (
              <motion.div
                key={plan.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.15 }}
                className={`glass-card p-8 flex flex-col relative ${
                  plan.highlight ? 'border-primary-500/50 ring-2 ring-primary-500/20 md:scale-105 z-10' : ''
                }`}
              >
                {plan.highlight && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-primary-500 to-indigo-500 text-white text-xs font-bold px-4 py-1 rounded-full">
                    محبوب‌ترین
                  </span>
                )}

                <div className="flex items-center gap-3 mb-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${plan.highlight ? 'bg-primary-500/20 text-primary-400' : 'bg-slate-700/50 text-slate-400'}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white">{plan.name}</h3>
                    <p className="text-xs text-slate-500">{plan.nameEn}</p>
                  </div>
                </div>

                <p className="text-slate-400 text-sm mb-6">{plan.description}</p>

                <div className="mb-8">
                  {plan.price === 0 ? (
                    <span className="text-4xl font-extrabold text-white">رایگان</span>
                  ) : (
                    <>
                      <span className="text-4xl font-extrabold gradient-text ltr inline-block">${plan.price}</span>
                      <span className="text-slate-400 text-sm mr-1">/ماه</span>
                    </>
                  )}
                </div>

                <ul className="space-y-3 mb-8 flex-1">
                  {plan.features.map((f, j) => (
                    <li key={j} className="flex items-start gap-2 text-sm text-slate-300">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                      {f}
                    </li>
                  ))}
                </ul>

                {plan.href ? (
                  <Link href={plan.href} className="btn-secondary text-center block">{plan.cta}</Link>
                ) : isCurrent ? (
                  <button disabled className="btn-secondary opacity-60 cursor-not-allowed w-full">پلن فعلی شما</button>
                ) : (
                  <button
                    onClick={() => handleCheckout(plan)}
                    disabled={loading === plan.id}
                    className={`w-full flex items-center justify-center gap-2 ${plan.highlight ? 'btn-primary' : 'btn-secondary'}`}
                  >
                    {loading === plan.id ? <Loader2 className="w-4 h-4 animate-spin" /> : plan.cta}
                  </button>
                )}
              </motion.div>
            )
          })}
        </div>

        <p className="text-center text-slate-500 text-sm mt-12">
          تمام امکانات و ابزارها ۱۰۰٪ رایگان هستند.
        </p>
      </div>
    </>
  )
}
