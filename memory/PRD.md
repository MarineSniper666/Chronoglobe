# Chronoglobe — Interactive World History Atlas

## Problem Statement
Design an interactive map of the world from the start of civilization to today. Must include land transformations (e.g., Bering Land Bridge), viruses/pandemics that wiped out populations, and technologies. Use databases from all over the world (Smithsonian and others) for accurate telling. A globe the user can spin with clickable regions that show details.

## User Choices (Feb 2026)
- **View**: 3D interactive globe (primary) + 2D map toggle for sensory accessibility
- **Timeline**: Auto-plays starting at 25,000 BCE, era markers with 2.5-minute cooldown
- **Data**: Historically curated using Smithsonian/British Museum/UNESCO/WHO sources
- **AI**: Claude Sonnet 4.5 for deep-dive expansions
- **TTS**: OpenAI tts-1-hd with Male (onyx) / Female (sage) narrator voice options
- **Auth**: None — public exploration
- **Interaction**: Clicking a key point pauses the world; panel shows attribution + lineage of related technologies/events; clicking a related event navigates to it.

## Architecture
- **Backend** (FastAPI + MongoDB + emergentintegrations)
  - `GET /api/events` — 66 curated events with merged `discovered_by` + `related_ids`
  - `GET /api/events/{id}` — single event
  - `GET /api/arcs` — 11 migration/exchange arcs (Beringia, Silk Road, Columbian Exchange, Slave Trade, Apollo)
  - `GET /api/empires` — 19 empire footprints with country arrays
  - `POST /api/expand` — SSE stream of Claude Sonnet 4.5 historian narrative
  - `POST /api/tts` — OpenAI tts-1-hd MP3 audio (voice: onyx | sage | others)
- **Frontend** (React + react-globe.gl + react-simple-maps + Tailwind + Framer)
  - Auto-playing timeline (25,000 BCE → 2026 CE) via requestAnimationFrame
  - Era jump buttons with 2.5-min SVG cooldown rings
  - Category filter layers, centered SearchBox (⌘K), 2D/3D toggle
  - Globe3D renders: empire polygon overlays (fading in/out by year), migration arcs (dashed, active by year), pulsing HTML event markers
  - SidePanel: streams AI content, plays TTS audio, shows Attributed To + clickable Lineage chain, Male/Female voice toggle
  - Auto-pauses timeline on marker/search/lineage click

## Design System
- Dark space-observatory + ancient cartography aesthetic
- Fonts: Cormorant Garamond (headings), JetBrains Mono (data), Outfit (body)
- Palette: black backgrounds, cartographer gold (#D4AF37), earth green, blood red, steel blue
- Glassmorphism panels, star-field, subtle glow

## Data
- **66 events**: 24 civilizations, 9 land transformations, 9 pandemics, 24 technologies
- **11 arcs**: Beringia, Out-of-Africa, Austronesian, Silk Road (Rome & Samarkand), Vinland, Columbian E/W, Slave Trade, Industrial diffusion, Apollo
- **19 empires**: Egypt, Persia, Alexander, Rome (Rep & Emp), Han, Byzantine, Caliphate, Tang, Mongol, Mali, Inca, Aztec, Ottoman, Spanish, British, Mughal, Russian, USSR
- **Lineage graph**: ~40 events mapped to their forebears and descendants

## What's Implemented (2026-02)
### First finish (iteration 1)
- Complete MVP: 3D/2D globe, timeline, era jumps, category filters, AI streaming, side panel — 100% tests pass

### Iteration 2 (arcs, empires, TTS, search)
- Migration arcs + empire overlays on globe
- OpenAI TTS (tts-1-hd) integration
- Centered SearchBox with ⌘K, keyboard nav
- **Fixed**: initial handleListen ReferenceError

### Iteration 3 (deep drop-down, pause, lineage, voice picker)
- Timeline auto-pauses when a marker/search result/lineage item is clicked
- SidePanel shows Attributed To (who discovered/led each event)
- Lineage & Trade Chain — clickable list of related events with ← / → arrows
- Male (onyx) / Female (sage) narrator voice toggle in the panel
- Full backend validation: distinct audio hashes for male vs female, 400 for empty text, fallback for invalid voice
- Frontend E2E verified: pause holds year stable, related-click swaps panel + jumps timeline + refocuses globe

## Backlog (P1 → P2)
- **P1**: URL-shareable moments (?year=1347&event=pan-blackdeath)
- **P1**: Expand lineage to cover all 66 events (currently ~40)
- **P2**: Timeline "compare" mode: split view of two eras side-by-side
- **P2**: Historical audio archive (real speeches when available: MLK 1963, Neil Armstrong etc.)
- **P2**: Export a personalized "history reel" as a video
