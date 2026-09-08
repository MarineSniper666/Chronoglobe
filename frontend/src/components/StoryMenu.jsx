import { Play, X } from 'lucide-react';

export default function StoryMenu({ open, tours, onClose, onStart }) {
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-[70] flex items-center justify-center px-6"
      data-testid="story-menu"
      onClick={onClose}
    >
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div
        className="relative w-full max-w-3xl max-h-[80vh] overflow-y-auto scroll-thin glass rounded-3xl p-8"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between mb-6">
          <div>
            <div className="font-mono-x text-[10px] uppercase tracking-[0.3em] gold-text mb-1">
              Story Mode
            </div>
            <h2 className="font-serif-h text-3xl text-white">Pick a guided tour</h2>
            <p className="text-white/60 text-sm mt-2 leading-relaxed max-w-lg">
              Each tour visits several events with narration.
              Perfect for classrooms — press play and let it run.
            </p>
          </div>
          <button
            onClick={onClose}
            data-testid="close-story-menu"
            className="w-9 h-9 rounded-full glass flex items-center justify-center hover:border-white/30 transition-colors"
            aria-label="Close tour menu"
          >
            <X size={14} className="text-white/80" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {tours.map((t) => (
            <button
              key={t.id}
              onClick={() => onStart(t)}
              data-testid={`start-tour-${t.id}`}
              className="text-left p-5 rounded-2xl border border-white/10 hover:border-[#D4AF37]/50 hover:bg-white/[0.03] transition-colors group"
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40">
                  {t.stops.length} stops
                </span>
                <span className="text-white/20">·</span>
                <span className="font-mono-x text-[9px] uppercase tracking-[0.25em] gold-text">
                  ~{Math.round(t.stops.length * 1.2)} min
                </span>
              </div>
              <h3 className="font-serif-h text-xl text-white mb-1 leading-tight">
                {t.title}
              </h3>
              <div className="font-mono-x text-[10px] uppercase tracking-[0.2em] text-white/50 mb-3">
                {t.subtitle}
              </div>
              <p className="text-white/70 text-[13px] leading-relaxed">
                {t.description}
              </p>
              <div className="mt-4 inline-flex items-center gap-2 gold-text font-mono-x text-[11px] uppercase tracking-[0.2em] opacity-70 group-hover:opacity-100 transition-opacity">
                <Play size={11} />
                Start Tour
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
