import { useEffect, useMemo, useState } from 'react';
import { Bookmark, Download, Upload, Trash2, X, MapPin } from 'lucide-react';
import {
  listBookmarks, removeBookmark, exportBookmarksJson,
  importBookmarksJson, clearBookmarks,
} from '../lib/bookmarks';
import { CATEGORIES, formatYear } from '../lib/history';

export default function BookmarksDrawer({ open, onClose, onPick, refreshTick }) {
  const [items, setItems] = useState([]);
  const [err, setErr] = useState(null);

  useEffect(() => { if (open) setItems(listBookmarks()); }, [open, refreshTick]);

  const handleExport = () => {
    const text = exportBookmarksJson();
    const blob = new Blob([text], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chronoglobe-bookmarks-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  };

  const handleImport = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const merged = importBookmarksJson(ev.target.result);
        setItems(merged);
        setErr(null);
      } catch (e2) { setErr(e2.message); }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  const grouped = useMemo(() => {
    return [...items].sort((a, b) => a.year - b.year);
  }, [items]);

  if (!open) return null;

  return (
    <aside
      className="fixed top-0 left-0 h-full w-full sm:w-[380px] z-50 glass-panel flex flex-col"
      data-testid="bookmarks-drawer"
      style={{ animation: 'slideinL 0.3s ease-out' }}
    >
      <style>{`@keyframes slideinL { from { transform: translateX(-100%);} to { transform: translateX(0);} }`}</style>

      <div className="px-6 pt-6 pb-4 flex items-center justify-between border-b border-white/5">
        <div className="flex items-center gap-2.5">
          <Bookmark size={16} className="gold-text" />
          <h2 className="font-serif-h text-xl text-white">Your Moments</h2>
          <span className="font-mono-x text-[10px] text-white/40 ml-1">{items.length}</span>
        </div>
        <button
          onClick={onClose}
          data-testid="close-bookmarks"
          className="w-8 h-8 rounded-full glass flex items-center justify-center hover:border-white/30 transition-colors"
          aria-label="Close bookmarks"
        >
          <X size={13} className="text-white/70" />
        </button>
      </div>

      <div className="flex items-center gap-2 px-6 py-3 border-b border-white/5">
        <button
          onClick={handleExport}
          disabled={!items.length}
          data-testid="export-bookmarks"
          className="flex items-center gap-1.5 px-3 h-7 rounded-full border border-white/10 hover:border-[#D4AF37]/40 text-[10px] font-mono-x uppercase tracking-[0.2em] text-white/80 disabled:opacity-40 transition-colors"
        >
          <Download size={10} /> Export
        </button>
        <label
          data-testid="import-bookmarks-label"
          className="flex items-center gap-1.5 px-3 h-7 rounded-full border border-white/10 hover:border-[#D4AF37]/40 text-[10px] font-mono-x uppercase tracking-[0.2em] text-white/80 cursor-pointer transition-colors"
        >
          <Upload size={10} /> Import
          <input
            type="file"
            accept="application/json"
            onChange={handleImport}
            data-testid="import-bookmarks-input"
            className="hidden"
          />
        </label>
        {items.length > 0 && (
          <button
            onClick={() => { clearBookmarks(); setItems([]); }}
            data-testid="clear-bookmarks"
            className="ml-auto flex items-center gap-1.5 px-3 h-7 rounded-full border border-white/10 hover:border-[#8B0000]/60 text-[10px] font-mono-x uppercase tracking-[0.2em] text-white/60 transition-colors"
          >
            <Trash2 size={10} /> Clear
          </button>
        )}
      </div>

      {err && (
        <div className="px-6 py-2 text-[11px] font-mono-x text-[#8B0000]" data-testid="bookmarks-error">
          {err}
        </div>
      )}

      <div className="flex-1 overflow-y-auto scroll-thin px-3 py-2" data-testid="bookmarks-list">
        {items.length === 0 ? (
          <div className="text-center px-6 py-16 text-white/40">
            <div className="font-serif-h text-lg mb-2">No bookmarks yet</div>
            <div className="font-mono-x text-[11px] leading-relaxed">
              Star any event from the side panel to save it here.
              Great for building a classroom playlist.
            </div>
          </div>
        ) : (
          grouped.map((b) => {
            const cat = CATEGORIES[b.category];
            return (
              <div
                key={b.id}
                className="group flex items-start gap-3 px-3 py-3 rounded-lg hover:bg-white/[0.03] border border-transparent hover:border-white/10 transition-colors"
                data-testid={`bookmark-${b.event_id}`}
              >
                <button
                  onClick={() => onPick(b.event_id)}
                  className="flex-1 text-left flex items-start gap-3"
                >
                  <span className={`mt-1.5 w-2 h-2 rounded-full ${cat?.dot || 'dot-civ'} shrink-0`} />
                  <div className="min-w-0 flex-1">
                    <div className="font-serif-h text-[15px] text-white/95 leading-tight truncate">
                      {b.title}
                    </div>
                    <div className="flex items-center gap-2 mt-1 font-mono-x text-[10px] text-white/45">
                      <span>{formatYear(b.year)}</span>
                      <span className="text-white/25">·</span>
                      <MapPin size={9} />
                      <span className="truncate">{b.region}</span>
                    </div>
                  </div>
                </button>
                <button
                  onClick={() => setItems(removeBookmark(b.event_id))}
                  data-testid={`remove-bookmark-${b.event_id}`}
                  className="opacity-0 group-hover:opacity-100 w-7 h-7 rounded-full flex items-center justify-center hover:bg-[#8B0000]/20 transition"
                  aria-label={`Remove bookmark for ${b.title}`}
                >
                  <Trash2 size={11} className="text-white/60" />
                </button>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}
