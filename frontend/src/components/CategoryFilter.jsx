import { useState } from 'react';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { CATEGORIES, CATEGORY_SUBTYPES, SUBTYPE_ACCENT } from '../lib/history';

export default function CategoryFilter({ active, onToggle, onToggleSubtype }) {
  // Independent expand/collapse state per category, since more than one
  // category (Technology, Civilizations, ...) can have a sub-filter list.
  const [expanded, setExpanded] = useState({});

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
          const subtypes = CATEGORY_SUBTYPES[key];
          const hasSubtypes = !!subtypes && Object.keys(subtypes).length > 0;
          const isExpanded = !!expanded[key];
          const accent = SUBTYPE_ACCENT[key] || cat.color;
          return (
            <div key={key}>
              <button
                onClick={() => onToggle(key)}
                data-testid={`filter-${key}`}
                className={`w-full flex items-center gap-3 px-2 py-2 rounded-lg border transition-colors duration-200
                  ${isOn ? 'border-white/15 bg-white/5' : 'border-transparent opacity-50 hover:opacity-80'}`}
              >
                <span className={`w-2.5 h-2.5 rounded-full ${cat.dot}`} />
                <span className="font-serif-h text-[15px] text-white/90 flex-1 text-left">
                  {cat.label}
                </span>
                {hasSubtypes && (
                  <span
                    role="button"
                    tabIndex={0}
                    onClick={(e) => { e.stopPropagation(); setExpanded((v) => ({ ...v, [key]: !v[key] })); }}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') { e.stopPropagation(); setExpanded((v) => ({ ...v, [key]: !v[key] })); }
                    }}
                    aria-label={isExpanded ? `Collapse ${cat.label} subtypes` : `Expand ${cat.label} subtypes`}
                    data-testid={`filter-${key}-expand`}
                    className="text-white/40 hover:text-white/80 p-0.5 -mr-1"
                  >
                    {isExpanded ? <ChevronDown size={13} /> : <ChevronRight size={13} />}
                  </span>
                )}
              </button>

              {hasSubtypes && isExpanded && (
                <div className="ml-5 mt-1 mb-1 flex flex-col gap-0.5 border-l border-white/10 pl-3">
                  {Object.entries(subtypes).map(([subKey, subLabel]) => {
                    const categorySubs = active.subtypesByCategory?.[key];
                    const subOn = categorySubs ? categorySubs[subKey] !== false : true;
                    return (
                      <button
                        key={subKey}
                        onClick={() => onToggleSubtype(key, subKey)}
                        data-testid={`filter-${key}-${subKey}`}
                        className={`flex items-center gap-2 px-2 py-1 rounded-md transition-colors duration-200 hover:bg-white/5
                          ${subOn ? 'text-white/70' : 'text-white/30'}`}
                      >
                        <span
                          className="w-1.5 h-1.5 rounded-full"
                          style={{ backgroundColor: subOn ? accent : 'rgba(255,255,255,0.15)' }}
                        />
                        <span className={`font-mono-x text-[10px] uppercase tracking-[0.1em] text-left flex-1 ${subOn ? '' : 'line-through'}`}>
                          {subLabel}
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
