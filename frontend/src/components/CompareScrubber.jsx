import { formatYear, getEraName } from '../lib/history';

export default function CompareScrubber({ yearB, setYearB, min, max }) {
  const pct = ((yearB - min) / (max - min)) * 100;
  return (
    <div
      className="fixed bottom-32 left-1/2 -translate-x-1/2 z-40 pointer-events-none"
      data-testid="compare-scrubber"
    >
      <div className="glass rounded-2xl px-5 py-3 pointer-events-auto w-[560px] max-w-[92vw]">
        <div className="flex items-baseline justify-between mb-1.5">
          <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40">
            Globe B · {getEraName(yearB)}
          </div>
          <div className="font-serif-h text-base gold-text" data-testid="compare-year">
            {formatYear(yearB)}
          </div>
        </div>
        <div className="relative h-1.5 rounded-full bg-white/10 overflow-hidden">
          <div
            className="absolute inset-y-0 left-0 rounded-full"
            style={{
              width: `${pct}%`,
              background: 'linear-gradient(90deg, #4A5568 0%, #D4AF37 100%)',
            }}
          />
          <input
            type="range"
            min={min}
            max={max}
            step={1}
            value={Math.round(yearB)}
            onChange={(e) => setYearB(Number(e.target.value))}
            data-testid="compare-slider"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            aria-label="Compare year"
          />
        </div>
      </div>
    </div>
  );
}
