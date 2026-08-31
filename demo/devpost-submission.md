# Devpost submission package

## Project overview

**Project name:** GroundTruth

**Elevator pitch:** One team learns. The whole organization gets stronger—and value compounds.

**Thumbnail:** `demo/final/devpost-thumbnail.png`

## Project story

## Inspiration

AI-assisted change velocity is compounding, but organizational value is not guaranteed to follow.
Google Cloud's DORA research captures the paradox: AI adoption is widespread and can improve local
work, yet system-level throughput and stability can still decline when organizational learning,
testing, ownership, and feedback systems do not keep pace.

Most engineering organizations already have issue trackers, postmortems, code scanners, and AI
coding tools. Their deeper problem is institutional: a failure is fixed locally, its causal lesson
remains trapped in one team, and another product pays to relearn it later. GroundTruth asks a
different question: **what if every verified mistake made the whole organization stronger?**

## What it does

GroundTruth is an institutional learning control plane for AI-native engineering. It turns a real
failure into a closed, auditable value loop:

1. reconstruct the evidence and intent;
2. derive a reusable causal signature;
3. proactively search structurally related components and products;
4. design a falsifier and safe control;
5. let deterministic evaluators—not the model—verify the claim;
6. preserve the learning in an append-only SHA-256 chain;
7. attach preventive controls to future changes; and
8. convert the lesson into shared human capability without employee ranking or blame.

The platform includes organization overview, consequence-routed changes, an assurance workspace,
institutional memory, incidents and learning, people and capability, and verified value.

## The flagship proof

We built a blind historical replay around real Kubernetes issue
[#29297](https://github.com/kubernetes/kubernetes/issues/29297). GroundTruth receives the issue and
bounded source from pinned pre-fix commit
`d7150bfaeae642efc08c8ede0ed2ec8ecb340c8e`. The eventual fixing PR, maintainer explanation, and
four-file patch scope are programmatically excluded from the agent packet.

Five Gemini agents independently reconstruct the shared-nested-pointer concurrency mechanism and
expand one reported ConfigMap failure to three sibling exposures: Secret, Downward API, and
GitRepo. Trusted code then executes the structural signature scan and a deterministic interleaving:
Mount A writes its wrapper name, Mount B overwrites the same nested object, and Mount A reads B's
name. A fresh-object control passes.

Only after those findings are frozen does GroundTruth reveal Kubernetes PR
[#29641](https://github.com/kubernetes/kubernetes/pull/29641). The four discovered paths exactly
match the four historical fix paths: **100% precision and 100% recall**.

This is a retrospective blind benchmark—not a claim that we discovered a previously unknown
Kubernetes defect. The later human patch acts as an independent external answer key.

## How we built it

- **Gemini 3.5 Flash on Vertex AI** performs bounded causal reasoning.
- **Google ADK `SequentialAgent`** orchestrates five structured `LlmAgent` specialists: Evidence
  Investigator, Causal Analyst, Pattern Scout, Adversary, and Learning Architect.
- **Google GenAI SDK** provides the model integration.
- **Google Cloud Functions / Cloud Run** host the FastAPI workflow.
- **Firestore Native** persists assurance runs and their evidence-linked results.
- **Pub/Sub** provides an asynchronous incident/evidence trigger.
- **Firebase Hosting** provides the stable public landing URL.
- **Deterministic Python evaluators** own structural matching, the aliasing reproducer, answer-key
  comparison, and ledger verification.

The production evidence run `assure_ef7e404586` completed in
`vertex-adk:gemini-3.5-flash` mode with five structured agent outputs, three trusted proof checks,
an exact 4/4 scope match, and a valid four-event learning chain.

## Challenges

The hardest challenge was preserving a trustworthy boundary between AI reasoning and proof. We
separated the allowed evidence packet from the historical answer key in code and tests, prevented
the model from writing its own verification result, and used deterministic evaluators for every
decisive claim. We also adapted the public runtime after a Google edge-routing anomaly by serving
the same FastAPI application through a verified Google Cloud Function while preserving the
containerized Cloud Run deployment.

## Accomplishments

- A real five-agent ADK workflow—not a simulated trace.
- An externally verifiable blind benchmark with an exact four-path answer-key match.
- A deterministic vulnerable interleaving and passing safe control.
- A real append-only hash chain with no public update/delete operation.
- A persisted production Vertex/ADK run and public multi-page platform.
- 63 passing tests, clean lint, reproducible builds, and zero browser-console errors.
- A human-development model based on capability and shared ownership rather than surveillance.

## What we learned

AI is best treated as an amplifier. Local generation speed creates value only when organizations
also improve their evidence, feedback, memory, verification, ownership, and learning systems.
Agent reasoning becomes far more credible when the product makes uncertainty visible and gives
authority to independent proof. And verified knowledge becomes economically valuable only when it
changes the next decision—not when it merely closes the previous incident.

## What's next

The next step is organization-scale causal retrieval across repositories, incident systems, CI,
and runtime telemetry; policy-as-code controls generated from verified lessons; cross-team
learning propagation; correction and supersession events in a durable ledger; and longitudinal
measurement connecting prevented recurrences to customer and business outcomes.

## Built with tags

Gemini 3.5 Flash; Google ADK; Google GenAI SDK; Vertex AI; Google Cloud Functions; Cloud Run;
Firestore; Pub/Sub; Firebase Hosting; FastAPI; Python; JavaScript; Jinja2; Pydantic; SHA-256;
Playwright; Docker; Cloud Build; Artifact Registry.

## Try it out links

- Live platform: https://groundtruth-507213.web.app
- Public repository: https://github.com/vj68/groundtruth
- Demo video: https://youtu.be/FVfVJJgpaNQ

## Additional info

- **Submitter type:** Individual
- **Country:** India
- **Category:** Taskmaster
- **Organization name:** N/A
- **Project start date:** 08-31-26
- **Repository:** https://github.com/vj68/groundtruth
- **Reproducible testing instructions:** Yes
- **Hosted URL:** https://groundtruth-507213.web.app
- **Testing instructions:** Open the hosted URL and choose “Assurance workspace.” The completed
  production run loads automatically. Verify the sealed evidence protocol, five-agent trace,
  deterministic proof checks, four-component blast radius, 4/4 historical answer-key reveal,
  append-only ledger, future recurrence control, and evidence disclosure. To run locally, follow
  README setup, set `ENABLE_GEMINI=false` for the deterministic continuity path, and run
  `uv run pytest` (63 tests).
- **Google SDKs:** Agent Development Kit (ADK); Google GenAI SDK (`google-genai`)
- **Google Cloud services:** Cloud Run; Firestore; Pub/Sub
- **Architecture diagram:** `demo/deck/rendered/architecture.png`
- **Google AI model:** Gemini 3.5 Flash on Vertex AI global endpoint
- **Bonus content:** https://youtu.be/FVfVJJgpaNQ
- **Startup prize:** Not selected
- **Social post:** blank unless separately published

## Project media

- Video: https://youtu.be/FVfVJJgpaNQ
- Gallery candidates:
  - `demo/deck/rendered/problem.png`
  - `demo/assets/screenshots/01-overview.png`
  - `demo/assets/screenshots/02-assurance-top.png`
  - `demo/deck/rendered/proof.png`
  - `demo/assets/screenshots/04-blast-radius.png`
  - `demo/deck/rendered/architecture.png`
  - `demo/deck/rendered/close.png`
