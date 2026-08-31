# GroundTruth

> **One team learns. The whole organization gets stronger.**

GroundTruth is an institutional learning control plane for AI-native engineering. It turns
every verified failure into organization-wide memory, preventive controls, and human
capability—so a known mistake does not have to become another team's incident.

**Live demo:** [groundtruth-507213.web.app](https://groundtruth-507213.web.app)

## The problem

AI is increasing the rate of software change faster than organizations increase the rate of
learning. Issues are closed, postmortems become documents, fixes remain local, and the deeper
lesson rarely reaches every structurally related component or future pull request.

GroundTruth closes that loop:

```text
failure → evidence → causal signature → organization-wide search → trusted proof
        → verified learning → preventive control → capability development
```

The core promise is deliberately bounded:

> Once an organization has verified a failure class, future changes should not be allowed to
> repeat it silently.

## The flagship proof: a blind Kubernetes replay

The demo uses real public Kubernetes evidence rather than a fabricated incident:

- original issue: [kubernetes/kubernetes#29297](https://github.com/kubernetes/kubernetes/issues/29297);
- pre-fix source snapshot: `d7150bfaeae642efc08c8ede0ed2ec8ecb340c8e`;
- independently withheld answer key:
  [kubernetes/kubernetes#29641](https://github.com/kubernetes/kubernetes/pull/29641).

During the replay, GroundTruth receives only the issue, bounded pre-fix source snapshots, and
the wrapper mutation path. The later fix, maintainer discussion, and four-file patch scope are
excluded from the agent packet.

Five Google ADK agents then:

1. separate observed evidence from hypotheses;
2. reconstruct the shared-nested-pointer causal mechanism;
3. search for the complete structural signature beyond ConfigMap;
4. design a deterministic falsifying interleaving and safe control; and
5. convert the verified lesson into technical, process, and capability interventions.

A trusted evaluator—not the model—then scans the evidence and executes the pointer-aliasing
reproducer. It finds four affected plugins:

| Component | Relationship | Verified pre-fix location |
|---|---|---|
| ConfigMap | Reported failure | `pkg/volume/configmap/configmap.go` |
| Secret | Proactive sibling exposure | `pkg/volume/secret/secret.go` |
| Downward API | Proactive sibling exposure | `pkg/volume/downwardapi/downwardapi.go` |
| GitRepo | Proactive sibling exposure | `pkg/volume/git_repo/git_repo.go` |

Only after those findings are frozen does GroundTruth reveal the historical fixing PR. The
independent scan matches all four paths with 100% precision and recall.

This is a retrospective benchmark, not a claim that GroundTruth discovered an unknown
Kubernetes bug. The historical patch is an external answer key proving that the system reached
the same blast radius without receiving the answer.

## The “aha” moment

```text
One reported ConfigMap failure
              ↓
Shared mutable nested state under concurrency
              ↓
Secret + Downward API + GitRepo also exposed
              ↓
Exact match to the later human patch
              ↓
Hash-linked learning GT-K8S-0001
              ↓
Future Northstar PR NSTR-204 blocked by the learned invariant
```

The future Northstar PR is explicitly synthetic concept data. Its purpose is to demonstrate
that a verified public lesson can become an enforceable organizational control instead of
remaining historical trivia.

## More than a bug scanner

GroundTruth is not positioned as another SAST tool or issue summarizer. Bug discovery is one
step inside a wider institutional loop:

- **Changes:** route assurance by consequence and intended value.
- **Assurance workspace:** show agent reasoning, trusted evaluators, and decisions.
- **Learning ledger:** preserve verified failure classes, provenance, uncertainty, and controls.
- **Incidents & learning:** connect technical, testing, process, organizational, and human dimensions.
- **People & capability:** create teach-backs, practice labs, pairing, and ownership without
  employee ranking or surveillance.
- **Verified value:** distinguish observed outcomes from attractive but unproven claims.

## Append-only learning ledger

Each verified learning transition is appended as a SHA-256 hash-linked event:

```text
HYPOTHESIS_RECORDED
  → EVIDENCE_VERIFIED
  → GROUND_TRUTH_CONFIRMED
  → CONTROL_ATTACHED
```

Every event includes its actor, payload, timestamp, previous hash, and own hash. The ledger API
supports append and read operations; there is no update or delete method. Corrections and
superseding evidence must become new events, preserving the institution's reasoning history.

## Trust boundaries

- Gemini interprets evidence and proposes causal knowledge.
- Agent outputs are structured and attributable through ADK session state.
- The answer key is absent from the allowed packet and revealed only after analysis.
- Deterministic code decides structural matches, pointer aliasing, precision, recall, and final
  evidence verification.
- Candidate lessons cannot enforce controls until trusted evidence verifies them.
- Gemini failure invokes a clearly labeled grounded continuity path; it never fabricates a
  model run.

## Built with Google Cloud

- **Gemini 3.5 Flash** on Vertex AI's global endpoint.
- **Google Agent Development Kit 2.8** with five `LlmAgent` specialists inside a real
  `SequentialAgent` and structured Pydantic outputs.
- **Cloud Run** for the FastAPI application and asynchronous assurance workflow.
- **Firebase Hosting** for the stable public front door.
- **Firestore Native** for durable assurance runs.
- **Pub/Sub** for asynchronous evidence/incident triggers.
- **Cloud Build + Artifact Registry** for reproducible deployment.

## Run locally

Prerequisites: Python 3.11–3.13, [`uv`](https://docs.astral.sh/uv/), a billed Google Cloud
project, and Application Default Credentials.

```bash
cd groundtruth
cp .env.example .env
gcloud auth application-default login
uv sync
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. Set `ENABLE_GEMINI=false` for the complete deterministic
continuity path without a Vertex call. The run is explicitly labeled
`grounded-local-fallback`.

Verification:

```bash
uv run ruff check app tests
uv run pytest
```

Expected: **62 tests pass**, including sealed-packet isolation, exact structural scope,
aliasing/fresh-object behavior, hash-chain integrity, API routes, and the full workflow.

## Deploy

```bash
gcloud run deploy groundtruth \
  --source=. \
  --project=groundtruth-507213 \
  --region=us-central1 \
  --service-account=groundtruth-runtime@groundtruth-507213.iam.gserviceaccount.com \
  --allow-unauthenticated \
  --min-instances=0 --max-instances=2 \
  --no-cpu-throttling \
  --cpu=1 --memory=1Gi --concurrency=8 --timeout=300 \
  --set-env-vars='GOOGLE_CLOUD_LOCATION=global,MODEL=gemini-3.5-flash,ENABLE_GEMINI=true,USE_VERTEX=true,USE_FIRESTORE=true,DEMO_DELAY_MS=180'
```

## Repository map

```text
app/agents/assurance.py       five-role Google ADK team
app/kubernetes_evidence.py    sealed benchmark, structural evaluator, reproducer
app/assurance_workflow.py     blind replay, reveal, verification, propagation
app/learning_ledger.py        append-only SHA-256 event chain
app/platform_data.py          generic organization and platform concept model
app/main.py                   FastAPI pages, APIs, Pub/Sub entrypoint
templates/platform.html       multi-page application shell
static/platform.*             platform interaction and visual system
tests/test_blind_replay.py    evidence-boundary and end-to-end proof
docs/                         architecture, claims, script, submission material
```

The original single-incident PoC remains preserved on the `archive/incident-poc` branch and
at `/legacy`; it is not the primary product experience.

## Evidence disclosure

Kubernetes issue, source locations, commit identifiers, and fixing PR are real public
artifacts. Northstar organization, people, financial, portfolio, and future-PR data are
synthetic concept data. Agent execution, Vertex calls, deterministic evaluator results,
tests, ledger hashes, and cloud infrastructure are real. See
[`docs/claims-ledger.md`](docs/claims-ledger.md) for exact claim boundaries.

AI will keep changing. The principle does not: organizations improve when experience becomes
verified shared capability, value remains the measure, and people gain better judgment instead
of better blame metrics.
