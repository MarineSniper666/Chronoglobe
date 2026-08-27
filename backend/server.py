from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, Response, HTMLResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
import uuid

from history_data import list_events, find_event
from history_geo import list_arcs, list_empires
from history_details import get_details
from share_card import render_og_card, render_share_html
from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone
from emergentintegrations.llm.openai import OpenAITextToSpeech

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

app = FastAPI()
api_router = APIRouter(prefix="/api")


class ExpandRequest(BaseModel):
    event_id: str


class TTSRequest(BaseModel):
    text: str
    voice: str = "onyx"


def _fmt_year(y: int) -> str:
    if y < 0:
        return f"{abs(y):,} BCE"
    return f"{y} CE"


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
    """Stream a deeper AI-generated historical narrative for an event."""
    event = find_event(req.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="LLM key not configured")

    system_message = (
        "You are a rigorous, museum-quality historian. When asked about a historical event, "
        "you provide a well-structured, factual expansion suitable for a curious general audience. "
        "Cite scholarship or institutions where relevant (Smithsonian, British Museum, UNESCO, WHO, "
        "national museums). Never invent facts. If a date is contested, say so briefly. "
        "Use markdown with short section headings: **Context**, **What Happened**, **Legacy**. "
        "Keep the response under 350 words."
    )

    prompt = (
        f"Event: {event['title']}\n"
        f"Approximate date: {_fmt_year(event['year'])}\n"
        f"Region: {event['region']}\n"
        f"Category: {event['category']}\n"
        f"Curator summary: {event['summary']}\n"
        f"Primary source hint: {event['source']}\n\n"
        "Expand this into a museum-caption-quality narrative."
    )

    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"expand-{req.event_id}-{uuid.uuid4().hex[:6]}",
        system_message=system_message,
    ).with_model("anthropic", "claude-sonnet-4-5-20250929")

    async def event_generator():
        try:
            async for ev in chat.stream_message(UserMessage(text=prompt)):
                if isinstance(ev, TextDelta):
                    # SSE format
                    yield f"data: {ev.content}\n\n"
                elif isinstance(ev, StreamDone):
                    yield "data: [DONE]\n\n"
                    break
        except Exception as exc:  # surface streaming errors to client
            logging.exception("LLM streaming failed")
            yield f"data: [ERROR] {str(exc)}\n\n"

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


@api_router.post("/tts")
async def tts(req: TTSRequest):
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="LLM key not configured")
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    # OpenAI TTS accepts up to 4096 characters
    text = text[:4000]
    voice = req.voice if req.voice in {"alloy", "ash", "coral", "echo", "fable",
                                        "nova", "onyx", "sage", "shimmer"} else "onyx"
    try:
        engine = OpenAITextToSpeech(api_key=EMERGENT_LLM_KEY)
        audio_bytes = await engine.generate_speech(
            text=text, model="tts-1-hd", voice=voice
        )
    except Exception as e:
        logging.exception("TTS failed")
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")
    return Response(content=audio_bytes, media_type="audio/mpeg")


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


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
