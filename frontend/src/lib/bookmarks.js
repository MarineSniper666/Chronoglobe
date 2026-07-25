// LocalStorage bookmarks helper
const KEY = 'chronoglobe:bookmarks:v1';

const read = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '[]');
  } catch { return []; }
};

const write = (list) => {
  try { localStorage.setItem(KEY, JSON.stringify(list)); } catch {}
};

export const listBookmarks = () => read();

export const isBookmarked = (eventId) =>
  read().some((b) => b.event_id === eventId);

export const addBookmark = (event, year) => {
  const list = read();
  if (list.some((b) => b.event_id === event.id)) return list;
  list.unshift({
    id: `bm_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
    event_id: event.id,
    title: event.title,
    year: event.year,
    at_year: Math.round(year),
    region: event.region,
    category: event.category,
    added_at: new Date().toISOString(),
  });
  write(list);
  return list;
};

export const removeBookmark = (eventId) => {
  const list = read().filter((b) => b.event_id !== eventId);
  write(list);
  return list;
};

export const clearBookmarks = () => { write([]); return []; };

export const exportBookmarksJson = () => {
  const list = read();
  const payload = {
    app: 'chronoglobe',
    version: 1,
    exported_at: new Date().toISOString(),
    count: list.length,
    bookmarks: list,
  };
  return JSON.stringify(payload, null, 2);
};

export const importBookmarksJson = (jsonText) => {
  try {
    const parsed = JSON.parse(jsonText);
    if (!parsed || !Array.isArray(parsed.bookmarks)) throw new Error('Invalid file');
    const existing = read();
    const seen = new Set(existing.map((b) => b.event_id));
    const merged = [...existing];
    for (const b of parsed.bookmarks) {
      if (!b.event_id || seen.has(b.event_id)) continue;
      merged.push(b);
      seen.add(b.event_id);
    }
    write(merged);
    return merged;
  } catch (e) {
    throw new Error(`Import failed: ${e.message}`);
  }
};
