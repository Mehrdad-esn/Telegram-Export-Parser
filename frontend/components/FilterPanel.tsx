import { useState } from 'react';
import { Filter, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface FilterPanelProps {
  availableSenders: string[];
  onApply: (filters: Record<string, unknown>) => void;
  onClear: () => void;
  active: boolean;
}

export default function FilterPanel({ availableSenders, onApply, onClear, active }: FilterPanelProps) {
  const [open, setOpen] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedSenders, setSelectedSenders] = useState<string[]>([]);
  const [keywords, setKeywords] = useState('');
  const [regex, setRegex] = useState('');
  const [minLength, setMinLength] = useState('');
  const [maxLength, setMaxLength] = useState('');
  const [hasMedia, setHasMedia] = useState<string>('');
  const { t } = useTranslation();

  const handleApply = () => {
    const filters: Record<string, unknown> = {};
    if (startDate) filters.start_date = startDate;
    if (endDate) filters.end_date = endDate;
    if (selectedSenders.length) filters.senders = selectedSenders;
    if (keywords.trim()) filters.keywords = keywords.split(',').map(k => k.trim()).filter(Boolean);
    if (regex.trim()) filters.regex = regex.trim();
    if (minLength) filters.min_length = parseInt(minLength);
    if (maxLength) filters.max_length = parseInt(maxLength);
    if (hasMedia === 'yes') filters.has_media = true;
    if (hasMedia === 'no') filters.has_media = false;
    onApply(filters);
    setOpen(false);
  };

  const handleClear = () => {
    setStartDate('');
    setEndDate('');
    setSelectedSenders([]);
    setKeywords('');
    setRegex('');
    setMinLength('');
    setMaxLength('');
    setHasMedia('');
    onClear();
    setOpen(false);
  };

  const toggleSender = (sender: string) => {
    setSelectedSenders(prev =>
      prev.includes(sender) ? prev.filter(s => s !== sender) : [...prev, sender]
    );
  };

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all border ${
          active
            ? 'bg-primary-500/20 border-primary-500 text-primary-300'
            : 'bg-slate-800/50 border-slate-700 text-slate-300 hover:border-primary-500/50'
        }`}
      >
        <Filter className="w-4 h-4" />
        {t('filter.button')}
        {active && <span className="w-2 h-2 rounded-full bg-primary-400" />}
      </button>

      {open && (
        <div className="absolute top-full mt-2 left-0 right-0 md:left-auto md:right-0 z-50 w-80 glass-panel p-5 space-y-4 shadow-2xl">
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-white">{t('filter.title')}</h4>
            <button onClick={() => setOpen(false)} className="text-slate-400 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t('filter.startDate')}</label>
              <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="input-field text-sm py-2" />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t('filter.endDate')}</label>
              <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="input-field text-sm py-2" />
            </div>
          </div>

          <div>
            <label className="text-xs text-slate-400 mb-1 block">{t('filter.keywords')}</label>
            <input type="text" value={keywords} onChange={e => setKeywords(e.target.value)} placeholder={t('filter.keywordsPlaceholder')} className="input-field text-sm py-2" />
          </div>

          <div>
            <label className="text-xs text-slate-400 mb-1 block">{t('filter.regex')}</label>
            <input type="text" value={regex} onChange={e => setRegex(e.target.value)} placeholder={t('filter.regexPlaceholder')} className="input-field text-sm py-2 font-mono" dir="ltr" />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t('filter.minLength')}</label>
              <input type="number" value={minLength} onChange={e => setMinLength(e.target.value)} className="input-field text-sm py-2" />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t('filter.maxLength')}</label>
              <input type="number" value={maxLength} onChange={e => setMaxLength(e.target.value)} className="input-field text-sm py-2" />
            </div>
          </div>

          <div>
            <label className="text-xs text-slate-400 mb-1 block">{t('filter.media')}</label>
            <select value={hasMedia} onChange={e => setHasMedia(e.target.value)} className="input-field text-sm py-2">
              <option value="">{t('filter.mediaAll')}</option>
              <option value="yes">{t('filter.mediaWith')}</option>
              <option value="no">{t('filter.mediaWithout')}</option>
            </select>
          </div>

          {availableSenders.length > 0 && (
            <div>
              <label className="text-xs text-slate-400 mb-2 block">{t('filter.sender')}</label>
              <div className="max-h-32 overflow-y-auto space-y-1">
                {availableSenders.slice(0, 20).map(sender => (
                  <label key={sender} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer hover:text-white">
                    <input
                      type="checkbox"
                      checked={selectedSenders.includes(sender)}
                      onChange={() => toggleSender(sender)}
                      className="rounded border-slate-600"
                    />
                    <span className="truncate">{sender}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-2 pt-2">
            <button onClick={handleApply} className="btn-primary flex-1 py-2 text-sm">{t('filter.apply')}</button>
            <button onClick={handleClear} className="btn-secondary flex-1 py-2 text-sm">{t('filter.clear')}</button>
          </div>
        </div>
      )}
    </div>
  );
}
