from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from app.domain import utc_now


class AssuranceStatus(StrEnum):
    QUEUED = "queued"
    INGESTING = "ingesting"
    CAUSAL = "causal-analysis"
    SCANNING = "scope-scan"
    PROVING = "proof"
    REVEALING = "ground-truth-reveal"
    LEDGER = "ledger-commit"
    COMPLETE = "complete"
    FAILED = "failed"


class AssuranceEvent(BaseModel):
    sequence: int
    stage: AssuranceStatus
    agent: str
    title: str
    detail: str
    timestamp: datetime = Field(default_factory=utc_now)
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentArtifact(BaseModel):
    agent: str
    title: str
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)
    evidence_ids: list[str] = Field(default_factory=list)


class ProductExposure(BaseModel):
    product: str
    team: str
    component: str
    relationship: str
    status: str
    action: str
    evidence: str


class EvidenceCheck(BaseModel):
    id: str
    label: str
    decision: str
    observed: str
    expected: str
    evidence: list[str] = Field(default_factory=list)
    trusted: bool = True


class AssuranceRun(BaseModel):
    id: str
    organization_id: str = "northstar-engineering"
    change_id: str
    status: AssuranceStatus = AssuranceStatus.QUEUED
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    mode: str = "grounded-local"
    events: list[AssuranceEvent] = Field(default_factory=list)
    artifacts: list[AgentArtifact] = Field(default_factory=list)
    evaluations: list[EvidenceCheck] = Field(default_factory=list)
    exposures: list[ProductExposure] = Field(default_factory=list)
    proactive_actions: list[dict[str, Any]] = Field(default_factory=list)
    decision: str | None = None
    decision_reason: str | None = None
    memory_update: dict[str, Any] | None = None
    ground_truth: dict[str, Any] | None = None
    ledger_events: list[dict[str, Any]] = Field(default_factory=list)
    ledger_verification: dict[str, Any] | None = None
    agent_trace: list[dict[str, str]] = Field(default_factory=list)
    error: str | None = None
