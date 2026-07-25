# Chronoglobe — Interactive World History Atlas

## Problem Statement
Design an interactive map of the world from the start of civilization to today. Must include land transformations (e.g., Bering Land Bridge), viruses/pandemics that wiped out populations, and technologies. Use databases from all over the world (Smithsonian and others) for accurate telling. A globe the user can spin with clickable regions that show details.

## User Choices (Feb 2026)
- **View**: 3D interactive globe (primary) + 2D map toggle for sensory accessibility
- **Timeline**: Auto-plays starting at 25,000 BCE, era markers have 2.5-minute cooldown
- **Data**: Historically curated using Smithsonian/British Museum/UNESCO/WHO sources
- **AI**: Claude Sonnet 4.5 for deep-dive expansions
- **Auth**: None — public exploration

## Architecture
- **Backend**: FastAPI + MongoDB + emergentintegrations (Claude Sonnet 4.5 streaming SSE)
  - `/api/` health check
  - `/api/events` — 66 curated historical events
  - `/api/events/{id}` — single event
  - `/api/expand` — SSE stream of Claude Sonnet 4.5 historical narrative
- **Frontend**: React + react-globe.gl (3D) + react-simple-maps (2D) + Tailwind
  - Auto-playing timeline (25,000 BCE → 2026 CE) driven by `requestAnimationFrame`
  - Era jump buttons with SVG cooldown rings
  - Category filter layers (Civilizations, Land, Pandemics, Technology)
  - Side panel with streamed AI content on marker click

## Design System
- Dark space-observatory + ancient cartography aesthetic
- Fonts: Cormorant Garamond (headings), JetBrains Mono (data), Outfit (body)
- Palette: black backgrounds, cartographer gold (#D4AF37), earth green, blood red, steel blue
- Glassmorphism panels with 20-24px backdrop-blur, star-field background

## Historical Dataset (66 events)
- **Civilizations** (24): Jericho, Sumer, Egypt, Indus, Xia, Olmec, Athens, Rome, Han, Maya, Byzantium, Islamic Caliphate, Tang, Vikings, Mongols, Mali, Inca, Aztec, Ottoman, USA, USSR, etc.
- **Land Transformations** (9): Bering Land Bridge, Doggerland, Green Sahara end, Thera, Vesuvius, Krakatoa, Tambora, Dust Bowl, Aral Sea
- **Pandemics** (9): Antonine, Justinian, Black Death, Smallpox in Americas, Cocoliztli, Cholera, 1918 Flu, HIV, COVID-19
- **Technologies** (24): Fire, Agriculture, Pottery, Writing, Wheel, Bronze, Iron, Alphabet, Paper, Gunpowder, Bi Sheng, Gutenberg, Steam, Electricity, Flight, Antibiotics, Nuclear, Transistor, DNA, Sputnik, Moon, ARPANET, Web, iPhone, CRISPR, LLMs

## What's Implemented (2026-02)
- Complete first-finish MVP passing all backend + frontend tests (100/100%)
- 66 curated historical events with source attribution
- 3D globe with pulsing category markers + 2D accessibility fallback
- Auto-playing timeline with era jumps (cooldown), scrubber, speed control
- Claude Sonnet 4.5 streaming AI deep-dive per event
- Category filter layers

## Backlog (P0 → P2)
- **P1**: Search box to jump to any event by name
- **P1**: Country/region outlines that appear/disappear as empires rise & fall
- **P1**: Migration path arcs (e.g. Beringia crossing, Silk Road, Columbian Exchange)
- **P2**: Cite specific citations/DOIs in the AI expansion output
- **P2**: Ability to bookmark/share a moment via URL (?year=1347)
- **P2**: Audio narration of the expansion (OpenAI TTS)
