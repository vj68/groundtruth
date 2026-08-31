from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.domain import Evidence, EvidenceKind


def load_incident() -> dict[str, Any]:
    path = get_settings().fixture_dir / "incident-481.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_evidence() -> list[Evidence]:
    incident = load_incident()
    evidence: list[Evidence] = []
    for item in incident["evidence"]:
        evidence.append(
            Evidence(
                id=item["id"],
                kind=EvidenceKind(item["kind"]),
                title=item["title"],
                excerpt=item["excerpt"],
                source=item["source"],
                observed=item.get("observed", True),
            )
        )
    return evidence


def fixture_path(name: str) -> Path:
    return get_settings().fixture_dir / name
