import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  FileJson, BarChart3, Download, ArrowLeft, ShieldCheck, Filter,
  Zap, Globe, Users, CheckCircle2, Star, TrendingUp, Lock
} from 'lucide-react'
import { useTranslation } from 'react-i18next'

const colors = ['blue', 'purple', 'pink', 'emerald', 'amber', 'cyan']

const colorMap: Record<string, string> = {
  blue: 'bg-blue-500/20 text-blue-400',
  purple: 'bg-purple-500/20 text-purple-400',
  pink: 'bg-pink-500/20 text-pink-400',
  emerald: 'bg-emerald-500/20 text-emerald-400',
  amber: 'bg-amber-500/20 text-amber-400',
  cyan: 'bg-cyan-500/20 text-cyan-400',
}

const featureIcons = [FileJson, BarChart3, Filter, Download, ShieldCheck, Zap]
const featureKeys = ['upload', 'chart', 'filter', 'export', 'security', 'speed']

const statKeys = ['OutputFormats', 'FilterTypes', 'MaxFile', 'Uptime']

const steps = ['step1', 'step2', 'step3']

const planKeys = ['free', 'pro', 'business']

export default function Home() {
  const { t } = useTranslation()

  return (
    <>
      <Head>
        <title>{t('home.title')}</title>
        <meta name="description" content={t('home.description')} />
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
            <span>{t('home.badge')}</span>
          </div>

          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            {t('home.heroTitleBefore')}<span className="gradient-text">{t('home.heroTitleGradient')}</span>{t('home.heroTitleAfter')}
          </h1>

          <p className="text-lg md:text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            {t('home.heroDesc')}
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/signup" className="btn-primary flex items-center justify-center gap-2 text-lg px-8">
              {t('home.ctaStart')} <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/dashboard" className="btn-secondary flex items-center justify-center text-lg px-8">
              {t('home.ctaDashboard')}
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
          {statKeys.map((key, i) => (
            <div key={key} className="glass-card p-5 text-center">
              <div className="text-2xl md:text-3xl font-bold gradient-text">{t(`home.stats${key}Value`)}</div>
              <div className="text-sm text-slate-400 mt-1">{t(`home.stats${key}`)}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* Features */}
      <section className="py-24">
        <div className="text-center mb-16">
          <h2 className="section-title">{t('home.featuresTitle')}</h2>
          <p className="text-slate-400 max-w-xl mx-auto">{t('home.featuresDesc')}</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featureKeys.map((key, i) => {
            const Icon = featureIcons[i]
            return (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass-card p-8 group hover:border-primary-500/30"
              >
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-5 ${colorMap[colors[i]]}`}>
                  <Icon className="w-7 h-7" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{t(`home.feature${key.charAt(0).toUpperCase() + key.slice(1)}Title`)}</h3>
                <p className="text-slate-400 leading-relaxed">{t(`home.feature${key.charAt(0).toUpperCase() + key.slice(1)}Desc`)}</p>
              </motion.div>
            )
          })}
        </div>
      </section>

      {/* How it works */}
      <section className="py-24">
        <div className="glass-panel p-10 md:p-16">
          <h2 className="section-title text-center mb-12">{t('home.howItWorks')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step, i) => (
              <div key={step} className="text-center">
                <div className="w-12 h-12 rounded-full bg-primary-500/20 border border-primary-500/40 flex items-center justify-center text-primary-300 font-bold text-lg mx-auto mb-4">
                  {['۱', '۲', '۳'][i]}
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{t(`home.${step}Title`)}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{t(`home.${step}Desc`)}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing preview */}
      <section className="py-24">
        <div className="text-center mb-16">
          <h2 className="section-title">{t('home.pricingTitle')}</h2>
          <p className="text-slate-400">{t('home.pricingDesc')}</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {planKeys.map((key, i) => (
            <div key={key} className={`glass-card p-8 relative ${key === 'pro' ? 'border-primary-500/50 ring-1 ring-primary-500/30 scale-105' : ''}`}>
              {key === 'pro' && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-500 text-white text-xs font-bold px-3 py-1 rounded-full">{t('pricing.popular')}</span>
              )}
              <h3 className="text-xl font-bold text-white mb-2">{t(`pricing.plans.${key}.name`)}</h3>
              <div className="text-3xl font-extrabold gradient-text mb-6">{t('home.pricingFree')}</div>
              <ul className="space-y-3 mb-8">
                {(t(`pricing.plans.${key}.features`, { returnObjects: true }) as string[]).map((f: string, j: number) => (
                  <li key={j} className="flex items-center gap-2 text-sm text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link href="/pricing" className={`block text-center py-3 rounded-xl font-medium transition-all ${key === 'pro' ? 'btn-primary' : 'btn-secondary'}`}>
                {t('home.pricingChoose')}
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
              <h3 className="text-xl font-bold text-white">{t('home.trustTitle')}</h3>
              <p className="text-slate-400 text-sm mt-1">{t('home.trustDesc')}</p>
            </div>
          </div>
          <div className="flex items-center gap-6 text-slate-400">
            <div className="flex items-center gap-2"><Globe className="w-5 h-5" /><span className="text-sm">{t('home.trustRtl')}</span></div>
            <div className="flex items-center gap-2"><Users className="w-5 h-5" /><span className="text-sm">{t('home.trustMultiUser')}</span></div>
            <div className="flex items-center gap-2"><TrendingUp className="w-5 h-5" /><span className="text-sm">{t('home.trustAnalytics')}</span></div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">{t('home.ctaTitle')}</h2>
        <p className="text-slate-400 mb-8">{t('home.ctaDesc')}</p>
        <Link href="/auth/signup" className="btn-primary inline-flex items-center gap-2 text-lg px-10">
          {t('home.ctaButton')} <ArrowLeft className="w-5 h-5" />
        </Link>
      </section>
    </>
  )
}
