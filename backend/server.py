import asyncio
import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, Response, HTMLResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from history_data import list_events, find_event
from history_geo import list_arcs, list_empires
from history_details import get_details
from share_card import render_og_card, render_share_html
from tours import list_tours, find_tour

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

app = FastAPI()
api_router = APIRouter(prefix="/api")


class ExpandRequest(BaseModel):
    event_id: str


def _fmt_year(y: int) -> str:
    if y < 0:
        return f"{abs(y):,} BCE"
    return f"{y} CE"


def _related_titles(related_ids):
    titles = []
    for rid in related_ids or []:
        rel = find_event(rid)
        if rel:
            titles.append(f"{rel['title']} ({_fmt_year(rel['year'])})")
    return titles


def build_deep_dive(event: dict, details: dict) -> str:
    """
    Build a museum-caption-quality writeup from data already on hand,
    in the same **Context** / **What Happened** / **Legacy** shape the
    old LLM prompt asked for. No external API calls, no cost, no key.
    """
    title = event["title"]
    year_str = _fmt_year(event["year"])
    region = event.get("region", "an unrecorded region")
    category = event.get("category", "history")
    summary = event.get("summary", "")
    source = event.get("source")
    discovered_by = details.get("discovered_by")
    related = _related_titles(details.get("related_ids"))

    lines = [f"# {title} — {year_str}", ""]

    lines.append("**Context**")
    context = f"Located in {region}, this {category} entry marks a documented turning point around {year_str}."
    if discovered_by:
        context += f" It is attributed to {discovered_by}."
    lines.append(context)
    lines.append("")

    lines.append("**What Happened**")
    lines.append(summary or "Details for this event are still being curated.")
    lines.append("")

    lines.append("**Legacy**")
    if related:
        legacy = "This connects directly to " + ", ".join(related[:4])
        if len(related) > 4:
            legacy += f", and {len(related) - 4} more linked events"
        legacy += " in the lineage chain — trace them from the panel above."
    else:
        legacy = "Its downstream effects are woven through the broader arc of this era."
    lines.append(legacy)

    if source:
        lines.append("")
        lines.append(f"*Source: {source}*")

    return "\n".join(lines)


@api_router.get("/")
async def root():
    return {"message": "Chronoglobe API online", "events": len(list_events())}


@api_router.get("/events")
async def get_events():
    """Return all historical events, sorted chronologically, with details merged."""
    events = sorted(list_events(), key=lambda e: e["year"])
    for e in events:
        d = get_details(e["id"])
        e["discovered_by"] = d.get("discovered_by")
        e["related_ids"] = d.get("related_ids", [])
    return {"events": events, "count": len(events)}


@api_router.get("/events/{event_id}")
async def get_event(event_id: str):
    e = find_event(event_id)
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    d = get_details(event_id)
    return {**e, "discovered_by": d.get("discovered_by"), "related_ids": d.get("related_ids", [])}


@api_router.post("/expand")
async def expand_event(req: ExpandRequest):
    """
    Stream a museum-caption-quality writeup for an event, built from the
    curated dataset already in this repo. Streamed word-by-word purely so
    the existing frontend "typing reveal" UI keeps working unchanged --
    there's no external API call or cost involved.
    """
    event = find_event(req.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    details = get_details(req.event_id)
    text = build_deep_dive(event, details)

    async def event_generator():
        words = text.split(" ")
        for i, w in enumerate(words):
            chunk = w if i == 0 else f" {w}"
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.012)
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@api_router.get("/arcs")
async def get_arcs():
    return {"arcs": list_arcs()}


@api_router.get("/empires")
async def get_empires():
    return {"empires": list_empires()}


@api_router.get("/og")
async def og_card(event: str):
    ev = find_event(event)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    png = render_og_card(ev)
    return Response(
        content=png,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@api_router.get("/share", response_class=HTMLResponse)
async def share_html(request: Request, event: str, year: Optional[int] = None):
    ev = find_event(event)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    fwd_proto = request.headers.get("x-forwarded-proto")
    fwd_host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    if fwd_host:
        scheme = fwd_proto or "https"
        host = f"{scheme}://{fwd_host}"
    else:
        host = str(request.base_url).rstrip('/')
    api_url = host
    base_url = host
    request_url = f"{host}{request.url.path}?{request.url.query}" if request.url.query else f"{host}{request.url.path}"
    used_year = year if year is not None else ev["year"]
    html = render_share_html(ev, used_year, base_url, api_url, request_url)
    return HTMLResponse(content=html)


@api_router.get("/tours")
async def get_tours():
    """Return all curated Story-Mode tours."""
    return {"tours": list_tours()}


@api_router.get("/tours/{tour_id}")
async def get_tour(tour_id: str):
    t = find_tour(tour_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tour not found")
    return t


app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
