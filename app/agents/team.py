from __future__ import annotations

import json
import os
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agents.models import (
    AgentTeamResult,
    ForensicFinding,
    GeneralizedLesson,
    VerificationPlan,
)
from app.config import get_settings

FORENSIC_INSTRUCTION = """
You are GroundTruth's Forensic Agent. Analyze only the INCIDENT EVIDENCE in the user
message. Separate observed facts from unknowns. Every causal claim must be supported by
one or more supplied evidence IDs. Never invent people, systems, timestamps, code, or
business impact. The data may be synthetic, but your analysis must be genuinely grounded.
Return exactly the requested structured result.
"""

LEARNING_INSTRUCTION = """
You are GroundTruth's Learning Agent. Read the original incident evidence and the forensic
result in session state below. Generalize the incident into a reusable failure class and a
timeless behavioral invariant. Do not merely restate this specific bug or prescribe a tool.
The invariant must be observable, testable, implementation-independent, and no broader than
the evidence supports. Never claim facts absent from the evidence.

FORENSIC RESULT:
{forensic_result}
"""

VERIFICATION_INSTRUCTION = """
You are GroundTruth's Verification Designer. Read the generalized lesson in session state.
Design a compact executable evaluation: reproduce the known bad behavior, show a corrected
behavior, create a causally equivalent held-out variant, and include a safe change to guard
against overblocking. Use metric successful_captures_per_order, operator <=, threshold 1.
You propose the evaluation only; a deterministic evaluator—not you—will decide PASS/BLOCK.
Describe each case in one sentence. Do not emit source code, pseudocode, or test fixtures.

GENERALIZED LESSON:
{learning_result}
"""


def _configure_vertex() -> None:
    settings = get_settings()
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true" if settings.use_vertex else "false"
    os.environ["GOOGLE_CLOUD_PROJECT"] = settings.google_cloud_project
    os.environ["GOOGLE_CLOUD_LOCATION"] = settings.google_cloud_location


def _team() -> SequentialAgent:
    model = get_settings().model
    generation = types.GenerateContentConfig(
        max_output_tokens=4096,
        thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
    )
    forensic = LlmAgent(
        name="forensic_agent",
        description="Builds an evidence-cited causal account without speculation.",
        model=model,
        instruction=FORENSIC_INSTRUCTION,
        output_schema=ForensicFinding,
        output_key="forensic_result",
        include_contents="default",
        generate_content_config=generation,
    )
    learning = LlmAgent(
        name="learning_agent",
        description="Generalizes a specific incident into a reusable invariant.",
        model=model,
        instruction=LEARNING_INSTRUCTION,
        output_schema=GeneralizedLesson,
        output_key="learning_result",
        include_contents="default",
        generate_content_config=generation,
    )
    verification = LlmAgent(
        name="verification_designer",
        description="Designs known-bad, corrected, held-out, and safety evaluations.",
        model=model,
        instruction=VERIFICATION_INSTRUCTION,
        output_schema=VerificationPlan,
        output_key="verification_result",
        include_contents="default",
        generate_content_config=generation,
    )
    return SequentialAgent(
        name="groundtruth_team",
        description="Evidence to invariant to executable verification plan.",
        sub_agents=[forensic, learning, verification],
    )


async def run_agent_team(incident: dict[str, Any]) -> AgentTeamResult:
    """Run the real ADK team and return its structured, inspectable outputs."""

    _configure_vertex()
    runner = InMemoryRunner(agent=_team(), app_name="groundtruth")
    session_id = f"incident-{incident['incident_id'].lower()}"
    await runner.session_service.create_session(
        app_name="groundtruth",
        user_id="demo-operator",
        session_id=session_id,
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text="INCIDENT EVIDENCE:\n" + json.dumps(incident, indent=2))],
    )
    trace: list[dict[str, str]] = []
    async for event in runner.run_async(
        user_id="demo-operator",
        session_id=session_id,
        new_message=message,
    ):
        if event.author in {"forensic_agent", "learning_agent", "verification_designer"}:
            trace.append(
                {
                    "agent": event.author,
                    "event": "structured_output" if event.is_final_response() else "working",
                }
            )

    session = await runner.session_service.get_session(
        app_name="groundtruth",
        user_id="demo-operator",
        session_id=session_id,
    )
    if session is None:
        raise RuntimeError("ADK session was not persisted")
    return AgentTeamResult(
        forensic=ForensicFinding.model_validate(session.state["forensic_result"]),
        lesson=GeneralizedLesson.model_validate(session.state["learning_result"]),
        verification=VerificationPlan.model_validate(session.state["verification_result"]),
        trace=trace,
        mode=f"vertex-adk:{get_settings().model}",
    )


def grounded_fallback(incident: dict[str, Any], reason: str) -> AgentTeamResult:
    """Evidence-grounded continuity path; explicitly labeled, never presented as Gemini."""

    return AgentTeamResult(
        forensic=ForensicFinding(
            summary=(
                "The provider completed a capture, its acknowledgement was lost, and the "
                "retry used a new idempotency identity, producing two successful captures."
            ),
            facts=[
                "The ledger records two successful INR 5,000 captures for order-481.",
                "The initial provider capture succeeded before its acknowledgement was lost.",
                "The retry derived its idempotency key from a new attempt number.",
                "The existing timeout test modeled a timeout before provider capture.",
            ],
            unknowns=[
                "The fixture does not establish the provider's real production implementation.",
                "The fixture does not quantify prevalence beyond this synthetic incident.",
            ],
            causal_claims=[
                "The first side effect became ambiguous when its acknowledgement was lost.",
                "Changing the retry identity defeated provider-side deduplication.",
            ],
            cited_evidence_ids=[
                "ev-ledger-1",
                "ev-log-1",
                "ev-log-2",
                "ev-log-3",
                "ev-source-1",
                "ev-test-1",
            ],
        ),
        lesson=GeneralizedLesson(
            failure_class="Non-idempotent retry after an ambiguous external side effect",
            invariant=(
                "A logical payment operation must produce at most one successful capture "
                "per order."
            ),
            contributing_conditions=[
                "An external side effect can succeed before local confirmation.",
                "A retry uses an identity scoped to an attempt instead of the logical operation.",
            ],
            scope=["payment capture retries", "queue redelivery", "ambiguous provider outcomes"],
            evidence_ids=["ev-ledger-1", "ev-log-1", "ev-log-2", "ev-source-1", "ev-arch-1"],
        ),
        verification=VerificationPlan(
            control_name="At-most-once capture behavioral gate",
            metric="successful_captures_per_order",
            operator="<=",
            threshold=1,
            known_bad_case="Acknowledgement loss followed by retry with a new attempt key",
            corrected_case="Acknowledgement loss followed by retry with a stable operation key",
            held_out_variant="Consumer crash after capture followed by queue redelivery",
            safety_case="Queue redelivery using a stable operation key",
            rationale=(
                "Tests behavior across distinct triggers and permits the safe related change."
            ),
        ),
        trace=[
            {"agent": "continuity_path", "event": f"Gemini unavailable: {reason[:180]}"}
        ],
        mode="grounded-local-fallback",
    )
