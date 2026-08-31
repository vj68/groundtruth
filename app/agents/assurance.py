from __future__ import annotations

import json
import os
from collections.abc import Callable
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agents.assurance_models import (
    AssuranceAgentResult,
    CausalAnalysis,
    EvidenceAnalysis,
    InstitutionalAction,
    PatternAnalysis,
    ProofAnalysis,
)
from app.config import get_settings


def _vertex_environment() -> None:
    settings = get_settings()
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true" if settings.use_vertex else "false"
    os.environ["GOOGLE_CLOUD_PROJECT"] = settings.google_cloud_project
    os.environ["GOOGLE_CLOUD_LOCATION"] = settings.google_cloud_location


def _agent_team() -> SequentialAgent:
    settings = get_settings()
    generation = types.GenerateContentConfig(
        max_output_tokens=3072,
        thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
    )
    investigator = LlmAgent(
        name="evidence_investigator",
        model=settings.model,
        description="Separates observed failure evidence from speculation.",
        instruction="""
You are GroundTruth's Evidence Investigator. Reconstruct only what the supplied public issue,
pre-fix source snapshot, and mutation site support. Identify the strongest signals, plausible
alternatives, and evidence limitations. You do not have the eventual fixing PR. Do not invent
its contents or use outside knowledge. Return the requested structured output only.
""",
        output_schema=EvidenceAnalysis,
        output_key="evidence_analysis",
        generate_content_config=generation,
    )
    causal = LlmAgent(
        name="causal_analyst",
        model=settings.model,
        description="Derives a reusable causal failure class rather than a textual label.",
        instruction="""
You are GroundTruth's Causal Analyst. Use the packet and investigator result to trace the exact
mechanism from shared object construction through mutation and concurrent observation. State a
failure class and a reusable invariant. Distinguish an outer Go value copy from nested pointer
isolation. Use only supplied evidence.

INVESTIGATION:
{evidence_analysis}
""",
        output_schema=CausalAnalysis,
        output_key="causal_analysis",
        generate_content_config=generation,
    )
    scout = LlmAgent(
        name="pattern_scout",
        model=settings.model,
        description="Searches beyond the reported component for the complete causal signature.",
        instruction="""
You are GroundTruth's Pattern Scout. Inspect every supplied source snapshot. A finding requires
all parts of the causal signature: a reusable package-level spec, a nested pointer, and a call to
the wrapper that mutates that nested object. List candidates and explain causal equivalence.
Reject wording-only matches and state a false-positive guard.

CAUSAL ANALYSIS:
{causal_analysis}
""",
        output_schema=PatternAnalysis,
        output_key="pattern_analysis",
        generate_content_config=generation,
    )
    adversary = LlmAgent(
        name="adversary",
        model=settings.model,
        description="Designs a falsifier and a safe control for the suspected pattern.",
        instruction="""
You are GroundTruth's Adversary. Design the smallest deterministic interleaving that proves
whether two callers share and overwrite the same nested Volume object. Define the vulnerable
observation and the fresh-object safe control. Do not claim execution; a trusted evaluator runs
the proof after you return the plan.

PATTERN ANALYSIS:
{pattern_analysis}
""",
        output_schema=ProofAnalysis,
        output_key="proof_analysis",
        generate_content_config=generation,
    )
    architect = LlmAgent(
        name="learning_architect",
        model=settings.model,
        description="Turns verified evidence into durable organizational protection.",
        instruction="""
You are GroundTruth's Learning Architect. Convert this candidate failure class into technical
controls, review/process improvements, and developmental human learning. Define how the lesson
should propagate to future repositories. Never blame or score an individual. The historical
answer key is still withheld; recommend actions conditional on trusted verification.

PROOF PLAN:
{proof_analysis}
""",
        output_schema=InstitutionalAction,
        output_key="institutional_action",
        generate_content_config=generation,
    )
    return SequentialAgent(
        name="groundtruth_blind_replay_team",
        description="Evidence to cause to scope to proof to institutional learning.",
        sub_agents=[investigator, causal, scout, adversary, architect],
    )


