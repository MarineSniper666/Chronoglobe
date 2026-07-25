export const CATEGORIES = {
  civilizations: { label: 'Civilizations', color: '#D4AF37', markerClass: 'marker-civ', dot: 'dot-civ' },
  land: { label: 'Land Transformations', color: '#6B8E23', markerClass: 'marker-land', dot: 'dot-land' },
  pandemics: { label: 'Pandemics', color: '#8B0000', markerClass: 'marker-pan', dot: 'dot-pan' },
  technology: { label: 'Technology', color: '#4682B4', markerClass: 'marker-tech', dot: 'dot-tech' },
};

export const ERAS = [
  { id: 'prehistoric', name: 'Prehistoric', jumpTo: -25000, range: [-500000, -3500] },
  { id: 'ancient', name: 'Ancient', jumpTo: -3000, range: [-3500, -500] },
  { id: 'classical', name: 'Classical', jumpTo: -300, range: [-500, 500] },
  { id: 'medieval', name: 'Medieval', jumpTo: 900, range: [500, 1500] },
  { id: 'early-modern', name: 'Early Modern', jumpTo: 1600, range: [1500, 1800] },
  { id: 'modern', name: 'Modern', jumpTo: 1900, range: [1800, 2026] },
];

// Timeline bounds
export const TIMELINE_START = -25000;
export const TIMELINE_END = 2026;

// Playback speeds (years advanced per real second)
export const SPEEDS = [
  { label: '1x', yps: 25 },
  { label: '2x', yps: 100 },
  { label: '5x', yps: 500 },
  { label: '10x', yps: 2500 },
];

export const ERA_COOLDOWN_MS = 150 * 1000; // 2.5 minutes

export const formatYear = (y) => {
  const n = Math.round(y);
  if (n < 0) return `${Math.abs(n).toLocaleString()} BCE`;
  return `${n.toLocaleString()} CE`;
};

export const getEraName = (year) => {
  for (const e of ERAS) {
    if (year >= e.range[0] && year <= e.range[1]) return e.name;
  }
  return year < -3500 ? 'Prehistoric' : 'Modern';
};
