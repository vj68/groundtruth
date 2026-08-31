from __future__ import annotations

import json
from threading import RLock
from typing import Protocol

from google.cloud import firestore

from app.config import get_settings
from app.domain import RunRecord, utc_now


class Store(Protocol):
    def create(self, run: RunRecord) -> RunRecord: ...
    def save(self, run: RunRecord) -> RunRecord: ...
    def get(self, run_id: str) -> RunRecord | None: ...
    def list(self) -> list[RunRecord]: ...


class MemoryStore:
    def __init__(self) -> None:
        self._runs: dict[str, RunRecord] = {}
        self._lock = RLock()

    def create(self, run: RunRecord) -> RunRecord:
        with self._lock:
            self._runs[run.id] = run.model_copy(deep=True)
            return run

    def save(self, run: RunRecord) -> RunRecord:
        with self._lock:
            run.updated_at = utc_now()
            self._runs[run.id] = run.model_copy(deep=True)
            return run

    def get(self, run_id: str) -> RunRecord | None:
        with self._lock:
            run = self._runs.get(run_id)
            return run.model_copy(deep=True) if run else None

    def list(self) -> list[RunRecord]:
        with self._lock:
            return [run.model_copy(deep=True) for run in self._runs.values()]


class FirestoreStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = firestore.Client(project=settings.google_cloud_project)
        self._collection = self._client.collection(settings.firestore_collection)

    def create(self, run: RunRecord) -> RunRecord:
        return self.save(run)

    def save(self, run: RunRecord) -> RunRecord:
        run.updated_at = utc_now()
        payload = json.loads(run.model_dump_json())
        self._collection.document(run.id).set(payload)
        return run

    def get(self, run_id: str) -> RunRecord | None:
        snapshot = self._collection.document(run_id).get()
        if not snapshot.exists:
            return None
        return RunRecord.model_validate(snapshot.to_dict())

    def list(self) -> list[RunRecord]:
        return [RunRecord.model_validate(doc.to_dict()) for doc in self._collection.stream()]


_store: Store | None = None


def get_store() -> Store:
    global _store
    if _store is None:
        _store = FirestoreStore() if get_settings().use_firestore else MemoryStore()
    return _store