async def run_assurance_agents(
    packet: dict[str, Any],
    on_progress: Callable[[str], None] | None = None,
) -> AssuranceAgentResult:
    settings = get_settings()
    _vertex_environment()
    runner = InMemoryRunner(agent=_agent_team(), app_name="groundtruth-blind-replay")
    session_id = f"blind-replay-{packet['snapshot_commit'][:10]}"
    await runner.session_service.create_session(
        app_name="groundtruth-blind-replay",
        user_id="groundtruth-operator",
        session_id=session_id,
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text="ALLOWED EVIDENCE PACKET:\n" + json.dumps(packet, indent=2))],
    )
    authors = {
        "evidence_investigator",
        "causal_analyst",
        "pattern_scout",
        "adversary",
        "learning_architect",
    }
    trace: list[dict[str, str]] = []
    async for event in runner.run_async(
        user_id="groundtruth-operator",
        session_id=session_id,
        new_message=message,
    ):
        if event.author in authors and event.is_final_response():
            trace.append({"agent": event.author, "event": "structured_output"})
            if on_progress:
                on_progress(event.author)

    session = await runner.session_service.get_session(
        app_name="groundtruth-blind-replay",
        user_id="groundtruth-operator",
        session_id=session_id,
    )
    if session is None:
        raise RuntimeError("ADK assurance session was not persisted")
    return AssuranceAgentResult(
        evidence=EvidenceAnalysis.model_validate(session.state["evidence_analysis"]),
        causal=CausalAnalysis.model_validate(session.state["causal_analysis"]),
        pattern=PatternAnalysis.model_validate(session.state["pattern_analysis"]),
        proof=ProofAnalysis.model_validate(session.state["proof_analysis"]),
        intervention=InstitutionalAction.model_validate(session.state["institutional_action"]),
        trace=trace,
        mode=f"vertex-adk:{settings.model}",
    )


def assurance_fallback(reason: str) -> AssuranceAgentResult:
    return AssuranceAgentResult(
        evidence=EvidenceAnalysis(
            observed_symptom=(
                "Concurrent ConfigMap mounts can resolve through the wrong wrapper path and "
                "leave pods waiting in ContainerCreating."
            ),
            strongest_signals=[
                "The failure is intermittent and appears under simultaneous mounts.",
                "Atomic-writer paths disagree with the logical ConfigMap volume being mounted.",
                "NewWrapperMounter mutates spec.Volume.Name.",
            ],
            competing_hypotheses=[
                "A missing ConfigMap can produce a similar mount-level symptom "
                "but not this path collision."
            ],
            evidence_limits=[
                "The supplied packet contains a bounded source snapshot, not the whole repository."
            ],
        ),
        causal=CausalAnalysis(
            root_cause=(
                "Each plugin reuses a package-level volume.Spec. Passing the outer struct by value "
                "does not copy its nested *api.Volume; the wrapper mutates that shared object's "
                "Name, "
                "so concurrent mounts overwrite one another."
            ),
            causal_chain=[
                "A package-level volume.Spec owns a nested *api.Volume.",
                "Multiple mounts reuse the same spec template.",
                "NewWrapperMounter receives only a shallow outer copy.",
                "It writes a request-specific name through the shared pointer.",
                "An interleaving makes one mount observe another mount's wrapper name.",
            ],
            failure_class="Shared mutable nested state reused across concurrent operations",
            reusable_invariant=(
                "Request-specific operations must not mutate pointer-reachable state shared by "
                "another concurrent request."
            ),
        ),
        pattern=PatternAnalysis(
            search_signature=[
                "package-level wrappedVolumeSpec value",
                "nested *api.Volume pointer",
                "NewWrapperMounter called with the reusable value",
                "request-specific mutation of spec.Volume.Name",
            ],
            candidate_components=["ConfigMap", "Secret", "Downward API", "GitRepo"],
            equivalence_reason=(
                "All four plugins retain the same mutable nested pointer and pass it into the same "
                "request-specific mutating wrapper path."
            ),
            false_positive_guard=(
                "Do not flag a factory-created spec, a deep copy, or a call path that never "
                "mutates "
                "pointer-reachable state."
            ),
        ),
        proof=ProofAnalysis(
            falsification_strategy=(
                "Shallow-copy one shared spec into Mount A and Mount B, write different "
                "wrapper names "
                "in an A/B interleaving, and assert that A retains its own name."
            ),
            vulnerable_observation="Mount A changes from wrapped_config-a to wrapped_config-b.",
            safe_control=(
                "Fresh nested Volume objects preserve distinct names across the same interleaving."
            ),
            confidence_basis=[
                "The nested object identity is shared in the vulnerable construction.",
                "The trusted interleaving directly observes cross-request overwrite.",
                "Every candidate satisfies the complete structural signature.",
            ],
        ),
        intervention=InstitutionalAction(
            technical_controls=[
                "Construct a fresh spec and nested Volume for every wrapper operation.",
                "Add a concurrent multi-volume regression test and race-detector lane.",
                "Scan new package-level templates for request-path mutation through "
                "nested pointers.",
            ],
            process_improvements=[
                "When a causal pattern is verified, expand review scope to every "
                "structural sibling.",
                "Require evidence that concurrency ownership is explicit in shared templates.",
            ],
            capability_development=[
                "Run a short Go shallow-copy and pointer-aliasing teach-back using "
                "the real failure."
            ],
            propagation_policy=(
                "Attach this invariant to future changes that introduce reusable object "
                "templates on "
                "concurrent request paths; require a fresh-object or deep-copy proof before merge."
            ),
            protected_value=(
                "One diagnosed failure protects every equivalent component and prevents each team "
                "from paying separately to learn the same concurrency lesson."
            ),
        ),
        trace=[{"agent": "grounded_continuity", "event": reason[:180]}],
        mode="grounded-local-fallback",
    )
