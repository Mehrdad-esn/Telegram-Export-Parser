import Head from 'next/head'
import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Placeholder: replace with actual backend call
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (res.ok) {
        // On success redirect to dashboard
        router.push('/dashboard');
      } else {
        console.error('Login failed');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <Head><title>Login</title></Head>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-md">
          <h2 className="text-2xl mb-4">Log in</h2>
          <label className="block mb-2">Email<input type="email" value={email} onChange={e => setEmail(e.target.value)} required className="w-full border p-2 rounded"/></label>
          <label className="block mb-4">Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} required className="w-full border p-2 rounded"/></label>
          <button className="w-full bg-blue-600 text-white py-2 rounded" type="submit">Log in</button>
        </form>
      </div>
    </>
  );
}