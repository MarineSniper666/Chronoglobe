import { useEffect, useMemo, useRef, useState } from 'react';
import { Search, X } from 'lucide-react';
import { CATEGORIES, formatYear } from '../lib/history';

export default function SearchBox({ events, onPick }) {
  const [q, setQ] = useState('');
  const [open, setOpen] = useState(false);
  const [idx, setIdx] = useState(0);
  const inputRef = useRef(null);
  const wrapRef = useRef(null);

  const results = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return [];
    return events
      .filter((e) =>
        e.title.toLowerCase().includes(s) ||
        e.region.toLowerCase().includes(s) ||
        e.summary.toLowerCase().includes(s)
      )
      .slice(0, 8);
  }, [q, events]);

  useEffect(() => {
    const onClickAway = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', onClickAway);
    return () => document.removeEventListener('mousedown', onClickAway);
  }, []);

  useEffect(() => {
    const onKey = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
        setOpen(true);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const pick = (e) => {
    onPick(e);
    setQ('');
    setOpen(false);
  };

  return (
    <div
      ref={wrapRef}
      className="fixed left-1/2 -translate-x-1/2 top-6 z-40 w-80"
      data-testid="search-box"
    >
      <div className="glass rounded-full flex items-center px-4 h-11 gap-3 focus-within:border-[#D4AF37]/40">
        <Search size={14} className="text-white/50" />
        <input
          ref={inputRef}
          value={q}
          onChange={(e) => { setQ(e.target.value); setOpen(true); setIdx(0); }}
          onFocus={() => setOpen(true)}
          onKeyDown={(e) => {
            if (!results.length) return;
            if (e.key === 'ArrowDown') { setIdx((i) => (i + 1) % results.length); e.preventDefault(); }
            else if (e.key === 'ArrowUp') { setIdx((i) => (i - 1 + results.length) % results.length); e.preventDefault(); }
            else if (e.key === 'Enter') { pick(results[idx]); }
            else if (e.key === 'Escape') { setOpen(false); }
          }}
          placeholder="Search history…  (⌘K)"
          data-testid="search-input"
          className="bg-transparent outline-none flex-1 text-white/90 placeholder:text-white/30 font-mono-x text-xs tracking-wide"
        />
        {q && (
          <button
            onClick={() => { setQ(''); inputRef.current?.focus(); }}
            data-testid="search-clear"
            className="text-white/40 hover:text-white/80"
            aria-label="Clear search"
          >
            <X size={12} />
          </button>
        )}
      </div>
      {open && results.length > 0 && (
        <div className="glass mt-2 rounded-2xl overflow-hidden" data-testid="search-results">
          {results.map((e, i) => {
            const cat = CATEGORIES[e.category];
            return (
              <button
                key={e.id}
                onClick={() => pick(e)}
                data-testid={`search-result-${e.id}`}
                className={`w-full text-left px-4 py-3 flex items-start gap-3 border-b border-white/5 last:border-0
                  ${i === idx ? 'bg-white/5' : 'hover:bg-white/[0.03]'}`}
              >
                <span className={`mt-1.5 w-2 h-2 rounded-full ${cat.dot} shrink-0`} />
                <div className="min-w-0 flex-1">
                  <div className="font-serif-h text-[15px] text-white/95 leading-tight truncate">
                    {e.title}
                  </div>
                  <div className="font-mono-x text-[10px] text-white/45 mt-1 flex items-center gap-2">
                    <span>{formatYear(e.year)}</span>
                    <span className="text-white/25">·</span>
                    <span className="truncate">{e.region}</span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
