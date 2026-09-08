import { useEffect, useState, useRef, useCallback } from 'react';

/**
 * Story Mode driver. Given a tour {id, title, stops:[event_id...]}, it
 * exposes:
 *   - active: the tour or null
 *   - stopIndex: current position in tour.stops
 *   - paused: user paused narration
 *   - currentEventId: the event that should be open right now
 *   - startTour(tour): begin
 *   - pauseTour() / resumeTour()
 *   - nextStop() / prevStop() / exitTour()
 *   - onAudioEnded(): called by the SidePanel when TTS finishes → advance
 */
export function useStoryMode({ events, onOpenEvent, onSetYear, onPauseTimeline }) {
  const [active, setActive] = useState(null);
  const [stopIndex, setStopIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  const activeRef = useRef(null);

  useEffect(() => { activeRef.current = active; }, [active]);

  const openStop = useCallback((tour, idx) => {
    const evId = tour.stops[idx];
    const ev = events.find((e) => e.id === evId);
    if (!ev) return;
    onPauseTimeline && onPauseTimeline();
    onSetYear(ev.year);
    onOpenEvent(ev);
  }, [events, onOpenEvent, onSetYear, onPauseTimeline]);

  const startTour = useCallback((tour) => {
    if (!tour || !tour.stops?.length) return;
    setActive(tour);
    setStopIndex(0);
    setPaused(false);
    openStop(tour, 0);
  }, [openStop]);

  const nextStop = useCallback(() => {
    const t = activeRef.current;
    if (!t) return;
    setStopIndex((i) => {
      const next = i + 1;
      if (next >= t.stops.length) {
        // Tour complete — leave panel open on the last stop and mark done.
        return i;
      }
      openStop(t, next);
      return next;
    });
  }, [openStop]);

  const prevStop = useCallback(() => {
    const t = activeRef.current;
    if (!t) return;
    setStopIndex((i) => {
      const p = Math.max(0, i - 1);
      openStop(t, p);
      return p;
    });
  }, [openStop]);

  const pauseTour = useCallback(() => setPaused(true), []);
  const resumeTour = useCallback(() => setPaused(false), []);
  const exitTour = useCallback(() => {
    setActive(null);
    setStopIndex(0);
    setPaused(false);
  }, []);

  const onAudioEnded = useCallback(() => {
    if (!activeRef.current) return;
    if (paused) return;
    nextStop();
  }, [paused, nextStop]);

  const currentEventId = active ? active.stops[stopIndex] : null;
  const total = active ? active.stops.length : 0;
  const isLast = active ? stopIndex >= total - 1 : false;

  return {
    active, stopIndex, total, isLast, paused, currentEventId,
    startTour, nextStop, prevStop, pauseTour, resumeTour, exitTour,
    onAudioEnded,
  };
}
