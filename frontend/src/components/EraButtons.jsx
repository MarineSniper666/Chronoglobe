import { useEffect, useState } from 'react';
import { ERAS, ERA_COOLDOWN_MS } from '../lib/history';

/**
 * Era jump buttons with a 2.5-minute cooldown per button.
 * Displays a circular progress ring for the cooldown.
 */
export default function EraButtons({ onJump }) {
  const [cooldowns, setCooldowns] = useState({}); // { eraId: expiresAt }
  const [, setTick] = useState(0);

  useEffect(() => {
    const iv = setInterval(() => setTick((t) => t + 1), 500);
    return () => clearInterval(iv);
  }, []);

  const handleClick = (era) => {
    const now = Date.now();
    if (cooldowns[era.id] && cooldowns[era.id] > now) return;
    onJump(era.jumpTo);
    setCooldowns((c) => ({ ...c, [era.id]: now + ERA_COOLDOWN_MS }));
  };

  return (
    <div
      className="fixed left-6 top-1/2 -translate-y-1/2 z-40 flex flex-col gap-3"
      data-testid="era-buttons"
    >
      <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40 pl-1 mb-1">
        Era Jump
      </div>
      {ERAS.map((era) => {
        const now = Date.now();
        const exp = cooldowns[era.id] || 0;
        const remaining = Math.max(0, exp - now);
        const disabled = remaining > 0;
        const progress = disabled ? 1 - remaining / ERA_COOLDOWN_MS : 1;
        const secs = Math.ceil(remaining / 1000);

        return (
          <button
            key={era.id}
            onClick={() => handleClick(era)}
            disabled={disabled}
            data-testid={`era-button-${era.id}`}
            className={`group relative w-40 pl-4 pr-3 py-2.5 rounded-full glass flex items-center gap-3
              ${disabled ? 'opacity-60 cursor-not-allowed' : 'hover:border-[#D4AF37]/50'}
              transition-colors duration-200`}
            aria-label={`Jump to ${era.name}`}
          >
            <span className="relative w-6 h-6 flex items-center justify-center">
              <svg width="24" height="24" viewBox="0 0 24 24" className="rotate-[-90deg]">
                <circle cx="12" cy="12" r="10" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1.5" />
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  fill="none"
                  stroke="#D4AF37"
                  strokeWidth="1.5"
                  strokeDasharray={`${2 * Math.PI * 10}`}
                  strokeDashoffset={`${2 * Math.PI * 10 * (1 - progress)}`}
                  strokeLinecap="round"
                  style={{ transition: 'stroke-dashoffset 0.4s linear' }}
                />
              </svg>
              <span className="absolute w-1.5 h-1.5 rounded-full gold-text bg-current" />
            </span>
            <span className="flex-1 text-left font-serif-h text-sm text-white/90">{era.name}</span>
            {disabled && (
              <span className="font-mono-x text-[10px] text-white/40">{secs}s</span>
            )}
          </button>
        );
      })}
    </div>
  );
}
