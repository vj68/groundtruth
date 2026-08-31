from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(UTC)


class RunStatus(StrEnum):
    RECEIVED = "received"
    INVESTIGATING = "investigating"
    GENERALIZING = "generalizing"
    VERIFYING = "verifying"
    LEARNED = "learned"
    EVALUATING = "evaluating"
    COMPLETE = "complete"
    FAILED = "failed"


class EvidenceKind(StrEnum):
    LOG = "log"
    LEDGER = "ledger"
    SOURCE = "source"
    TEST = "test"
    INCIDENT = "incident"
    ARCHITECTURE = "architecture"


class Evidence(BaseModel):
    id: str
    kind: EvidenceKind
    title: str
    excerpt: str
    source: str
    observed: bool = True


class CausalStep(BaseModel):
    order: int
    claim: str
    evidence_ids: list[str]
    confidence: str = "supported"


class Investigation(BaseModel):
    summary: str
    facts: list[str]
    unknowns: list[str]
    causal_chain: list[CausalStep]
    evidence: list[Evidence]


class ControlSpec(BaseModel):
    name: str
    failure_class: str
    invariant: str
    metric: str = "successful_captures_per_order"
    operator: str = "<="
    threshold: int = 1
    contributing_conditions: list[str]
    scope: list[str]


class LearningRecord(BaseModel):
    id: str
    incident_id: str
    failure_class: str
    invariant: str
    control: ControlSpec
    evidence_ids: list[str]
    verified_at: datetime | None = None
    status: str = "candidate"


class TraceEvent(BaseModel):
    sequence: int
    event: str
    detail: str
    timestamp: datetime = Field(default_factory=utc_now)


class Capture(BaseModel):
    capture_id: str
    order_id: str
    amount: int
    idempotency_key: str


class ScenarioResult(BaseModel):
    case_id: str
    label: str
    expected_decision: str
    observed_captures: int
    invariant_limit: int = 1
    passed: bool
    decision: str
    trace: list[TraceEvent]
    captures: list[Capture]
    duration_ms: int


class WorkflowEvent(BaseModel):
    sequence: int
    stage: RunStatus
    title: str
    detail: str
    timestamp: datetime = Field(default_factory=utc_now)
    payload: dict[str, Any] = Field(default_factory=dict)


class RunRecord(BaseModel):
    id: str
    incident_id: str
    status: RunStatus = RunStatus.RECEIVED
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    mode: str = "grounded-local"
    events: list[WorkflowEvent] = Field(default_factory=list)
    investigation: Investigation | None = None
    learning: LearningRecord | None = None
    evaluations: list[ScenarioResult] = Field(default_factory=list)
    agent_trace: list[dict[str, Any]] = Field(default_factory=list)
    disclosure: str = ""
    error: str | None = None
