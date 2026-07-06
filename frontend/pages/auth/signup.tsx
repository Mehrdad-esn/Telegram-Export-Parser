import Head from 'next/head'
import { useState } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { UserPlus, Mail, Lock, AlertCircle, ArrowRight } from 'lucide-react'

export default function Signup() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const res = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      
      if (res.ok) {
        router.push('/auth/login?registered=true');
      } else {
        setError(data.detail || 'Signup failed');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head><title>ثبت‌نام | Telegram Parser</title></Head>
      <div className="flex items-center justify-center min-h-[80vh]">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <div className="glass-panel p-10">
            <div className="flex flex-col items-center mb-8 text-center">
              <div className="w-14 h-14 bg-emerald-100 dark:bg-emerald-900/50 rounded-2xl flex items-center justify-center mb-4">
                <UserPlus className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />
              </div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-white">ثبت‌نام</h2>
              <p className="text-slate-500 mt-2">تحلیل چت‌های تلگرام را شروع کنید</p>
            </div>

            {error && (
              <div className="mb-6 p-3 rounded-lg bg-red-50 text-red-600 text-sm flex items-center gap-2">
                <AlertCircle className="w-4 h-4" /> {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input 
                    type="email" 
                    value={email} 
                    onChange={e => setEmail(e.target.value)} 
                    required 
                    className="input-field pl-11"
                    placeholder="you@example.com"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input 
                    type="password" 
                    value={password} 
                    onChange={e => setPassword(e.target.value)} 
                    required 
                    className="input-field pl-11"
                    placeholder="Create a strong password"
                  />
                </div>
              </div>

              <button 
                className="btn-primary w-full mt-8 flex justify-center items-center gap-2 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:shadow-emerald-500/50 shadow-emerald-500/30" 
                type="submit"
                disabled={loading}
              >
                {loading ? 'در حال ایجاد...' : 'ایجاد حساب'}
                {!loading && <ArrowRight className="w-4 h-4" />}
              </button>
            </form>

            <p className="mt-8 text-center text-sm text-slate-500">
              قبلاً ثبت‌نام کرده‌اید؟{' '}
              <Link href="/auth/login" className="font-semibold text-emerald-600 hover:text-emerald-500">
                ورود
              </Link>
            </p>
          </div>
        </motion.div>
      </div>
    </>
  );
}