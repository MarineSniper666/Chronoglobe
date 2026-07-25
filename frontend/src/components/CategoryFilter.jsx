import { CATEGORIES } from '../lib/history';

export default function CategoryFilter({ active, onToggle }) {
  return (
    <div
      className="fixed right-6 top-24 z-40 glass rounded-2xl p-4 w-56"
      data-testid="category-filter"
    >
      <div className="font-mono-x text-[9px] uppercase tracking-[0.25em] text-white/40 mb-3">
        Layers
      </div>
      <div className="flex flex-col gap-2">
        {Object.entries(CATEGORIES).map(([key, cat]) => {
          const isOn = active[key];
          return (
            <button
              key={key}
              onClick={() => onToggle(key)}
              data-testid={`filter-${key}`}
              className={`flex items-center gap-3 px-2 py-2 rounded-lg border transition-colors duration-200
                ${isOn ? 'border-white/15 bg-white/5' : 'border-transparent opacity-50 hover:opacity-80'}`}
            >
              <span className={`w-2.5 h-2.5 rounded-full ${cat.dot}`} />
              <span className="font-serif-h text-[15px] text-white/90 flex-1 text-left">
                {cat.label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
