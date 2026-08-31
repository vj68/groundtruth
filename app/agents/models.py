from pydantic import BaseModel, Field


class ForensicFinding(BaseModel):
    summary: str
    facts: list[str] = Field(min_length=3, max_length=8)
    unknowns: list[str] = Field(max_length=5)
    causal_claims: list[str] = Field(min_length=2, max_length=6)
    cited_evidence_ids: list[str] = Field(min_length=3)


class GeneralizedLesson(BaseModel):
    failure_class: str
    invariant: str
    contributing_conditions: list[str] = Field(min_length=2, max_length=6)
    scope: list[str] = Field(min_length=2, max_length=6)
    evidence_ids: list[str] = Field(min_length=3)


class VerificationPlan(BaseModel):
    control_name: str
    metric: str
    operator: str
    threshold: int
    known_bad_case: str = Field(max_length=280)
    corrected_case: str = Field(max_length=280)
    held_out_variant: str = Field(max_length=280)
    safety_case: str = Field(max_length=280)
    rationale: str = Field(max_length=500)


class AgentTeamResult(BaseModel):
    forensic: ForensicFinding
    lesson: GeneralizedLesson
    verification: VerificationPlan
    trace: list[dict[str, str]]
    mode: str
