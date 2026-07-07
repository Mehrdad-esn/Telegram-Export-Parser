import Head from 'next/head'
import Link from 'next/link'
import { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { UploadCloud, BarChart3, Download, AlertCircle, Loader2, RefreshCw, MessageSquare } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { ProtectedRoute, useAuth } from '../../context/AuthContext'
import { apiFetch } from '../../lib/api'
import FilterPanel from '../../components/FilterPanel'
import { useTranslation } from 'react-i18next'

function formatNumber(n: number | string, locale: string): string {
  const num = typeof n === 'string' ? parseInt(n, 10) : n
  if (isNaN(num)) return String(n)
  return new Intl.NumberFormat(locale === 'fa' ? 'fa-IR' : 'en-US').format(num)
}

function DashboardContent() {
  const { user } = useAuth()
  const { t, i18n } = useTranslation()
  const locale = i18n.language
  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [errorMsg, setErrorMsg] = useState('')
  const [uploadId, setUploadId] = useState('')
  const [chats, setChats] = useState<any[]>([])
  const [selectedChat, setSelectedChat] = useState<number | null>(null)
  const [stats, setStats] = useState<any>(null)
  const [statsLoading, setStatsLoading] = useState(false)
  const [exportFormat, setExportFormat] = useState('csv')
  const [isExporting, setIsExporting] = useState(false)
  const [activeFilters, setActiveFilters] = useState<Record<string, unknown>>({})
  const [filtersActive, setFiltersActive] = useState(false)

  const fileInputRef = useRef<HTMLInputElement>(null)

  const allowedFormats = user?.usage?.formats || ['csv', 'txt', 'json', 'md', 'html', 'xlsx', 'excel']

  const uploadFile = async (file: File) => {
    if (!file.name.endsWith('.json')) {
      setErrorMsg(t('dashboard.uploadError'))
      setUploadState('error')
      return
    }

    setUploadState('uploading')
    setErrorMsg('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await apiFetch('/api/web/upload', { method: 'POST', body: formData })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || t('dashboard.uploadFailed'))

      setUploadId(data.upload_id)
      setChats(data.chats)
      setUploadState('success')
      setSelectedChat(null)
      setStats(null)
    } catch (err: any) {
      setErrorMsg(err.message)
      setUploadState('error')
    }
  }

  const loadStats = async (index: number, filters?: Record<string, unknown>) => {
    setSelectedChat(index)
    setStats(null)
    setStatsLoading(true)

    const f = filters ?? activeFilters
    const params = new URLSearchParams()
    if (f.start_date) params.set('start_date', String(f.start_date))
    if (f.end_date) params.set('end_date', String(f.end_date))
    if (f.senders) params.set('senders', (f.senders as string[]).join(','))
    if (f.keywords) params.set('keywords', (f.keywords as string[]).join(','))

    try {
      const qs = params.toString()
      const res = await apiFetch(`/api/web/stats/${uploadId}/${index}${qs ? '?' + qs : ''}`)
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'خطا در بارگذاری آمار')
      setStats(data)
    } catch (err: any) {
      alert(err.message)
      setSelectedChat(null)
    } finally {
      setStatsLoading(false)
    }
  }

  const handleApplyFilters = (filters: Record<string, unknown>) => {
    setActiveFilters(filters)
    setFiltersActive(Object.keys(filters).length > 0)
    if (selectedChat !== null) loadStats(selectedChat, filters)
  }

  const handleClearFilters = () => {
    setActiveFilters({})
    setFiltersActive(false)
    if (selectedChat !== null) loadStats(selectedChat, {})
  }

  const handleExport = async () => {
    if (selectedChat === null) return
    setIsExporting(true)

    try {
      const res = await apiFetch(`/api/web/export/${uploadId}`, {
        method: 'POST',
        body: JSON.stringify({
          chat_index: selectedChat,
          format: exportFormat,
          filters: Object.keys(activeFilters).length ? activeFilters : null,
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'خروجی ناموفق')

      window.location.href = `/api/web/download/${data.file_id}`
    } catch (err: any) {
      alert(err.message)
    } finally {
      setIsExporting(false)
    }
  }

  const resetUpload = () => {
    setUploadState('idle')
    setUploadId('')
    setChats([])
    setSelectedChat(null)
    setStats(null)
    setActiveFilters({})
    setFiltersActive(false)
  }

  const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#14b8a6', '#f59e0b']

  return (
    <>
      <Head><title>{t('dashboard.title')}</title></Head>

      <div className="w-full">
        {/* Guest alert banner */}
        {!user && (
          <div className="glass-panel px-6 py-4 mb-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm border-amber-500/20 bg-amber-500/5">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400">
                <AlertCircle className="w-4 h-4" />
              </div>
              <div className="text-right">
                <span className="text-slate-300 font-medium block sm:inline">{t('dashboard.guestAlert')}</span>
                <span className="text-slate-400 sm:mr-2">{t('dashboard.guestDesc')}</span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/auth/login" className="text-slate-300 hover:text-white transition-colors">{t('dashboard.guestLogin')}</Link>
              <Link href="/auth/signup" className="btn-primary py-1.5 px-4 text-xs">{t('dashboard.guestSignup')}</Link>
              {uploadState === 'success' && (
                <>
                  <span className="text-slate-600">|</span>
                  <button onClick={resetUpload} className="flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors">
                    <RefreshCw className="w-4 h-4" /> {t('dashboard.newUpload')}
                  </button>
                </>
              )}
            </div>
          </div>
        )}

        {/* Usage bar */}
        {user?.usage && (
          <div className="glass-panel px-6 py-3 mb-6 flex flex-wrap items-center justify-between gap-4 text-sm">
            <div className="flex items-center gap-4">
              <span className="text-slate-400">{t('dashboard.plan')}: <strong className="text-primary-300">{locale === 'en' ? user.usage.plan_name_en : user.usage.plan_name}</strong></span>
              <span className="text-slate-500">|</span>
              <span className="text-slate-400">
                {t('dashboard.upload')}: {formatNumber(user.usage.uploads_used, locale)}/{user.usage.uploads_limit ?? '∞'}
              </span>
              <span className="text-slate-400">
                {t('dashboard.export')}: {formatNumber(user.usage.exports_used, locale)}/{user.usage.exports_limit ?? '∞'}
              </span>
            </div>
            {uploadState === 'success' && (
              <button onClick={resetUpload} className="flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors">
                <RefreshCw className="w-4 h-4" /> {t('dashboard.newUpload')}
              </button>
            )}
          </div>
        )}

        {uploadState !== 'success' ? (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-2xl mx-auto mt-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-white">{t('dashboard.uploadTitle')}</h1>
              <p className="text-slate-400 mt-2">{t('dashboard.uploadDesc')}</p>
            </div>

            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => { e.preventDefault(); const f = e.dataTransfer.files?.[0]; if (f) uploadFile(f) }}
              onClick={() => fileInputRef.current?.click()}
              className={`glass-panel p-12 text-center cursor-pointer border-2 border-dashed transition-all duration-300
                ${uploadState === 'error' ? 'border-red-400/50 bg-red-900/10' :
                  uploadState === 'uploading' ? 'border-primary-400/50 bg-primary-900/10' :
                  'border-slate-600 hover:border-primary-500/50 hover:bg-primary-900/10'}`}
            >
              <input type="file" ref={fileInputRef} onChange={(e) => { const f = e.target.files?.[0]; if (f) uploadFile(f) }} accept=".json" className="hidden" />

              {uploadState === 'uploading' ? (
                <div className="flex flex-col items-center">
                  <Loader2 className="w-16 h-16 text-primary-400 animate-spin mb-4" />
                  <p className="text-lg font-medium text-primary-300">{t('dashboard.uploading')}</p>
                  <p className="text-sm text-slate-500 mt-2">{t('dashboard.uploadingHint')}</p>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <UploadCloud className={`w-16 h-16 mb-4 ${uploadState === 'error' ? 'text-red-400' : 'text-slate-500'}`} />
                  <p className="text-xl font-medium text-slate-200">{t('dashboard.dropzone')}</p>
                  <p className="text-sm text-slate-500 mt-2">{t('dashboard.dropzoneHint', { size: user?.usage?.max_file_size_mb ?? 10240 })}</p>
                </div>
              )}
            </div>

            {uploadState === 'error' && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-6 p-4 rounded-xl bg-red-900/20 text-red-400 flex items-center gap-3">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <p>{errorMsg}</p>
              </motion.div>
            )}
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Chat sidebar */}
            <div className="lg:col-span-4 glass-panel flex flex-col h-[80vh] overflow-hidden">
              <div className="p-5 border-b border-slate-700/50 flex items-center justify-between">
                <h2 className="text-lg font-bold text-white">{t('dashboard.chats')}</h2>
                <span className="px-3 py-1 bg-primary-500/20 text-primary-300 rounded-full text-xs font-semibold">{chats.length}</span>
              </div>
              <div className="flex-1 overflow-y-auto p-3 space-y-2">
                {chats.map((chat, idx) => (
                  <button
                    key={idx}
                    onClick={() => loadStats(idx)}
                    className={`w-full text-right p-4 rounded-xl transition-all border ${
                      selectedChat === idx
                        ? 'bg-primary-500/10 border-primary-500/50 ring-1 ring-primary-500/30'
                        : 'bg-slate-800/30 border-slate-700/50 hover:border-primary-500/30'
                    }`}
                  >
                    <div className="font-semibold text-white truncate">{chat.name}</div>
                    <div className="text-sm text-slate-400 mt-1 flex items-center gap-1">
                      <MessageSquare className="w-3 h-3" />
                      {formatNumber(chat.message_count, locale)} {t('dashboard.messages')}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Main panel */}
            <div className="lg:col-span-8 glass-panel min-h-[80vh] flex flex-col overflow-hidden">
              {selectedChat === null ? (
                <div className="flex-1 flex flex-col items-center justify-center text-slate-500 p-8 text-center">
                  <BarChart3 className="w-20 h-20 mb-4 opacity-30" />
                  <h3 className="text-xl font-medium text-slate-300">{t('dashboard.selectChat')}</h3>
                  <p className="mt-2 text-sm">{t('dashboard.selectChatHint')}</p>
                </div>
              ) : statsLoading ? (
                <div className="flex-1 flex flex-col items-center justify-center">
                  <Loader2 className="w-12 h-12 text-primary-400 animate-spin mb-4" />
                  <p className="text-slate-400">{t('dashboard.loadingStats')}</p>
                </div>
              ) : stats ? (
                <div className="flex-1 overflow-y-auto">
                  <div className="p-5 border-b border-slate-700/50 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sticky top-0 bg-dark-800/90 backdrop-blur-md z-10">
                    <div>
                      <h2 className="text-xl font-bold text-white">{chats[selectedChat].name}</h2>
                      <p className="text-slate-400 text-sm">
                        {formatNumber(stats.filtered_messages ?? stats.total_messages, locale)} {t('dashboard.messages')}
                        {stats.filters_applied && ` ${t('dashboard.fromTotal', { count: formatNumber(stats.total_unfiltered, locale) })}`}
                      </p>
                    </div>
                    <div className="flex items-center gap-3 flex-wrap">
                      <FilterPanel
                        availableSenders={stats.available_senders || []}
                        onApply={handleApplyFilters}
                        onClear={handleClearFilters}
                        active={filtersActive}
                      />
                      <div className="flex items-center gap-2 bg-slate-800/50 p-1.5 rounded-lg border border-slate-700/50">
                        <select
                          value={exportFormat}
                          onChange={(e) => setExportFormat(e.target.value)}
                          className="bg-transparent border-none text-sm font-medium focus:ring-0 cursor-pointer text-white"
                        >
                          {allowedFormats.includes('csv') && <option value="csv">CSV</option>}
                          {allowedFormats.includes('txt') && <option value="txt">Text</option>}
                          {allowedFormats.includes('json') && <option value="json">JSON</option>}
                          {(allowedFormats.includes('xlsx') || allowedFormats.includes('excel')) && <option value="excel">Excel</option>}
                          {allowedFormats.includes('md') && <option value="md">Markdown</option>}
                          {allowedFormats.includes('html') && <option value="html">HTML</option>}
                        </select>
                        <button onClick={handleExport} disabled={isExporting} className="btn-primary py-2 px-4 text-sm flex items-center gap-2">
                          {isExporting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                          {t('dashboard.exportLabel')}
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="p-5 space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      {[
                        { label: t('dashboard.totalMessages'), value: formatNumber(stats.total_messages, locale) },
                        { label: t('dashboard.dailyAvg'), value: formatNumber(Math.round(stats.daily_avg || 0), locale) },
                        { label: t('dashboard.avgLength'), value: `${stats.avg_message_length} ${t('dashboard.characters')}` },
                      ].map((m, i) => (
                        <div key={i} className="bg-slate-800/40 rounded-xl p-5 border border-slate-700/30">
                          <div className="text-slate-400 text-sm mb-1">{m.label}</div>
                          <div className="text-2xl font-bold text-white">{m.value}</div>
                        </div>
                      ))}
                    </div>

                    {stats.timeline?.length > 0 && (
                      <div className="bg-slate-800/30 rounded-xl p-5 border border-slate-700/30">
                        <h3 className="text-lg font-bold text-white mb-4">{t('dashboard.activityChart')}</h3>
                        <div className="h-56">
                          <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={stats.timeline}>
                              <defs>
                                <linearGradient id="colorMsg" x1="0" y1="0" x2="0" y2="1">
                                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                </linearGradient>
                              </defs>
                              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" opacity={0.2} />
                              <XAxis dataKey="date" tick={{ fontSize: 11 }} tickLine={false} axisLine={false} minTickGap={30} />
                              <YAxis tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                              <RechartsTooltip contentStyle={{ borderRadius: '12px', border: 'none', background: '#1e293b', color: '#fff' }} />
                              <Area type="monotone" dataKey="messages" stroke="#6366f1" strokeWidth={2} fill="url(#colorMsg)" />
                            </AreaChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                      <div className="bg-slate-800/30 rounded-xl p-5 border border-slate-700/30">
                        <h3 className="text-lg font-bold text-white mb-4">{t('dashboard.topTalkers')}</h3>
                        {stats.top_talkers_chart?.length > 0 ? (
                          <>
                            <div className="h-48">
                              <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                  <Pie data={stats.top_talkers_chart.slice(0, 5)} cx="50%" cy="50%" innerRadius={50} outerRadius={70} paddingAngle={4} dataKey="count">
                                    {stats.top_talkers_chart.slice(0, 5).map((_: any, index: number) => (
                                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                  </Pie>
                                  <RechartsTooltip contentStyle={{ borderRadius: '8px', border: 'none', background: '#1e293b', color: '#fff' }} />
                                </PieChart>
                              </ResponsiveContainer>
                            </div>
                            <div className="mt-3 space-y-2">
                              {stats.top_talkers_chart.slice(0, 5).map((p: any, idx: number) => (
                                <div key={idx} className="flex justify-between text-sm">
                                  <div className="flex items-center gap-2">
                                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[idx] }} />
                                    <span className="text-slate-300 truncate max-w-[140px]">{p.name}</span>
                                  </div>
                                  <span className="font-semibold text-white">{formatNumber(p.count, locale)}</span>
                                </div>
                              ))}
                            </div>
                          </>
                        ) : <p className="text-slate-500 text-center py-8">{t('dashboard.noData')}</p>}
                      </div>

                      <div className="bg-slate-800/30 rounded-xl p-5 border border-slate-700/30">
                        <h3 className="text-lg font-bold text-white mb-4">{t('dashboard.topWords')}</h3>
                        <div className="space-y-3">
                          {Object.entries(stats.top_words || {}).slice(0, 8).map(([word, count]: any, idx: number) => {
                            const maxCount = Object.values(stats.top_words)[0] as number
                            return (
                              <div key={idx}>
                                <div className="flex justify-between text-sm mb-1">
                                  <span className="text-slate-300">{word}</span>
                                  <span className="text-slate-500">{count}</span>
                                </div>
                                <div className="w-full bg-slate-700/50 rounded-full h-1.5">
                                  <div className="bg-gradient-to-l from-primary-400 to-primary-600 h-1.5 rounded-full" style={{ width: `${(count / maxCount) * 100}%` }} />
                                </div>
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        )}
      </div>
    </>
  )
}

export default function Dashboard() {
  return (
    <DashboardContent />
  )
}
