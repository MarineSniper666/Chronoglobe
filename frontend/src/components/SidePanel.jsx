import { useEffect, useRef, useState } from 'react';
import { X, Sparkles, MapPin, Volume2, Pause, Loader2 } from 'lucide-react';
import { CATEGORIES, formatYear } from '../lib/history';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function SidePanel({ event, onClose }) {
  const [aiText, setAiText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [audioPlaying, setAudioPlaying] = useState(false);
  const abortRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    if (!event) return;
    setAiText('');
    setError(null);
    setLoading(true);
    // Reset audio when event changes
    if (audioRef.current) { audioRef.current.pause(); audioRef.current = null; }
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    setAudioPlaying(false);
    setAudioLoading(false);

    const controller = new AbortController();
    abortRef.current = controller;

    (async () => {
      try {
        const res = await fetch(`${API}/expand`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ event_id: event.id }),
          signal: controller.signal,
        });
        if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const parts = buffer.split('\n\n');
          buffer = parts.pop() || '';
          for (const part of parts) {
            if (!part.startsWith('data: ')) continue;
            const payload = part.slice(6);
            if (payload === '[DONE]') { setLoading(false); return; }
            if (payload.startsWith('[ERROR]')) {
              setError(payload.replace('[ERROR] ', ''));
              setLoading(false);
              return;
            }
            setAiText((t) => t + payload);
          }
        }
      } catch (e) {
        if (e.name !== 'AbortError') setError(e.message);
      } finally {
        setLoading(false);
      }
    })();

    return () => controller.abort();
  }, [event]);

  if (!event) return null;
  const cat = CATEGORIES[event.category];

  return (
    <aside
      className="fixed top-0 right-0 h-full w-full sm:w-[440px] z-50 glass-panel flex flex-col animate-[slidein_0.35s_ease-out]"
      data-testid="side-panel"
      style={{ animation: 'slidein 0.35s ease-out' }}
    >
      <style>{`@keyframes slidein { from { transform: translateX(100%);} to { transform: translateX(0);} }`}</style>

      <div className="relative overflow-hidden">
        <div
          className="h-40 relative"
          style={{
            background: `linear-gradient(135deg, ${cat.color}22 0%, transparent 70%), url('https://images.pexels.com/photos/9494906/pexels-photo-9494906.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940') center/cover`,
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-b from-[#0A0A0C]/40 via-[#0A0A0C]/70 to-[#0A0A0C]" />
        </div>
        <button
          onClick={onClose}
          data-testid="close-panel"
          className="absolute top-4 right-4 w-9 h-9 rounded-full glass flex items-center justify-center hover:border-white/30 transition-colors duration-200"
          aria-label="Close panel"
        >
          <X size={15} className="text-white/80" />
        </button>

        <div className="absolute bottom-5 left-6 right-6">
          <div className="flex items-center gap-2 mb-2">
            <span className={`inline-block w-2 h-2 rounded-full ${cat.dot}`} />
            <span className="font-mono-x text-[10px] uppercase tracking-[0.25em] text-white/60">
              {cat.label}
            </span>
          </div>
          <div className="font-mono-x text-[11px] text-white/70">
            {formatYear(event.year)}
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto scroll-thin px-6 py-6">
        <h2 className="font-serif-h text-3xl leading-tight text-white mb-3">{event.title}</h2>

        <div className="flex items-center gap-2 text-white/50 font-mono-x text-[11px] mb-5">
          <MapPin size={11} />
          <span>{event.region}</span>
          <span className="text-white/25">·</span>
          <span>{event.lat.toFixed(2)}°, {event.lng.toFixed(2)}°</span>
        </div>

        <p className="text-white/80 leading-relaxed mb-6">{event.summary}</p>

        <div className="flex items-center justify-between mb-3 pt-3 border-t border-white/5">
          <div className="flex items-center gap-2">
            <Sparkles size={13} className="gold-text" />
            <span className="font-mono-x text-[10px] uppercase tracking-[0.25em] gold-text">
              Historian&apos;s Deep Dive
            </span>
          </div>
          <button
            onClick={handleListen}
            disabled={!aiText || loading || audioLoading}
            data-testid="listen-button"
            className="flex items-center gap-2 px-3 h-7 rounded-full gold-border border text-[10px] font-mono-x uppercase tracking-[0.2em] gold-text hover:bg-[#D4AF37]/10 disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-200"
            aria-label="Listen to narration"
          >
            {audioLoading ? <Loader2 size={11} className="animate-spin" /> :
              audioPlaying ? <Pause size={11} /> : <Volume2 size={11} />}
            {audioPlaying ? 'Pause' : 'Listen'}
          </button>
        </div>

        {error && (
          <div className="text-[#8B0000] text-sm font-mono-x" data-testid="ai-error">
            Unable to load: {error}
          </div>
        )}
        <div
          data-testid="ai-content"
          className="text-white/85 leading-relaxed whitespace-pre-wrap text-[15px]"
        >
          {aiText}
          {loading && <span className="inline-block w-2 h-4 ml-1 bg-[#D4AF37] animate-pulse align-middle" />}
        </div>

        <div className="mt-8 pt-4 border-t border-white/5">
          <div className="font-mono-x text-[10px] uppercase tracking-[0.25em] text-white/40 mb-1">
            Source
          </div>
          <div className="text-white/60 text-sm">{event.source}</div>
        </div>
      </div>
    </aside>
  );
}
