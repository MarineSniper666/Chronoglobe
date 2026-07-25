export const CATEGORIES = {
  civilizations: { label: 'Civilizations', color: '#D4AF37', markerClass: 'marker-civ', dot: 'dot-civ' },
  land: { label: 'Land Transformations', color: '#6B8E23', markerClass: 'marker-land', dot: 'dot-land' },
  pandemics: { label: 'Pandemics', color: '#8B0000', markerClass: 'marker-pan', dot: 'dot-pan' },
  technology: { label: 'Technology', color: '#4682B4', markerClass: 'marker-tech', dot: 'dot-tech' },
};

// Macro eras (top-level jumps)
export const ERAS = [
  { id: 'prehistoric', name: 'Prehistoric', jumpTo: -25000, range: [-500000, -3500] },
  { id: 'ancient', name: 'Ancient', jumpTo: -3000, range: [-3500, -500] },
  { id: 'classical', name: 'Classical', jumpTo: -300, range: [-500, 500] },
  { id: 'medieval', name: 'Medieval', jumpTo: 900, range: [500, 1500] },
  { id: 'early-modern', name: 'Early Modern', jumpTo: 1600, range: [1500, 1800] },
  { id: 'modern', name: 'Modern', jumpTo: 1900, range: [1800, 2026] },
];

// Sub-periods within each macro era. `parent` points to the ERAS id.
export const SUB_PERIODS = [
  // Prehistoric
  { id: 'sp-upper-paleo', name: 'Upper Paleolithic', jumpTo: -25000, start: -40000, end: -10000, parent: 'prehistoric', showTick: false },
  { id: 'sp-mesolithic', name: 'Mesolithic', jumpTo: -9000, start: -10000, end: -7000, parent: 'prehistoric', showTick: true },
  { id: 'sp-neolithic', name: 'Neolithic', jumpTo: -6500, start: -8000, end: -3500, parent: 'prehistoric', showTick: true },
  // Ancient
  { id: 'sp-early-bronze', name: 'Early Bronze Age', jumpTo: -3200, start: -3300, end: -2100, parent: 'ancient', showTick: true },
  { id: 'sp-middle-bronze', name: 'Middle Bronze Age', jumpTo: -1900, start: -2100, end: -1550, parent: 'ancient', showTick: false },
  { id: 'sp-late-bronze', name: 'Late Bronze Age', jumpTo: -1400, start: -1550, end: -1200, parent: 'ancient', showTick: false },
  { id: 'sp-iron-age', name: 'Iron Age', jumpTo: -1100, start: -1200, end: -550, parent: 'ancient', showTick: true },
  // Classical
  { id: 'sp-classical-antiquity', name: 'Classical Antiquity', jumpTo: -450, start: -800, end: -300, parent: 'classical', showTick: true },
  { id: 'sp-hellenistic', name: 'Hellenistic Age', jumpTo: -300, start: -323, end: -30, parent: 'classical', showTick: false },
  { id: 'sp-roman-peace', name: 'Pax Romana', jumpTo: 100, start: -27, end: 180, parent: 'classical', showTick: false },
  { id: 'sp-late-antiquity', name: 'Late Antiquity', jumpTo: 350, start: 180, end: 500, parent: 'classical', showTick: false },
  // Medieval
  { id: 'sp-early-middle', name: 'Early Middle Ages', jumpTo: 700, start: 500, end: 1000, parent: 'medieval', showTick: false },
  { id: 'sp-high-middle', name: 'High Middle Ages', jumpTo: 1150, start: 1000, end: 1300, parent: 'medieval', showTick: false },
  { id: 'sp-late-middle', name: 'Late Middle Ages', jumpTo: 1400, start: 1300, end: 1500, parent: 'medieval', showTick: false },
  // Early Modern
  { id: 'sp-renaissance', name: 'Renaissance', jumpTo: 1500, start: 1400, end: 1600, parent: 'early-modern', showTick: true },
  { id: 'sp-discovery', name: 'Age of Discovery', jumpTo: 1550, start: 1400, end: 1700, parent: 'early-modern', showTick: false },
  { id: 'sp-scientific', name: 'Scientific Revolution', jumpTo: 1620, start: 1543, end: 1687, parent: 'early-modern', showTick: false },
  { id: 'sp-enlightenment', name: 'Enlightenment', jumpTo: 1750, start: 1685, end: 1815, parent: 'early-modern', showTick: false },
  // Modern
  { id: 'sp-industrial', name: 'Industrial Revolution', jumpTo: 1800, start: 1760, end: 1840, parent: 'modern', showTick: true },
  { id: 'sp-victorian', name: 'Victorian Era', jumpTo: 1870, start: 1837, end: 1901, parent: 'modern', showTick: false },
  { id: 'sp-world-wars', name: 'World Wars Era', jumpTo: 1918, start: 1914, end: 1945, parent: 'modern', showTick: false },
  { id: 'sp-space-age', name: 'Space Age', jumpTo: 1965, start: 1957, end: 1991, parent: 'modern', showTick: true },
  { id: 'sp-digital', name: 'Digital Age', jumpTo: 1990, start: 1980, end: 2000, parent: 'modern', showTick: false },
  { id: 'sp-information', name: 'Information Age', jumpTo: 2015, start: 2000, end: 2026, parent: 'modern', showTick: true },
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

// Return the sub-period that best matches the given year (narrowest match wins).
export const getSubPeriod = (year) => {
  const candidates = SUB_PERIODS.filter((sp) => year >= sp.start && year <= sp.end);
  if (!candidates.length) return null;
  candidates.sort((a, b) => (a.end - a.start) - (b.end - b.start));
  return candidates[0];
};

export const getSubPeriodsFor = (eraId) =>
  SUB_PERIODS.filter((sp) => sp.parent === eraId);

// Tick marks worth showing on the timeline scrubber
export const TIMELINE_TICKS = SUB_PERIODS.filter((sp) => sp.showTick);
