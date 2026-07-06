import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  FileJson, BarChart3, Download, ArrowLeft, ShieldCheck, Filter,
  Zap, Globe, Users, CheckCircle2, Star, TrendingUp, Lock
} from 'lucide-react'

const features = [
  { icon: FileJson, title: 'آپلود JSON', desc: 'فایل result.json تلگرام را مستقیم آپلود کنید — پشتیبانی از export کامل و تک‌چت', color: 'blue' },
  { icon: BarChart3, title: 'تحلیل عمیق', desc: 'نمودار فعالیت روزانه، پرحرف‌ترین اعضا، پرتکرارترین کلمات و آمار دقیق', color: 'purple' },
  { icon: Filter, title: 'فیلتر پیشرفته', desc: 'فیلتر بر اساس تاریخ، فرستنده، کلمه کلیدی، regex و نوع رسانه', color: 'pink' },
  { icon: Download, title: 'خروجی چندفرمت', desc: 'CSV، Excel، TXT، Markdown، HTML و JSON — آماده برای Excel و BI', color: 'emerald' },
  { icon: ShieldCheck, title: 'امنیت داده', desc: 'پردازش امن با احراز هویت JWT و محدودیت دسترسی بر اساس پلن', color: 'amber' },
  { icon: Zap, title: 'سرعت بالا', desc: 'پردازش سریع فایل‌های بزرگ با موتور بهینه‌شده Python', color: 'cyan' },
]

const stats = [
  { value: '6+', label: 'فرمت خروجی' },
  { value: '6', label: 'نوع فیلتر' },
  { value: '۱۰GB', label: 'حداکثر فایل' },
  { value: '99.9%', label: 'آپ‌تایم' },
]

const plans = [
  { name: 'رایگان', price: '۰', features: ['آپلود نامحدود', 'خروجی نامحدود', 'CSV, TXT, JSON', 'فیلتر پایه', 'فایل تا ۱۰GB'] },
  { name: 'حرفه‌ای', price: '۰', features: ['آپلود نامحدود', 'خروجی نامحدود', 'همه فرمت‌ها', 'فیلتر پیشرفته', 'فایل تا ۱۰GB'], highlight: true },
  { name: 'سازمانی', price: '۰', features: ['آپلود نامحدود', 'خروجی نامحدود', 'همه فرمت‌ها', 'پشتیبانی اولویت‌دار', 'فایل تا ۱۰GB'] },
]

const colorMap: Record<string, string> = {
  blue: 'bg-blue-500/20 text-blue-400',
  purple: 'bg-purple-500/20 text-purple-400',
  pink: 'bg-pink-500/20 text-pink-400',
  emerald: 'bg-emerald-500/20 text-emerald-400',
  amber: 'bg-amber-500/20 text-amber-400',
  cyan: 'bg-cyan-500/20 text-cyan-400',
}

