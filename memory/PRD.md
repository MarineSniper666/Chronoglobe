# Chronoglobe — Interactive World History Atlas

## Problem Statement
Design an interactive map of the world from the start of civilization to today. Must include land transformations (e.g., Bering Land Bridge), viruses/pandemics that wiped out populations, and technologies. Use databases from all over the world (Smithsonian and others) for accurate telling. A globe the user can spin with clickable regions that show details.

## User Choices
- **View**: 3D interactive globe (primary) + 2D map toggle for sensory accessibility
- **Timeline**: Auto-plays starting at 25,000 BCE, era markers with 2.5-minute cooldown
- **Data**: Historically curated using Smithsonian/British Museum/UNESCO/WHO sources
- **AI**: Claude Sonnet 4.5 for deep-dive expansions + OpenAI TTS for narration
- **Auth**: None — public exploration

## Architecture
- **Backend** (FastAPI + MongoDB + emergentintegrations):
  - `/api/events`, `/api/events/{id}` — 66 curated historical events
  - `/api/expand` — SSE stream of Claude Sonnet 4.5 narrative
  - `/api/arcs` — 11 migration/trade arcs with year ranges
  - `/api/empires` — 19 historical empires with country footprints
  - `/api/tts` — OpenAI TTS mp3 (tts-1-hd, onyx/sage voices)
- **Frontend** (React + react-globe.gl + react-simple-maps + Tailwind):
  - 3D globe with pulsing markers, arc animations, and empire polygon overlays
  - Auto-playing timeline, era jump buttons with SVG cooldown rings
  - Centered SearchBox with keyboard nav
  - SidePanel with streamed AI text + Listen button + Male/Female voice toggle

## What's Implemented (2026-02)
- 66 curated historical events, 11 migration arcs, 19 empire footprints
- 3D globe (react-globe.gl) with dashed animated arcs + fading empire polygons
- 2D accessibility fallback (react-simple-maps)
- Auto-play timeline 25,000 BCE → 2026 CE with era jumps, cooldowns, speed control
- Claude Sonnet 4.5 streaming deep-dive per event
- OpenAI TTS narration with Male/Female voice toggle
- Event search with keyboard nav (⌘K, arrows, Enter, Esc)
- All backend + frontend tests: 100% pass (iteration_3.json)

## Backlog (P0 → P2)
- P1: Additional empires (Persian Sassanid, Songhai, Zulu, Ming/Qing detail)
- P1: More arcs (Polynesian navigation detail, Trans-Saharan trade, Marco Polo journey)
- P2: Shareable URL params (?year=1347) for classroom linking
- P2: Timeline "compare years" — split-screen 2-globe view
- P2: Related-events lineage graph (SidePanel already scaffolded for `related_ids`)
