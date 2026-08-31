from pydantic import BaseModel, Field


class EvidenceAnalysis(BaseModel):
    observed_symptom: str = Field(max_length=800)
    strongest_signals: list[str] = Field(min_length=2, max_length=5)
    competing_hypotheses: list[str] = Field(min_length=1, max_length=5)
    evidence_limits: list[str] = Field(min_length=1, max_length=4)


class CausalAnalysis(BaseModel):
    root_cause: str = Field(max_length=1200)
    causal_chain: list[str] = Field(min_length=3, max_length=7)
    failure_class: str = Field(max_length=500)
    reusable_invariant: str = Field(max_length=800)


class PatternAnalysis(BaseModel):
    search_signature: list[str] = Field(min_length=2, max_length=6)
    candidate_components: list[str] = Field(min_length=1, max_length=8)
    equivalence_reason: str = Field(max_length=1200)
    false_positive_guard: str = Field(max_length=800)


class ProofAnalysis(BaseModel):
    falsification_strategy: str = Field(max_length=1200)
    vulnerable_observation: str = Field(max_length=800)
    safe_control: str = Field(max_length=800)
    confidence_basis: list[str] = Field(min_length=2, max_length=6)


class InstitutionalAction(BaseModel):
    technical_controls: list[str] = Field(min_length=2, max_length=5)
    process_improvements: list[str] = Field(min_length=1, max_length=5)
    capability_development: list[str] = Field(min_length=1, max_length=4)
    propagation_policy: str = Field(max_length=1200)
    protected_value: str = Field(max_length=800)


class AssuranceAgentResult(BaseModel):
    evidence: EvidenceAnalysis
    causal: CausalAnalysis
    pattern: PatternAnalysis
    proof: ProofAnalysis
    intervention: InstitutionalAction
    trace: list[dict[str, str]]
    mode: str
