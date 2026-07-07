import Link from 'next/link'
import { FileText, Github, Mail, Shield } from 'lucide-react'
import { useTranslation } from 'react-i18next'

const Footer = () => {
  const { t } = useTranslation()

  return (
    <footer className="mt-auto border-t border-slate-800/50 bg-slate-950/50">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-6 h-6 text-primary-500" />
              <span className="font-bold text-white text-lg">{t('footer.brand')}</span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed max-w-md">
              {t('footer.description')}
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">{t('footer.product')}</h4>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><Link href="/dashboard" className="hover:text-primary-400 transition-colors">{t('footer.dashboard')}</Link></li>
              <li><Link href="/pricing" className="hover:text-primary-400 transition-colors">{t('footer.pricing')}</Link></li>
              <li><Link href="/auth/signup" className="hover:text-primary-400 transition-colors">{t('footer.signup')}</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-4">{t('footer.security')}</h4>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex items-center gap-2"><Shield className="w-3 h-3" /> {t('footer.secureProcessing')}</li>
              <li className="flex items-center gap-2"><Mail className="w-3 h-3" /> {t('footer.email')}</li>
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-slate-800/50 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm text-slate-500">
            {t('footer.copyright', { year: new Date().getFullYear() })}
          </p>
          <p className="text-xs text-slate-600">{t('footer.madeWith')}</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer;
