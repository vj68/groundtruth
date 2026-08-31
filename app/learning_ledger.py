from __future__ import annotations

import hashlib
import json
from threading import RLock
from typing import Any

from pydantic import BaseModel, Field

from app.domain import utc_now


class LedgerEvent(BaseModel):
    sequence: int
    learning_id: str
    event_type: str
    actor: str
    timestamp: str = Field(default_factory=lambda: utc_now().isoformat())
    payload: dict[str, Any] = Field(default_factory=dict)
    previous_hash: str
    event_hash: str


class LearningLedger:
    """Append-only, hash-linked learning ledger with no update or delete operation."""

    def __init__(self) -> None:
        self._events: list[LedgerEvent] = []
        self._lock = RLock()

    @staticmethod
    def _hash(event: dict[str, Any]) -> str:
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def append(
        self,
        learning_id: str,
        event_type: str,
        actor: str,
        payload: dict[str, Any],
    ) -> LedgerEvent:
        with self._lock:
            previous_hash = self._events[-1].event_hash if self._events else "GENESIS"
            body = {
                "sequence": len(self._events) + 1,
                "learning_id": learning_id,
                "event_type": event_type,
                "actor": actor,
                "timestamp": utc_now().isoformat(),
                "payload": payload,
                "previous_hash": previous_hash,
            }
            event = LedgerEvent(**body, event_hash=self._hash(body))
            self._events.append(event)
            return event.model_copy(deep=True)

    def list(self) -> list[LedgerEvent]:
        with self._lock:
            return [event.model_copy(deep=True) for event in self._events]

    def verify(self) -> dict[str, Any]:
        with self._lock:
            previous_hash = "GENESIS"
            for event in self._events:
                body = event.model_dump(exclude={"event_hash"})
                if event.previous_hash != previous_hash or self._hash(body) != event.event_hash:
                    return {
                        "valid": False,
                        "events": len(self._events),
                        "failed_at": event.sequence,
                    }
                previous_hash = event.event_hash
            return {
                "valid": True,
                "events": len(self._events),
                "head": previous_hash,
                "scheme": "SHA-256 hash chain · append-only API",
            }


_ledger = LearningLedger()


def get_learning_ledger() -> LearningLedger:
    return _ledger
