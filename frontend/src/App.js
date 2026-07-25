import { useEffect, useMemo, useState, useCallback, useRef, Suspense, lazy } from 'react';
import axios from 'axios';
import '@/App.css';

import Header from '@/components/Header';
import TimelineBar from '@/components/TimelineBar';
import EraButtons from '@/components/EraButtons';
import CategoryFilter from '@/components/CategoryFilter';
import SidePanel from '@/components/SidePanel';
import Map2D from '@/components/Map2D';
import SearchBox from '@/components/SearchBox';
import CompareScrubber from '@/components/CompareScrubber';
import { useTimeline } from '@/hooks/useTimeline';
import { TIMELINE_START, TIMELINE_END } from '@/lib/history';

const Globe3D = lazy(() => import('@/components/Globe3D'));

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

function App() {
  const [events, setEvents] = useState([]);
  const [arcs, setArcs] = useState([]);
  const [empires, setEmpires] = useState([]);
  const [mode, setMode] = useState('3d');
  const [compareOn, setCompareOn] = useState(false);
  const [yearB, setYearB] = useState(1900);
  const [selected, setSelected] = useState(null);
  const [focus, setFocus] = useState(null);
  const [filters, setFilters] = useState({
    civilizations: true,
    land: true,
    pandemics: true,
    technology: true,
  });

  const { year, setYear, playing, togglePlay, speed, cycleSpeed, pause } = useTimeline();
  const urlParsedRef = useRef(false);
  const initialUrlRef = useRef(window.location.search);

  // Load data
  useEffect(() => {
    axios.get(`${API}/events`).then((r) => setEvents(r.data.events || [])).catch(() => {});
    axios.get(`${API}/arcs`).then((r) => setArcs(r.data.arcs || [])).catch(() => {});
    axios.get(`${API}/empires`).then((r) => setEmpires(r.data.empires || [])).catch(() => {});
  }, []);

  // Parse URL on load: ?year=1347&event=pan-blackdeath&compare=1900
  useEffect(() => {
    if (!events.length || urlParsedRef.current) return;
    const p = new URLSearchParams(initialUrlRef.current);
    const y = p.get('year');
    const ev = p.get('event');
    const cmp = p.get('compare');
    if (y != null && !Number.isNaN(Number(y))) {
      setYear(Number(y));
      pause(); // pause at the shared moment
    }
    if (cmp != null && !Number.isNaN(Number(cmp))) {
      setYearB(Number(cmp));
      setCompareOn(true);
    }
    if (ev) {
      const e = events.find((x) => x.id === ev);
      if (e) { setSelected(e); setFocus(e); }
    }
    urlParsedRef.current = true;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [events.length]);

  // Write URL when meaningful state changes (only after initial parse)
  useEffect(() => {
    if (!urlParsedRef.current) return;
    const p = new URLSearchParams();
    p.set('year', String(Math.round(year)));
    if (compareOn) p.set('compare', String(Math.round(yearB)));
    if (selected) p.set('event', selected.id);
    window.history.replaceState(null, '', `${window.location.pathname}?${p.toString()}`);
  }, [year, yearB, compareOn, selected]);

  const filterFn = useCallback(
    (e, y) => e.year <= y && filters[e.category],
    [filters]
  );

  const visibleEventsA = useMemo(
    () => events.filter((e) => filterFn(e, year)),
    [events, year, filterFn]
  );

  const visibleEventsB = useMemo(
    () => events.filter((e) => filterFn(e, yearB)),
    [events, yearB, filterFn]
  );

  const handleSelect = (e) => { setSelected(e); setFocus(e); };

  const handleSearchPick = (e) => {
    setYear(Math.max(e.year, TIMELINE_START));
    setSelected(e);
    setFocus(e);
  };

  const handleOpenRelated = (relatedId) => {
    const e = events.find((x) => x.id === relatedId);
    if (!e) return;
    setYear(Math.max(e.year, TIMELINE_START));
    setSelected(e);
    setFocus(e);
  };

  const handleJump = (targetYear) => setYear(targetYear);
  const toggleFilter = (key) => setFilters((f) => ({ ...f, [key]: !f[key] }));
  const onReset = () => setYear(TIMELINE_START);
  const toggleCompare = () => setCompareOn((v) => !v);

  const autoRotate = playing && !selected && !compareOn;

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
    } catch (e) { /* ignore */ }
  };

  return (
    <div className="App starfield" data-testid="app-root">
      {mode === '3d' ? (
        <Suspense fallback={<div className="absolute inset-0 flex items-center justify-center text-white/40 font-mono-x text-xs">Loading globe…</div>}>
          {compareOn ? (
            <div className="absolute inset-0 flex" data-testid="compare-view">
              <div className="relative flex-1 border-r border-white/10">
                <Globe3D
                  visibleEvents={visibleEventsA}
                  arcs={arcs}
                  empires={empires}
                  year={year}
                  onSelect={handleSelect}
                  focusEvent={focus}
                  autoRotate={false}
                />
                <div className="absolute top-24 left-4 glass rounded-full px-3 py-1.5 font-mono-x text-[10px] gold-text pointer-events-none">
                  A · {Math.round(year)}
                </div>
              </div>
              <div className="relative flex-1">
                <Globe3D
                  visibleEvents={visibleEventsB}
                  arcs={arcs}
                  empires={empires}
                  year={yearB}
                  onSelect={handleSelect}
                  focusEvent={null}
                  autoRotate={false}
                />
                <div className="absolute top-24 right-4 glass rounded-full px-3 py-1.5 font-mono-x text-[10px] gold-text pointer-events-none">
                  B · {Math.round(yearB)}
                </div>
              </div>
            </div>
          ) : (
            <Globe3D
              visibleEvents={visibleEventsA}
              arcs={arcs}
              empires={empires}
              year={year}
              onSelect={handleSelect}
              focusEvent={focus}
              autoRotate={autoRotate}
            />
          )}
        </Suspense>
      ) : (
        <Map2D visibleEvents={visibleEventsA} onSelect={handleSelect} />
      )}

      <Header
        mode={mode}
        setMode={setMode}
        year={year}
        visibleCount={visibleEventsA.length}
        compareOn={compareOn}
        toggleCompare={toggleCompare}
        onShare={handleShare}
      />
      <SearchBox events={events} onPick={handleSearchPick} />
      <EraButtons onJump={handleJump} />
      <CategoryFilter active={filters} onToggle={toggleFilter} />

      {compareOn && (
        <CompareScrubber
          yearB={yearB}
          setYearB={setYearB}
          min={TIMELINE_START}
          max={TIMELINE_END}
        />
      )}

      <TimelineBar
        year={year}
        setYear={setYear}
        playing={playing}
        togglePlay={togglePlay}
        speed={speed}
        cycleSpeed={cycleSpeed}
        onReset={onReset}
      />

      {selected && events.length > 0 && (
        <SidePanel
          event={selected}
          allEvents={events}
          onClose={() => setSelected(null)}
          onOpenRelated={handleOpenRelated}
        />
      )}
    </div>
  );
}

export default App;
