import Head from 'next/head'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>Telegram Export Parser</title>
        <meta name="description" content="Frontend for Telegram Export Parser" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
        <h1 className="text-4xl font-bold mb-4">Telegram Export Parser</h1>
        <p className="mb-6 text-gray-600">Upload your Telegram export files and convert them to readable text or other formats.</p>
        <div className="space-x-4">
          <Link href="/auth/login"><a className="px-4 py-2 bg-blue-600 text-white rounded">Log in</a></Link>
          <Link href="/auth/signup"><a className="px-4 py-2 bg-green-600 text-white rounded">Sign up</a></Link>
          <Link href="/dashboard"><a className="px-4 py-2 bg-gray-200 text-gray-800 rounded">Dashboard</a></Link>
        </div>
      </main>
    </>
  )
}