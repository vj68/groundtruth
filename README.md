# GroundTruth

> **A postmortem remembers what happened. GroundTruth changes what happens next.**

GroundTruth is an executable organizational-learning system for AI-native engineering. It
turns one incident into an evidence-backed failure class, creates a preventive behavioral
control, proves that control against real execution, and automatically applies the verified
lesson to future changes.

**Live demo:** [groundtruth-507213.web.app](https://groundtruth-507213.web.app)

## The 90-second story

An AI-generated retry patch passes all 48 existing tests and human review. In production,
the payment provider captures ₹5,000, its acknowledgement is lost, and the retry uses a new
idempotency key. The customer is charged twice.

Click **Run GroundTruth**. Three specialist agents built with Google ADK:

1. build a causal account grounded in eight evidence objects;
2. generalize the defect into a reusable, implementation-independent invariant; and
3. propose known-bad, corrected, held-out, and safety evaluations.

Then the language model leaves the decision boundary. A deterministic payment-state
simulator proves the learning:

| Future change | Captures | Decision | Why it matters |
|---|---:|---|---|
| Original AI retry patch | 2 | **BLOCK** | Reproduces the incident |
| Corrected stable key | 1 | **PASS** | Proves the fix is viable |
| Exact future recurrence | 2 | **BLOCK** | Prevents repetition |
| Held-out crash + redelivery | 2 | **BLOCK** | Generalizes beyond matching code |
| Safe redelivery change | 1 | **PASS** | Proves the gate does not freeze innovation |

The timeless invariant is simple:

```text
A logical payment operation must produce at most one successful capture per order.
```

## Why this is different

Incident tools store prose. Static analyzers match known patterns. GroundTruth closes the
learning loop:

```text
incident → evidence → causal model → failure class → executable invariant
         → known-bad/corrected proof → held-out evaluation → durable memory
```

The model interprets and generalizes; real behavior supplies truth. A lesson is never marked
verified merely because an LLM says it is correct.

## Built with Google Cloud

- **Gemini 3.5 Flash** on Vertex AI's global endpoint for structured forensic synthesis,
  generalization, and verification design.
- **Google Agent Development Kit 2.8** with a real `SequentialAgent` team and structured
  Pydantic outputs stored in ADK session state.
- **Cloud Run** for the public application and workflow runtime, cost-capped at 0–2 instances.
- **Firebase Hosting** for the stable public front door and full-service Cloud Run rewrite.
- **Firestore Native** for durable runs and verified organizational memory.
- **Pub/Sub** for asynchronous incident ingestion.
- **Cloud Build + Artifact Registry** for reproducible deployment.

The runtime service account has only `Vertex AI User`, `Cloud Datastore User`, and
`Pub/Sub Publisher` roles.

## Safety and grounding

- Agent inputs contain a closed evidence packet with stable evidence IDs.
- The forensic prompt forbids unsupported people, systems, timestamps, code, and impact.
- Facts and unknowns are separate structured fields.
- Causal claims expose their evidence citations.
- The evaluator is deterministic and isolated from model output.
- Certification requires both known-bad rejection and corrected-path acceptance.
- A held-out variant tests causal generalization; a safe change tests overblocking.
- Gemini failures invoke a clearly labeled grounded continuity path, never a fake model claim.

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

Open `http://127.0.0.1:8000`. To exercise the complete deterministic experience without a
Vertex call, set `ENABLE_GEMINI=false`. The UI labels that execution
`grounded-local-fallback`.

Run all verification:

```bash
uv run ruff check app tests
uv run pytest
uv run python -m app.cli evaluate
```

Expected: **57 tests pass** and all five evaluation cases are verified.

## Deploy

The checked-in `Dockerfile` is the deployment source. This is the cost-capped deployment
shape used by the live demo:

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
  --set-env-vars='GOOGLE_CLOUD_LOCATION=global,MODEL=gemini-3.5-flash,ENABLE_GEMINI=true,USE_VERTEX=true,USE_FIRESTORE=true'
```

## Repository map

```text
app/agents/       ADK specialist team, prompts, structured contracts
app/lab/          deterministic payment provider and evaluation scenarios
app/workflow.py   certification and future-change learning loop
app/main.py       FastAPI UI, API, and Pub/Sub push entrypoint
firebase.json     stable Hosting front door rewritten to Cloud Run
fixtures/         synthetic incident evidence packet
templates/        evidence-first demo interface
tests/            legacy suite, evaluator, workflow, and web checks
docs/             architecture, demo script, and submission evidence
```

## Evidence and disclosure

All company, customer, payment-provider, order, code-change, and incident data are synthetic.
Agent execution, Gemini calls, ADK orchestration, test execution, cloud infrastructure, and
evaluation outcomes are real. The exact limits of every claim are documented in
[`docs/claims-ledger.md`](docs/claims-ledger.md).

See also:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/demo-script.md`](docs/demo-script.md)
- [`docs/submission.md`](docs/submission.md)
- [`BLOCKERS.md`](BLOCKERS.md)

## The larger idea

AI increases the rate of change. GroundTruth makes the rate of learning compound with it.
Its principle is independent of today's models and tools: organizations improve when
experience becomes verified capability, value creation remains the measure, and people gain
better judgment instead of better blame metrics.
