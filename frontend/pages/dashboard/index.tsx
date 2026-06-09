import Head from 'next/head'
import UploadForm from '../../components/UploadForm'

export default function Dashboard() {
  return (
    <>
      <Head><title>Dashboard</title></Head>
      <div className="min-h-screen p-8 bg-gray-50">
        <h1 className="text-3xl mb-6">Dashboard</h1>
        <UploadForm />
      </div>
    </>
  );
}