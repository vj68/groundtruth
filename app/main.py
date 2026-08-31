from __future__ import annotations

import asyncio
import base64
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.assurance_store import get_assurance_store
from app.assurance_workflow import create_assurance_run, execute_assurance
from app.fixtures import load_incident
from app.kubernetes_evidence import allowed_evidence_packet
from app.learning_ledger import get_learning_ledger
from app.platform_data import platform_payload
from app.store import get_store
from app.workflow import create_run, execute_run

app = FastAPI(
    title="GroundTruth",
    description="Executable organizational learning for AI-native engineering.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


PLATFORM_PAGES = {
    "overview": "Organization",
    "changes": "Changes",
    "assurance": "Assurance",
    "memory": "Organizational Memory",
    "incidents": "Incidents & Learning",
    "capability": "People & Capability",
    "outcomes": "Verified Value",
}


def platform_page(request: Request, page: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="platform.html",
        context={
            "page": page,
            "page_title": PLATFORM_PAGES[page],
            "organization": platform_payload()["organization"],
        },
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return platform_page(request, "overview")


@app.get("/overview", response_class=HTMLResponse)
async def overview(request: Request) -> HTMLResponse:
    return platform_page(request, "overview")


@app.get("/changes", response_class=HTMLResponse)
async def changes(request: Request) -> HTMLResponse:
    return platform_page(request, "changes")


@app.get("/changes/{change_id}", response_class=HTMLResponse)
async def change_detail(request: Request, change_id: str) -> HTMLResponse:
    if change_id != "K8S-29297":
        raise HTTPException(status_code=404, detail="Concept change not found")
    return platform_page(request, "assurance")


@app.get("/memory", response_class=HTMLResponse)
async def memory(request: Request) -> HTMLResponse:
    return platform_page(request, "memory")


@app.get("/incidents", response_class=HTMLResponse)
async def incidents(request: Request) -> HTMLResponse:
    return platform_page(request, "incidents")


@app.get("/capability", response_class=HTMLResponse)
async def capability(request: Request) -> HTMLResponse:
    return platform_page(request, "capability")


@app.get("/outcomes", response_class=HTMLResponse)
async def outcomes(request: Request) -> HTMLResponse:
    return platform_page(request, "outcomes")


@app.get("/legacy", response_class=HTMLResponse)
async def legacy(request: Request) -> HTMLResponse:
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


@app.get("/api/platform")
async def platform() -> dict:
    return platform_payload()


@app.get("/api/benchmark")
async def benchmark() -> dict:
    """Return only the evidence allowed before the historical answer-key reveal."""

    return allowed_evidence_packet()


@app.get("/api/learning-ledger")
async def learning_ledger() -> dict:
    ledger = get_learning_ledger()
    return {
        "events": [event.model_dump(mode="json") for event in ledger.list()],
        "verification": ledger.verify(),
    }


@app.post("/api/assurance-runs", status_code=202)
async def start_assurance(change_id: str = "K8S-29297") -> dict[str, str]:
    store = get_assurance_store()
    try:
        run = create_assurance_run(change_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    store.create(run)
    asyncio.create_task(execute_assurance(run.id, store))
    return {"run_id": run.id, "status": run.status}


@app.get("/api/assurance-runs")
async def list_assurance_runs() -> list[dict]:
    return [json.loads(run.model_dump_json()) for run in get_assurance_store().list()]


@app.get("/api/assurance-runs/{run_id}")
async def get_assurance_run(run_id: str) -> dict:
    run = get_assurance_store().get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Assurance run not found")
    return json.loads(run.model_dump_json())


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
    store = get_assurance_store()
    run = create_assurance_run()
    store.create(run)
    asyncio.create_task(execute_assurance(run.id, store))
