import { Globe, Map } from 'lucide-react';
import { formatYear, getEraName } from '../lib/history';

export default function Header({ mode, setMode, year, visibleCount }) {
  return (
    <header
      className="fixed top-0 left-0 right-0 z-40 px-6 py-5 flex items-center justify-between pointer-events-none"
      data-testid="app-header"
    >
      <div className="pointer-events-auto">
        <div className="font-mono-x text-[10px] uppercase tracking-[0.35em] text-white/40">
          A World History Atlas
        </div>
        <h1 className="font-serif-h text-3xl gold-text leading-none mt-1">Chronoglobe</h1>
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
            <div className="font-serif-h text-sm text-white/90 leading-none mt-1">
              {getEraName(year)}
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
