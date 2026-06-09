import Link from 'next/link'

const Header = () => {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/"><a className="font-bold text-xl">Telegram Export Parser</a></Link>
        <nav className="space-x-4">
          <Link href="/dashboard"><a>Dashboard</a></Link>
          <Link href="/auth/login"><a>Login</a></Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;