export default function Home() {
  return (
    <>
      <Head>
        <title>Telegram Export Parser | تحلیل حرفه‌ای چت‌های تلگرام</title>
        <meta name="description" content="ابزار تجاری تحلیل و خروجی‌گیری از export تلگرام — نمودار، فیلتر، CSV، Excel" />
      </Head>

      {/* Hero */}
      <section className="relative flex flex-col items-center justify-center min-h-[85vh] text-center overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-600/20 rounded-full blur-3xl animate-pulse-slow" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-indigo-600/15 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
        </div>

        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }} className="max-w-5xl mx-auto">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-300 font-medium text-sm mb-8">
            <Star className="w-4 h-4" />
            <span>ابزار تجاری تحلیل داده تلگرام</span>
          </div>

          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            قدرت <span className="gradient-text">داده‌های تلگرام</span>
            <br />را آزاد کنید
          </h1>

          <p className="text-lg md:text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            JSON خام export تلگرام را به گزارش‌های تحلیلی، نمودارهای تعاملی و فایل‌های CSV/Excel قابل استفاده تبدیل کنید — در چند ثانیه.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/signup" className="btn-primary flex items-center justify-center gap-2 text-lg px-8">
              شروع رایگان <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/dashboard" className="btn-secondary flex items-center justify-center text-lg px-8">
              مشاهده داشبورد
            </Link>
          </div>
        </motion.div>

        {/* Stats bar */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20 w-full max-w-3xl"
        >
          {stats.map((s, i) => (
            <div key={i} className="glass-card p-5 text-center">
              <div className="text-2xl md:text-3xl font-bold gradient-text">{s.value}</div>
              <div className="text-sm text-slate-400 mt-1">{s.label}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* Features */}
      <section className="py-24">
        <div className="text-center mb-16">
          <h2 className="section-title">همه چیز برای تحلیل حرفه‌ای</h2>
          <p className="text-slate-400 max-w-xl mx-auto">از آپلود تا خروجی — یک پلتفرم کامل برای تیم‌های داده، محققان و کسب‌وکارها</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass-card p-8 group hover:border-primary-500/30"
            >
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-5 ${colorMap[f.color]}`}>
                <f.icon className="w-7 h-7" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">{f.title}</h3>
              <p className="text-slate-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="py-24">
        <div className="glass-panel p-10 md:p-16">
          <h2 className="section-title text-center mb-12">چگونه کار می‌کند؟</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: '۱', title: 'Export از تلگرام', desc: 'در Telegram Desktop: Settings → Advanced → Export Telegram Data → JSON' },
              { step: '۲', title: 'آپلود و تحلیل', desc: 'فایل result.json را در داشبورد آپلود کنید و چت مورد نظر را انتخاب کنید' },
              { step: '۳', title: 'خروجی بگیرید', desc: 'نمودارها را ببینید، فیلتر کنید و به فرمت دلخواه دانلود کنید' },
            ].map((item, i) => (
              <div key={i} className="text-center">
                <div className="w-12 h-12 rounded-full bg-primary-500/20 border border-primary-500/40 flex items-center justify-center text-primary-300 font-bold text-lg mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{item.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing preview */}
      <section className="py-24">
        <div className="text-center mb-16">
          <h2 className="section-title">پلن‌های قیمت‌گذاری</h2>
          <p className="text-slate-400">از رایگان شروع کنید، هر زمان ارتقا دهید</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <div key={i} className={`glass-card p-8 relative ${plan.highlight ? 'border-primary-500/50 ring-1 ring-primary-500/30 scale-105' : ''}`}>
              {plan.highlight && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-500 text-white text-xs font-bold px-3 py-1 rounded-full">محبوب‌ترین</span>
              )}
              <h3 className="text-xl font-bold text-white mb-2">{plan.name}</h3>
              <div className="text-3xl font-extrabold gradient-text mb-6">رایگان</div>
              <ul className="space-y-3 mb-8">
                {plan.features.map((f, j) => (
                  <li key={j} className="flex items-center gap-2 text-sm text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link href="/pricing" className={`block text-center py-3 rounded-xl font-medium transition-all ${plan.highlight ? 'btn-primary' : 'btn-secondary'}`}>
                انتخاب پلن
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Trust */}
      <section className="py-16">
        <div className="glass-panel p-10 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 flex items-center justify-center">
              <Lock className="w-8 h-8 text-emerald-400" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">امنیت در اولویت</h3>
              <p className="text-slate-400 text-sm mt-1">احراز هویت JWT، محدودیت دسترسی و پردازش امن داده‌ها</p>
            </div>
          </div>
          <div className="flex items-center gap-6 text-slate-400">
            <div className="flex items-center gap-2"><Globe className="w-5 h-5" /><span className="text-sm">RTL Support</span></div>
            <div className="flex items-center gap-2"><Users className="w-5 h-5" /><span className="text-sm">Multi-user</span></div>
            <div className="flex items-center gap-2"><TrendingUp className="w-5 h-5" /><span className="text-sm">Analytics</span></div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">آماده تحلیل چت‌هایتان هستید؟</h2>
        <p className="text-slate-400 mb-8">همین الان ثبت‌نام کنید — رایگان و بدون نیاز به کارت اعتباری</p>
        <Link href="/auth/signup" className="btn-primary inline-flex items-center gap-2 text-lg px-10">
          شروع رایگان <ArrowLeft className="w-5 h-5" />
        </Link>
      </section>
    </>
  )
}
