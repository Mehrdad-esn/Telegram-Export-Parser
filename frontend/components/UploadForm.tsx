import { useState } from 'react'

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setStatus('Uploading...');
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        setStatus('Upload successful');
      } else {
        setStatus('Upload failed');
      }
    } catch (err) {
      console.error(err);
      setStatus('Upload error');
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md max-w-lg">
      <label className="block mb-2">Select export file
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} className="mt-2" />
      </label>
      <button type="submit" className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Upload</button>
      {status && <p className="mt-2 text-sm text-gray-600">{status}</p>}
    </form>
  )
}