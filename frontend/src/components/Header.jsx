import { Globe, Map, Columns, Link2, Bookmark } from 'lucide-react';
import { formatYear, getEraName, getSubPeriod } from '../lib/history';

export default function Header({
  mode, setMode, year, visibleCount, compareOn, toggleCompare,
  onShare, onOpenBookmarks, bookmarkCount = 0,
}) {
  const sub = getSubPeriod(year);
  return (
    <header
      className="fixed top-0 left-0 right-0 z-[60] px-6 py-5 flex items-center justify-between pointer-events-none"
      data-testid="app-header"
    >
      <div className="pointer-events-auto flex items-center gap-3">
        <button
          onClick={onOpenBookmarks}
          data-testid="open-bookmarks"
          className="glass rounded-full h-9 px-3 flex items-center gap-2 text-white/70 hover:text-white font-mono-x text-xs transition-colors duration-200"
          title="Your saved moments"
          aria-label="Open bookmarks drawer"
        >
          <Bookmark size={12} />
          {bookmarkCount > 0 && (
            <span className="gold-text" data-testid="bookmark-count">{bookmarkCount}</span>
          )}
        </button>
        <button
          onClick={onShare}
          data-testid="share-button"
          className="glass rounded-full w-9 h-9 flex items-center justify-center text-white/70 hover:text-white transition-colors duration-200"
          title="Copy shareable link to this moment"
          aria-label="Copy shareable link"
        >
          <Link2 size={13} />
        </button>
        <div>
          <div className="font-mono-x text-[10px] uppercase tracking-[0.35em] text-white/40">
            A World History Atlas
          </div>
          <h1 className="font-serif-h text-3xl gold-text leading-none mt-1">Chronoglobe</h1>
        </div>
      </div>

      <div className="pointer-events-auto flex items-center gap-4">
        <div className="glass rounded-full px-4 py-2 flex items-center gap-4">
          <div className="text-right">
            <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40">
              Now Showing
            </div>
            <div className="font-serif-h text-lg text-white leading-none mt-0.5">
              {formatYear(year)}
            </div>
          </div>
          <div className="w-px h-8 bg-white/10" />
          <div>
            <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40">
              Era
            </div>
            <div className="font-serif-h text-sm text-white/90 leading-none mt-1 flex items-center gap-1.5">
              {getEraName(year)}
              {sub && (
                <>
                  <span className="text-white/25">·</span>
                  <span className="gold-text" data-testid="header-sub-period">{sub.name}</span>
                </>
              )}
            </div>
          </div>
          <div className="w-px h-8 bg-white/10" />
          <div>
            <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40">
              Events
            </div>
            <div className="font-mono-x text-sm gold-text leading-none mt-1" data-testid="visible-count">
              {visibleCount}
            </div>
          </div>
        </div>

        <button
          onClick={toggleCompare}
          data-testid="compare-toggle"
          aria-pressed={compareOn}
          className={`glass rounded-full px-3.5 h-9 flex items-center gap-2 font-mono-x text-xs transition-colors duration-200
            ${compareOn ? 'gold-border gold-text bg-[#D4AF37]/10' : 'text-white/70 hover:text-white'}`}
          title="Compare two years side by side"
        >
          <Columns size={12} /> {compareOn ? 'Comparing' : 'Compare'}
        </button>

        <div className="glass rounded-full p-1 flex items-center gap-1" role="tablist" aria-label="View mode">
          <button
            onClick={() => setMode('3d')}
            data-testid="mode-3d"
            aria-pressed={mode === '3d'}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono-x transition-colors duration-200
              ${mode === '3d' ? 'bg-[#D4AF37] text-[#030304]' : 'text-white/70 hover:text-white'}`}
          >
            <Globe size={12} /> 3D
          </button>
          <button
            onClick={() => setMode('2d')}
            data-testid="mode-2d"
            aria-pressed={mode === '2d'}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono-x transition-colors duration-200
              ${mode === '2d' ? 'bg-[#D4AF37] text-[#030304]' : 'text-white/70 hover:text-white'}`}
            aria-label="Switch to 2D accessibility map"
          >
            <Map size={12} /> 2D
          </button>
        </div>
      </div>
    </header>
  );
}
