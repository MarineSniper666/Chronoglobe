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
import BookmarksDrawer from '@/components/BookmarksDrawer';
import StoryMenu from '@/components/StoryMenu';
import StoryRibbon from '@/components/StoryRibbon';
import { listBookmarks } from '@/lib/bookmarks';
import { useTimeline } from '@/hooks/useTimeline';
import { useStoryMode } from '@/hooks/useStoryMode';
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
  const [bookmarksOpen, setBookmarksOpen] = useState(false);
  const [bookmarkTick, setBookmarkTick] = useState(0);
  const [bookmarkCount, setBookmarkCount] = useState(0);
  const [bookmarks, setBookmarks] = useState([]);
  const [tours, setTours] = useState([]);
  const [storyMenuOpen, setStoryMenuOpen] = useState(false);
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
    axios.get(`${API}/tours`).then((r) => setTours(r.data.tours || [])).catch(() => {});
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

  useEffect(() => {
    const list = listBookmarks();
    setBookmarkCount(list.length);
    setBookmarks(list);
  }, [bookmarkTick]);

  const handleRandomEvent = () => {
    if (!events.length) return;
    const e = events[Math.floor(Math.random() * events.length)];
    setYear(Math.max(e.year, TIMELINE_START));
    setSelected(e);
    setFocus(e);
  };

  // Story Mode driver
  const story = useStoryMode({
    events,
    onOpenEvent: (e) => { setSelected(e); setFocus(e); },
    onSetYear: (y) => setYear(Math.max(y, TIMELINE_START)),
    onPauseTimeline: pause,
  });

  const handleShare = async () => {
    try {
      // Prefer the /api/share URL so social crawlers get the OG card;
      // when clicked in a normal browser it redirects to the app URL.
      const url = selected
        ? `${window.location.origin}/api/share?event=${selected.id}&year=${Math.round(year)}`
        : window.location.href;
      await navigator.clipboard.writeText(url);
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
        onOpenBookmarks={() => setBookmarksOpen(true)}
        bookmarkCount={bookmarkCount}
        onOpenTours={() => setStoryMenuOpen(true)}
        onRandomEvent={handleRandomEvent}
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
        bookmarks={bookmarks}
        onPickBookmark={(eventId) => {
          const e = events.find((x) => x.id === eventId);
          if (!e) return;
          setYear(Math.max(e.year, TIMELINE_START));
          setSelected(e);
          setFocus(e);
        }}
      />

      {selected && events.length > 0 && (
        <SidePanel
          event={selected}
          allEvents={events}
          onClose={() => { setSelected(null); if (story.active) story.exitTour(); }}
          onOpenRelated={handleOpenRelated}
          currentYear={year}
          onBookmarkChange={() => setBookmarkTick((t) => t + 1)}
          autoPlayAudio={!!story.active && !story.paused}
          onAudioEnded={story.onAudioEnded}
        />
      )}

      <StoryMenu
        open={storyMenuOpen}
        tours={tours}
        onClose={() => setStoryMenuOpen(false)}
        onStart={(t) => { setStoryMenuOpen(false); story.startTour(t); }}
      />

      <StoryRibbon
        tour={story.active}
        stopIndex={story.stopIndex}
        total={story.total}
        paused={story.paused}
        isLast={story.isLast}
        complete={story.complete}
        onPause={story.pauseTour}
        onResume={story.resumeTour}
        onNext={story.nextStop}
        onPrev={story.prevStop}
        onExit={() => { story.exitTour(); }}
      />

      <BookmarksDrawer
        open={bookmarksOpen}
        onClose={() => setBookmarksOpen(false)}
        onPick={(eventId) => {
          const e = events.find((x) => x.id === eventId);
          if (!e) return;
          setYear(Math.max(e.year, TIMELINE_START));
          setSelected(e);
          setFocus(e);
          setBookmarksOpen(false);
        }}
        refreshTick={bookmarkTick}
      />

      <div className="fixed bottom-2 left-4 z-40 pointer-events-none select-none">
        <span className="font-serif-h italic text-white/25 text-[11px] tracking-wide">
          Created by Ace Ruben Masters — 2026
        </span>
      </div>
    </div>
  );
}

export default App;
