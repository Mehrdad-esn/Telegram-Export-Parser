import Head from 'next/head'
import { useState } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { LogIn, Mail, Lock, AlertCircle, ArrowRight } from 'lucide-react'
import { setTokens } from '../../lib/api'

export default function Login() {
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
      // Create x-www-form-urlencoded format for OAuth2PasswordRequestForm
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });
      const data = await res.json();
      
      if (res.ok) {
        setTokens(data.access_token, data.refresh_token);
        const redirect = typeof router.query.redirect === 'string' ? router.query.redirect : '/dashboard';
        router.push(redirect);
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head><title>ورود | Telegram Parser</title></Head>
      <div className="flex items-center justify-center min-h-[80vh]">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <div className="glass-panel p-10">
            <div className="flex flex-col items-center mb-8 text-center">
              <div className="w-14 h-14 bg-primary-100 dark:bg-primary-900/50 rounded-2xl flex items-center justify-center mb-4">
                <LogIn className="w-7 h-7 text-primary-600 dark:text-primary-400" />
              </div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-white">خوش آمدید</h2>
              <p className="text-slate-500 mt-2">برای ادامه وارد حساب خود شوید</p>
            </div>

            {error && (
              <div className="mb-6 p-3 rounded-lg bg-red-50 text-red-600 text-sm flex items-center gap-2">
                <AlertCircle className="w-4 h-4" /> {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">ایمیل</label>
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
                <div className="flex justify-between mb-2">
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">رمز عبور</label>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input 
                    type="password" 
                    value={password} 
                    onChange={e => setPassword(e.target.value)} 
                    required 
                    className="input-field pl-11"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <button 
                className="btn-primary w-full mt-8 flex justify-center items-center gap-2" 
                type="submit"
                disabled={loading}
              >
                {loading ? 'در حال ورود...' : 'ورود'}
                {!loading && <ArrowRight className="w-4 h-4" />}
              </button>
            </form>

            <p className="mt-8 text-center text-sm text-slate-500">
              حساب ندارید؟{' '}
              <Link href="/auth/signup" className="font-semibold text-primary-600 hover:text-primary-500">
                ثبت‌نام
              </Link>
            </p>
          </div>
        </motion.div>
      </div>
    </>
  );
}