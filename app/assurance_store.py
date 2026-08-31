from __future__ import annotations

import json
from threading import RLock
from typing import Protocol

from google.cloud import firestore

from app.config import get_settings
from app.domain import utc_now
from app.platform_domain import AssuranceRun


class AssuranceStore(Protocol):
    def create(self, run: AssuranceRun) -> AssuranceRun: ...
    def save(self, run: AssuranceRun) -> AssuranceRun: ...
    def get(self, run_id: str) -> AssuranceRun | None: ...
    def list(self) -> list[AssuranceRun]: ...


class MemoryAssuranceStore:
    def __init__(self) -> None:
        self._runs: dict[str, AssuranceRun] = {}
        self._lock = RLock()

    def create(self, run: AssuranceRun) -> AssuranceRun:
        return self.save(run)

    def save(self, run: AssuranceRun) -> AssuranceRun:
        with self._lock:
            run.updated_at = utc_now()
            self._runs[run.id] = run.model_copy(deep=True)
            return run

    def get(self, run_id: str) -> AssuranceRun | None:
        with self._lock:
            run = self._runs.get(run_id)
            return run.model_copy(deep=True) if run else None

    def list(self) -> list[AssuranceRun]:
        with self._lock:
            return [run.model_copy(deep=True) for run in self._runs.values()]


class FirestoreAssuranceStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = firestore.Client(project=settings.google_cloud_project)
        self._collection = self._client.collection("groundtruth-assurance-runs")

    def create(self, run: AssuranceRun) -> AssuranceRun:
        return self.save(run)

    def save(self, run: AssuranceRun) -> AssuranceRun:
        run.updated_at = utc_now()
        self._collection.document(run.id).set(json.loads(run.model_dump_json()))
        return run

    def get(self, run_id: str) -> AssuranceRun | None:
        snapshot = self._collection.document(run_id).get()
        if not snapshot.exists:
            return None
        return AssuranceRun.model_validate(snapshot.to_dict())

    def list(self) -> list[AssuranceRun]:
        return [AssuranceRun.model_validate(doc.to_dict()) for doc in self._collection.stream()]


_assurance_store: AssuranceStore | None = None


def get_assurance_store() -> AssuranceStore:
    global _assurance_store
    if _assurance_store is None:
        _assurance_store = (
            FirestoreAssuranceStore() if get_settings().use_firestore else MemoryAssuranceStore()
        )
    return _assurance_store
