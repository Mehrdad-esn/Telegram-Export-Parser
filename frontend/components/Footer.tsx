import Link from 'next/link'
import { FileText, Github, Mail, Shield } from 'lucide-react'

const Footer = () => (
  <footer className="mt-auto border-t border-slate-800/50 bg-slate-950/50">
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="md:col-span-2">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="w-6 h-6 text-primary-500" />
            <span className="font-bold text-white text-lg">Telegram Export Parser</span>
          </div>
          <p className="text-slate-400 text-sm leading-relaxed max-w-md">
            ابزار حرفه‌ای تحلیل و خروجی‌گیری از چت‌های تلگرام. JSON خام را به گزارش‌های قابل استفاده، نمودارهای تحلیلی و فایل‌های CSV، Excel و Markdown تبدیل کنید.
          </p>
        </div>

        <div>
          <h4 className="font-semibold text-white mb-4">محصول</h4>
          <ul className="space-y-2 text-sm text-slate-400">
            <li><Link href="/dashboard" className="hover:text-primary-400 transition-colors">داشبورد</Link></li>
            <li><Link href="/pricing" className="hover:text-primary-400 transition-colors">قیمت‌ها</Link></li>
            <li><Link href="/auth/signup" className="hover:text-primary-400 transition-colors">ثبت‌نام</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-semibold text-white mb-4">امنیت</h4>
          <ul className="space-y-2 text-sm text-slate-400">
            <li className="flex items-center gap-2"><Shield className="w-3 h-3" /> پردازش امن</li>
            <li className="flex items-center gap-2"><Mail className="w-3 h-3" /> support@telegramparser.io</li>
          </ul>
        </div>
      </div>

      <div className="mt-10 pt-6 border-t border-slate-800/50 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p className="text-sm text-slate-500">
          © {new Date().getFullYear()} Telegram Export Parser. تمامی حقوق محفوظ است.
        </p>
        <p className="text-xs text-slate-600">ساخته شده با ❤️ برای تحلیل‌گران داده</p>
      </div>
    </div>
  </footer>
)

export default Footer;
