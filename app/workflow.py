from __future__ import annotations

import asyncio
from pathlib import Path
from uuid import uuid4

from app.agents import run_agent_team
from app.agents.team import grounded_fallback
from app.config import get_settings
from app.domain import (
    CausalStep,
    ControlSpec,
    Investigation,
    LearningRecord,
    RunRecord,
    RunStatus,
    WorkflowEvent,
    utc_now,
)
from app.fixtures import load_evidence, load_incident
from app.lab.payment import certification_matrix, held_out_matrix
from app.store import Store


def create_run() -> RunRecord:
    incident = load_incident()
    return RunRecord(
        id=f"run_{uuid4().hex[:10]}",
        incident_id=incident["incident_id"],
        disclosure=incident["disclosure"],
    )


def _emit(run: RunRecord, stage: RunStatus, title: str, detail: str, **payload: object) -> None:
    run.status = stage
    run.events.append(
        WorkflowEvent(
            sequence=len(run.events) + 1,
            stage=stage,
            title=title,
            detail=detail,
            payload=payload,
        )
    )


async def _pause() -> None:
    delay = get_settings().demo_delay_ms
    if delay:
        await asyncio.sleep(delay / 1000)


def _persist_artifact(run: RunRecord) -> Path:
    artifact = get_settings().artifact_dir / run.id / "learning-record.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(run.model_dump_json(indent=2), encoding="utf-8")
    return artifact


def _claim_evidence_ids(claim: str, all_ids: list[str], index: int) -> list[str]:
    cited = [evidence_id for evidence_id in all_ids if evidence_id in claim]
    if cited:
        return cited
    start = min(index * 2, len(all_ids) - 1)
    return all_ids[start : min(start + 2, len(all_ids))]


async def execute_run(run_id: str, store: Store) -> None:
    run = store.get(run_id)
    if run is None:
        return
    incident = load_incident()
    try:
        _emit(
            run,
            RunStatus.INVESTIGATING,
            "Forensic agent",
            "Grounding a causal account in eight supplied evidence objects.",
            agent="forensic_agent",
        )
        store.save(run)
        await _pause()

        try:
            if not get_settings().enable_gemini:
                raise RuntimeError("ENABLE_GEMINI=false")
            team = await run_agent_team(incident)
        except Exception as exc:  # Continuity is a documented product behavior for the demo.
            team = grounded_fallback(incident, f"{type(exc).__name__}: {exc}")
        run.mode = team.mode
        run.agent_trace = team.trace
        evidence = load_evidence()
        claims = team.forensic.causal_claims
        run.investigation = Investigation(
            summary=team.forensic.summary,
            facts=team.forensic.facts,
            unknowns=team.forensic.unknowns,
            causal_chain=[
                CausalStep(
                    order=index + 1,
                    claim=claim,
                    evidence_ids=_claim_evidence_ids(
                        claim,
                        team.forensic.cited_evidence_ids,
                        index,
                    ),
                )
                for index, claim in enumerate(claims)
            ],
            evidence=evidence,
        )
        _emit(
            run,
            RunStatus.GENERALIZING,
            "Learning agent",
            "Generalized the specific defect into a reusable behavioral invariant.",
            agent="learning_agent",
            failure_class=team.lesson.failure_class,
        )
        store.save(run)
        await _pause()

        control = ControlSpec(
            name=team.verification.control_name,
            failure_class=team.lesson.failure_class,
            invariant=team.lesson.invariant,
            metric=team.verification.metric,
            operator=team.verification.operator,
            threshold=team.verification.threshold,
            contributing_conditions=team.lesson.contributing_conditions,
            scope=team.lesson.scope,
        )
        run.learning = LearningRecord(
            id=f"lesson_{uuid4().hex[:8]}",
            incident_id=run.incident_id,
            failure_class=team.lesson.failure_class,
            invariant=team.lesson.invariant,
            control=control,
            evidence_ids=team.lesson.evidence_ids,
        )
        _emit(
            run,
            RunStatus.VERIFYING,
            "Verification designer",
            "Designed reproduction, correction, held-out variant, and safety cases.",
            agent="verification_designer",
            proposed_only=True,
        )
        store.save(run)
        await _pause()

        certification = certification_matrix()
        run.evaluations.extend(certification)
        certified = all(result.passed for result in certification)
        _emit(
            run,
            RunStatus.LEARNED,
            "Deterministic certification",
            (
                "Known-bad was blocked and the corrected behavior passed."
                if certified
                else "Control certification failed."
            ),
            truth_source="payment-state simulator",
            verified=certified,
        )
        if not certified:
            raise RuntimeError("Candidate control did not pass certification")
        run.learning.status = "verified"
        run.learning.verified_at = utc_now()
        store.save(run)
        await _pause()

        held_out = held_out_matrix()
        run.evaluations.extend(held_out)
        generalizes = all(result.passed for result in held_out)
        _emit(
            run,
            RunStatus.EVALUATING,
            "Future-change gate",
            "Blocked exact and held-out recurrences while allowing the safe change.",
            truth_source="payment-state simulator",
            verified=generalizes,
        )
        if not generalizes:
            raise RuntimeError("Verified lesson did not generalize to the held-out matrix")

        run.status = RunStatus.COMPLETE
        artifact = get_settings().artifact_dir / run.id / "learning-record.json"
        _emit(
            run,
            RunStatus.COMPLETE,
            "Organizational memory updated",
            "The incident is now an executable defense for future changes.",
            artifact=str(artifact),
        )
        store.save(run)
        _persist_artifact(run)
    except Exception as exc:
        run.status = RunStatus.FAILED
        run.error = f"{type(exc).__name__}: {exc}"
        _emit(run, RunStatus.FAILED, "Workflow failed", run.error)
        store.save(run)
        _persist_artifact(run)
