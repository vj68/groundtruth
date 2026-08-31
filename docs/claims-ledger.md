# Claims ledger

This ledger prevents the demo from outrunning its evidence.

| Claim | Status | Evidence | Limit |
|---|---|---|---|
| Kubernetes issue #29297 is real | Verified | Public [GitHub issue](https://github.com/kubernetes/kubernetes/issues/29297) | Historical 2016 case |
| The benchmark source is pre-fix | Verified | Pinned commit `d7150bfaeae642efc08c8ede0ed2ec8ecb340c8e` | Bounded excerpts, not full repository checkout |
| The agent packet excludes the answer key | Verified | `allowed_evidence_packet()`; test asserts `29641` and `expected_paths` are absent | Application-level isolation, not an external audit |
| The causal signature appears in four plugins | Verified | Trusted structural evaluator; exact file and line evidence | Purpose-built evaluator for this failure class |
| A shallow copy shares the nested object | Verified | Deterministic A/B aliasing reproducer | Minimal semantic reproducer, not a full Kubernetes e2e run |
| Fresh objects isolate both mounts | Verified | Deterministic safe-control execution | Same bounded reproducer |
| Historical PR #29641 changed the same four plugins | Verified | Public [merged PR](https://github.com/kubernetes/kubernetes/pull/29641) and file diff | Historical external answer key |
| Blind findings match the answer key exactly | Verified | Four discovered paths equal four withheld paths; precision 1.0, recall 1.0 | One benchmark case |
| Gemini 3.5 Flash executes five agents | Verified | Live Vertex run returned five ADK terminal structured outputs | Cloud/model access and latency dependent |
| ADK orchestrates five specialists | Verified | `SequentialAgent`, five `LlmAgent` objects, Pydantic session outputs, trace | Sequential rather than parallel |
| Ledger events are hash-linked | Verified | SHA-256 canonical event hashes and chain verifier | Demo-scale in-process ledger API |
| Ledger exposes no update/delete operation | Verified | Public `LearningLedger` API and tests | Storage administrator controls are outside this PoC |
| All automated tests pass | Verified | `62 passed`; Ruff clean | Test suite is repository-specific |
| All seven platform routes render | Verified | FastAPI tests plus Playwright desktop/mobile walkthrough | Chrome/Playwright browser coverage |
| Browser console is clean | Verified | Playwright console check: zero errors/warnings | Local production-like run |
| Public cloud path works end to end | Previously verified, redeployment pending | Firebase Hosting → Cloud Run → Vertex → Firestore | Must be reverified for the rebuilt revision |
| NSTR-204 is a real production PR | **Not claimed** | Explicitly labeled synthetic concept data | Demonstrates future enforcement only |
| Northstar metrics represent a real company | **Not claimed** | UI and documentation disclosure | Synthetic organizational model |
| GroundTruth prevents every recurring bug | **Not claimed** | One exact historical benchmark | Requires broad longitudinal evaluation |
| GroundTruth proves financial ROI | **Not claimed** | Product thesis and concept ledger only | Requires deployment outcome data |
| Contributors were incompetent | **Not claimed** | No individual evaluation | Product is designed around systemic improvement |

## Evidence classes

### Real public evidence

- Kubernetes issue, comments, repository paths, commits, and fixing PR.

### Real execution

- Gemini/Vertex calls;
- Google ADK orchestration and structured state handoff;
- structural evaluator and deterministic reproducer;
- hash computation and chain verification;
- FastAPI workflow, tests, browser interaction, and cloud infrastructure.

### Synthetic concept data

- Northstar Engineering organization, teams, people, metrics, portfolio, and outcomes;
- future change `NSTR-204`;
- any avoided-cost or organizational-performance illustration.

The interface discloses these classes where they appear. It does not mix a synthetic future
change into the historical Kubernetes answer-key calculation.
