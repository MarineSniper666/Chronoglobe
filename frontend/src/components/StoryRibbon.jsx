import { Pause, Play, SkipForward, SkipBack, X, Clapperboard } from 'lucide-react';

export default function StoryRibbon({
  tour, stopIndex, total, paused, isLast,
  onPause, onResume, onNext, onPrev, onExit,
}) {
  if (!tour) return null;
  return (
    <div
      className="fixed top-24 left-1/2 -translate-x-1/2 z-[55] pointer-events-none"
      data-testid="story-ribbon"
    >
      <div className="glass rounded-full pl-4 pr-2 py-1.5 flex items-center gap-4 pointer-events-auto gold-border border">
        <Clapperboard size={13} className="gold-text" />
        <div className="flex flex-col leading-tight">
          <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40">
            Story · Stop {stopIndex + 1} of {total}
          </div>
          <div className="font-serif-h text-[15px] text-white truncate max-w-[380px]">
            {tour.title}
          </div>
        </div>

        {/* Progress dots */}
        <div className="flex items-center gap-1.5" data-testid="story-progress">
          {Array.from({ length: total }).map((_, i) => (
            <span
              key={i}
              className={`w-1.5 h-1.5 rounded-full transition-colors ${
                i === stopIndex ? 'bg-[#D4AF37]' :
                i < stopIndex ? 'bg-[#D4AF37]/50' : 'bg-white/15'
              }`}
            />
          ))}
        </div>

        <div className="w-px h-6 bg-white/10" />

        <button
          onClick={onPrev}
          data-testid="story-prev"
          disabled={stopIndex === 0}
          className="w-7 h-7 rounded-full flex items-center justify-center text-white/70 hover:text-white disabled:opacity-30 transition-colors"
          aria-label="Previous stop"
        >
          <SkipBack size={11} />
        </button>
        <button
          onClick={paused ? onResume : onPause}
          data-testid="story-pause"
          className="w-7 h-7 rounded-full flex items-center justify-center gold-text hover:bg-white/5 transition-colors"
          aria-label={paused ? 'Resume tour' : 'Pause tour'}
        >
          {paused ? <Play size={12} /> : <Pause size={12} />}
        </button>
        <button
          onClick={onNext}
          data-testid="story-next"
          disabled={isLast}
          className="w-7 h-7 rounded-full flex items-center justify-center text-white/70 hover:text-white disabled:opacity-30 transition-colors"
          aria-label="Next stop"
        >
          <SkipForward size={11} />
        </button>
        <button
          onClick={onExit}
          data-testid="story-exit"
          className="w-7 h-7 rounded-full flex items-center justify-center text-white/70 hover:text-[#8B0000] transition-colors"
          aria-label="Exit tour"
        >
          <X size={12} />
        </button>
      </div>
    </div>
  );
}
