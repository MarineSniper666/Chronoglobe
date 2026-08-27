import { useEffect, useRef, useState } from 'react';
import { X, Sparkles, MapPin, Volume2, Pause, Loader2, Users, GitBranch, Star } from 'lucide-react';
import { CATEGORIES, formatYear } from '../lib/history';
import { isBookmarked, addBookmark, removeBookmark } from '../lib/bookmarks';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function SidePanel({ event, allEvents = [], onClose, onOpenRelated, currentYear, onBookmarkChange }) {
  const [aiText, setAiText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [audioPlaying, setAudioPlaying] = useState(false);
  const [voice, setVoice] = useState('onyx'); // 'onyx' = male, 'sage' = female
  const [bookmarked, setBookmarked] = useState(false);
  const abortRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    if (event) setBookmarked(isBookmarked(event.id));
  }, [event]);

  const toggleBookmark = () => {
    if (!event) return;
    if (bookmarked) {
      removeBookmark(event.id);
      setBookmarked(false);
    } else {
      addBookmark(event, currentYear ?? event.year);
      setBookmarked(true);
    }
    onBookmarkChange && onBookmarkChange();
  };

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

  const handleListen = async () => {
    if (!aiText || loading) return;
    if (audioRef.current) {
      if (audioPlaying) { audioRef.current.pause(); setAudioPlaying(false); }
      else { audioRef.current.play(); setAudioPlaying(true); }
      return;
    }
    setAudioLoading(true);
    try {
      const cleanText = aiText.replace(/\*\*/g, '').replace(/[#*_`]/g, '');
      const res = await fetch(`${API}/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: cleanText, voice }),
      });
      if (!res.ok) throw new Error(`TTS HTTP ${res.status}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
      const audio = new Audio(url);
      audio.onended = () => setAudioPlaying(false);
      audioRef.current = audio;
      audio.play();
      setAudioPlaying(true);
    } catch (e) {
      setError(`Audio: ${e.message}`);
    } finally {
      setAudioLoading(false);
    }
  };

  const changeVoice = (v) => {
    if (v === voice) return;
    // Invalidate cached audio so next Listen re-fetches in new voice
    if (audioRef.current) { audioRef.current.pause(); audioRef.current = null; }
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    setAudioPlaying(false);
    setVoice(v);
  };

  useEffect(() => {
    // Cleanup audio + blob URL on unmount
    return () => {
      if (audioRef.current) { audioRef.current.pause(); }
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
          onClick={toggleBookmark}
          data-testid="bookmark-toggle"
          aria-pressed={bookmarked}
          className={`absolute top-4 right-16 w-9 h-9 rounded-full glass flex items-center justify-center transition-colors duration-200
            ${bookmarked ? 'gold-border gold-text bg-[#D4AF37]/10' : 'hover:border-white/30 text-white/80'}`}
          aria-label={bookmarked ? 'Remove bookmark' : 'Bookmark this moment'}
          title={bookmarked ? 'Remove bookmark' : 'Bookmark this moment'}
        >
          <Star size={14} fill={bookmarked ? '#D4AF37' : 'none'} />
        </button>
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

        {event.discovered_by && (
          <div className="mb-6 rounded-xl border border-white/5 bg-white/[0.02] px-4 py-3.5" data-testid="discovered-by">
            <div className="flex items-center gap-2 mb-1.5">
              <Users size={11} className="gold-text" />
              <span className="font-mono-x text-[9px] uppercase tracking-[0.25em] gold-text">
                Attributed To
              </span>
            </div>
            <div className="text-white/90 text-[14px] leading-snug">{event.discovered_by}</div>
          </div>
        )}

        {event.related_ids && event.related_ids.length > 0 && (
          <div className="mb-6" data-testid="lineage-graph">
            <div className="flex items-center gap-2 mb-2.5">
              <GitBranch size={11} className="gold-text" />
              <span className="font-mono-x text-[9px] uppercase tracking-[0.25em] gold-text">
                Lineage &amp; Trade Chain
              </span>
            </div>
            <div className="flex flex-col gap-1.5">
              {event.related_ids.map((rid) => {
                const rel = allEvents.find((e) => e.id === rid);
                if (!rel) return null;
                const rcat = CATEGORIES[rel.category];
                const dir = rel.year < event.year ? '←' : '→';
                return (
                  <button
                    key={rid}
                    onClick={() => onOpenRelated && onOpenRelated(rid)}
                    data-testid={`related-${rid}`}
                    className="group flex items-center gap-3 text-left px-3 py-2 rounded-lg border border-white/5 hover:border-[#D4AF37]/40 hover:bg-white/[0.03] transition-colors duration-200"
                  >
                    <span className="font-mono-x text-[10px] text-white/40 w-4 text-center">{dir}</span>
                    <span className={`w-1.5 h-1.5 rounded-full ${rcat.dot} shrink-0`} />
                    <span className="font-serif-h text-[14px] text-white/90 flex-1 truncate group-hover:text-white">
                      {rel.title}
                    </span>
                    <span className="font-mono-x text-[10px] text-white/40 shrink-0">
                      {formatYear(rel.year)}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        <div className="flex items-center justify-between mb-3 pt-3 border-t border-white/5 flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <Sparkles size={13} className="gold-text" />
            <span className="font-mono-x text-[10px] uppercase tracking-[0.25em] gold-text">
              Historian&apos;s Deep Dive
            </span>
          </div>
          <div className="flex items-center gap-2">
            <div className="glass rounded-full p-0.5 flex items-center" role="radiogroup" aria-label="Narrator voice">
              <button
                onClick={() => changeVoice('onyx')}
                data-testid="voice-male"
                aria-pressed={voice === 'onyx'}
                className={`px-2.5 h-6 rounded-full font-mono-x text-[9px] uppercase tracking-[0.15em] transition-colors duration-200
                  ${voice === 'onyx' ? 'bg-[#D4AF37] text-[#030304]' : 'text-white/60 hover:text-white'}`}
              >
                Male
              </button>
              <button
                onClick={() => changeVoice('sage')}
                data-testid="voice-female"
                aria-pressed={voice === 'sage'}
                className={`px-2.5 h-6 rounded-full font-mono-x text-[9px] uppercase tracking-[0.15em] transition-colors duration-200
                  ${voice === 'sage' ? 'bg-[#D4AF37] text-[#030304]' : 'text-white/60 hover:text-white'}`}
              >
                Female
              </button>
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
