import { useEffect, useMemo, useState, Suspense, lazy } from 'react';
import axios from 'axios';
import '@/App.css';

import Header from '@/components/Header';
import TimelineBar from '@/components/TimelineBar';
import EraButtons from '@/components/EraButtons';
import CategoryFilter from '@/components/CategoryFilter';
import SidePanel from '@/components/SidePanel';
import Map2D from '@/components/Map2D';
import SearchBox from '@/components/SearchBox';
import { useTimeline } from '@/hooks/useTimeline';
import { TIMELINE_START } from '@/lib/history';

const Globe3D = lazy(() => import('@/components/Globe3D'));

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

function App() {
  const [events, setEvents] = useState([]);
  const [arcs, setArcs] = useState([]);
  const [empires, setEmpires] = useState([]);
  const [mode, setMode] = useState('3d');
  const [selected, setSelected] = useState(null);
  const [focus, setFocus] = useState(null);
  const [filters, setFilters] = useState({
    civilizations: true,
    land: true,
    pandemics: true,
    technology: true,
  });

  const { year, setYear, playing, togglePlay, speed, cycleSpeed, pause } = useTimeline();

  useEffect(() => {
    axios.get(`${API}/events`).then((r) => setEvents(r.data.events || [])).catch(() => {});
    axios.get(`${API}/arcs`).then((r) => setArcs(r.data.arcs || [])).catch(() => {});
    axios.get(`${API}/empires`).then((r) => setEmpires(r.data.empires || [])).catch(() => {});
  }, []);

  const visibleEvents = useMemo(
    () => events.filter((e) => e.year <= year && filters[e.category]),
    [events, year, filters]
  );

  const handleSelect = (e) => { setSelected(e); setFocus(e); pause(); };

  const handleSearchPick = (e) => {
    // Jump timeline to the event year, focus camera, open panel, pause playback
    setYear(Math.max(e.year, TIMELINE_START));
    setSelected(e);
    setFocus(e);
    pause();
  };

  const handleRelated = (relatedId) => {
    const target = events.find((ev) => ev.id === relatedId);
    if (!target) return;
    setYear(Math.max(target.year, TIMELINE_START));
    setSelected(target);
    setFocus(target);
  };

  const handleJump = (targetYear) => setYear(targetYear);
  const toggleFilter = (key) => setFilters((f) => ({ ...f, [key]: !f[key] }));
  const onReset = () => setYear(TIMELINE_START);

  const autoRotate = playing && !selected;

  return (
    <div className="App starfield" data-testid="app-root">
      {mode === '3d' ? (
        <Suspense fallback={<div className="absolute inset-0 flex items-center justify-center text-white/40 font-mono-x text-xs">Loading globe…</div>}>
          <Globe3D
            visibleEvents={visibleEvents}
            arcs={arcs}
            empires={empires}
            year={year}
            onSelect={handleSelect}
            focusEvent={focus}
            autoRotate={autoRotate}
          />
        </Suspense>
      ) : (
        <Map2D visibleEvents={visibleEvents} onSelect={handleSelect} />
      )}

      <Header mode={mode} setMode={setMode} year={year} visibleCount={visibleEvents.length} />
      <SearchBox events={events} onPick={handleSearchPick} />
      <EraButtons onJump={handleJump} />
      <CategoryFilter active={filters} onToggle={toggleFilter} />
      <TimelineBar
        year={year}
        setYear={setYear}
        playing={playing}
        togglePlay={togglePlay}
        speed={speed}
        cycleSpeed={cycleSpeed}
        onReset={onReset}
      />

      {selected && <SidePanel event={selected} allEvents={events} onClose={() => setSelected(null)} onOpenRelated={handleRelated} />}
    </div>
  );
}

export default App;
