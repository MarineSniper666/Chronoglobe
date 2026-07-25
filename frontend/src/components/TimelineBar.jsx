import { Play, Pause, Gauge, RotateCcw } from 'lucide-react';
import {
  TIMELINE_START, TIMELINE_END, TIMELINE_TICKS,
  formatYear, getEraName, getSubPeriod,
} from '../lib/history';

export default function TimelineBar({
  year, setYear, playing, togglePlay, speed, cycleSpeed, onReset,
}) {
  const range = TIMELINE_END - TIMELINE_START;
  const pct = ((year - TIMELINE_START) / range) * 100;
  const sub = getSubPeriod(year);

  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-40 px-6 pb-6 pointer-events-none"
      data-testid="timeline-bar"
    >
      <div className="glass rounded-2xl px-6 py-5 pointer-events-auto max-w-6xl mx-auto">
        <div className="flex items-center gap-5">
          <button
            onClick={togglePlay}
            data-testid="play-button"
            className="w-11 h-11 rounded-full flex items-center justify-center gold-border border transition-colors duration-200 hover:bg-[#D4AF37]/10"
            aria-label={playing ? 'Pause' : 'Play'}
          >
            {playing ? <Pause size={16} className="gold-text" /> : <Play size={16} className="gold-text ml-0.5" />}
          </button>

          <button
            onClick={onReset}
            data-testid="reset-button"
            className="w-9 h-9 rounded-full flex items-center justify-center border border-white/10 hover:border-white/30 transition-colors duration-200"
            aria-label="Restart timeline"
          >
            <RotateCcw size={13} className="text-white/70" />
          </button>

          <div className="flex-1">
            <div className="flex items-baseline justify-between mb-2">
              <div>
                <div className="font-mono-x text-[10px] uppercase tracking-[0.2em] text-white/40 flex items-center gap-2">
                  <span>{getEraName(year)}</span>
                  {sub && (
                    <>
                      <span className="text-white/20">·</span>
                      <span
                        className="gold-text"
                        data-testid="sub-period-label"
                      >
                        {sub.name}
                      </span>
                    </>
                  )}
                </div>
                <div
                  className="font-serif-h text-2xl gold-text"
                  data-testid="current-year"
                >
                  {formatYear(year)}
                </div>
              </div>
              <div className="font-mono-x text-[10px] uppercase tracking-[0.2em] text-white/40 text-right">
                <div>25,000 BCE → 2026 CE</div>
                <div className="mt-0.5">{Math.round(pct)}%</div>
              </div>
            </div>

            <div className="relative">
              {/* Sub-era tick labels above the track */}
              <div className="absolute -top-3 left-0 right-0 h-3 pointer-events-none">
                {TIMELINE_TICKS.map((t) => {
                  const left = ((t.start - TIMELINE_START) / range) * 100;
                  if (left < 0 || left > 100) return null;
                  return (
                    <div
                      key={t.id}
                      className="absolute -translate-x-1/2"
                      style={{ left: `${left}%` }}
                      data-testid={`tick-${t.id}`}
                    >
                      <div className="w-px h-2 bg-white/25 mx-auto" />
                    </div>
                  );
                })}
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
                  min={TIMELINE_START}
                  max={TIMELINE_END}
                  step={1}
                  value={Math.round(year)}
                  onChange={(e) => setYear(Number(e.target.value))}
                  data-testid="timeline-slider"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  aria-label="Timeline scrubber"
                />
              </div>

              {/* Tiny labels below the track for major ticks */}
              <div className="relative mt-1 h-3 pointer-events-none">
                {TIMELINE_TICKS.map((t) => {
                  const left = ((t.start - TIMELINE_START) / range) * 100;
                  if (left < 3 || left > 97) return null;
                  return (
                    <div
                      key={`lbl-${t.id}`}
                      className="absolute -translate-x-1/2 font-mono-x text-[8px] text-white/35 whitespace-nowrap"
                      style={{ left: `${left}%` }}
                    >
                      {t.name}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          <button
            onClick={cycleSpeed}
            data-testid="speed-button"
            className="px-3 h-9 rounded-full flex items-center gap-2 border border-white/10 hover:border-white/30 font-mono-x text-xs text-white/80 transition-colors duration-200"
          >
            <Gauge size={12} />
            {speed.label}
          </button>
        </div>
      </div>
    </div>
  );
}
