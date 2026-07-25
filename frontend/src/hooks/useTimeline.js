import { useState, useEffect, useRef, useCallback } from 'react';
import { TIMELINE_START, TIMELINE_END, SPEEDS } from '../lib/history';

/**
 * Timeline hook: manages currentYear, playing state, and speed.
 * Advances year at speed.yps per real second.
 */
export function useTimeline() {
  const [year, setYear] = useState(TIMELINE_START);
  const [playing, setPlaying] = useState(true);
  const [speedIdx, setSpeedIdx] = useState(1);
  const rafRef = useRef(null);
  const lastTs = useRef(null);

  const speed = SPEEDS[speedIdx];

  useEffect(() => {
    if (!playing) {
      cancelAnimationFrame(rafRef.current);
      lastTs.current = null;
      return;
    }
    const tick = (ts) => {
      if (lastTs.current == null) lastTs.current = ts;
      const dt = (ts - lastTs.current) / 1000;
      lastTs.current = ts;
      setYear((y) => {
        const next = y + speed.yps * dt;
        if (next >= TIMELINE_END) {
          setPlaying(false);
          return TIMELINE_END;
        }
        return next;
      });
      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [playing, speed.yps]);

  const jumpTo = useCallback((y) => {
    setYear(Math.max(TIMELINE_START, Math.min(TIMELINE_END, y)));
  }, []);

  const togglePlay = useCallback(() => {
    if (year >= TIMELINE_END) {
      setYear(TIMELINE_START);
      setPlaying(true);
    } else {
      setPlaying((p) => !p);
    }
  }, [year]);

  const cycleSpeed = useCallback(() => {
    setSpeedIdx((i) => (i + 1) % SPEEDS.length);
  }, []);

  const pause = useCallback(() => setPlaying(false), []);

  return { year, setYear: jumpTo, playing, togglePlay, speedIdx, speed, cycleSpeed, pause };
}
