from __future__ import annotations

import asyncio
import base64
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.fixtures import load_incident
from app.store import get_store
from app.workflow import create_run, execute_run

app = FastAPI(
    title="GroundTruth",
    description="Executable organizational learning for AI-native engineering.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"incident": load_incident()},
    )


@app.get("/healthz")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "groundtruth"}


@app.get("/api/incident")
async def incident() -> dict:
    return load_incident()


@app.post("/api/runs", status_code=202)
async def start_run() -> dict[str, str]:
    store = get_store()
    run = create_run()
    store.create(run)
    asyncio.create_task(execute_run(run.id, store))
    return {"run_id": run.id, "status": run.status}


@app.get("/api/runs")
async def list_runs() -> list[dict]:
    return [json.loads(run.model_dump_json()) for run in get_store().list()]


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str) -> dict:
    run = get_store().get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return json.loads(run.model_dump_json())


@app.post("/api/pubsub/incidents", status_code=204)
async def pubsub_incident(request: Request) -> None:
    """Google Pub/Sub push entrypoint; message content is intentionally not trusted."""

    envelope = await request.json()
    encoded = envelope.get("message", {}).get("data", "")
    if encoded:
        base64.b64decode(encoded, validate=True)
    store = get_store()
    run = create_run()
    store.create(run)
    asyncio.create_task(execute_run(run.id, store))
