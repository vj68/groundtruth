# Submission material

## Project name

GroundTruth

## Tagline

One team learns. The whole organization gets stronger.

## One-line pitch

GroundTruth turns every verified engineering failure into organization-wide memory,
preventive controls, and human capability—so known mistakes do not recur silently in the AI
era.

## Short description

AI accelerates software output faster than organizations convert experience into judgment.
GroundTruth is an institutional learning control plane: five Google ADK agents reconstruct a
failure's causal signature, proactively search related systems, design a falsifier, and create
an intervention package; deterministic evaluators verify the evidence before an append-only
ledger applies the lesson to future changes.

## The proof

GroundTruth performs a blind historical replay of real Kubernetes issue #29297. Agents receive
the original issue and source before the fix; the later merged PR is sealed. The system derives
the shared-nested-pointer concurrency failure, finds ConfigMap, Secret, Downward API, and GitRepo,
and proves the aliasing with a deterministic interleaving. Only then does it reveal Kubernetes PR
#29641—the independent findings match its four-file scope exactly.

The verified lesson becomes hash-linked institutional memory, a future shared-template control,
a blocked synthetic Northstar PR, and a developmental teach-back.

## Problem

- AI-assisted change velocity is compounding.
- Postmortems and issue trackers preserve symptoms but rarely operationalize causal knowledge.
- Fixes remain local even when the same failure class exists across components, teams, or
  products.
- One team learns through pain; another team pays to learn the same lesson again.
- Organizations can respond with more process or employee scoring, neither of which creates
  durable capability.

## Solution

GroundTruth creates a closed learning loop:

1. reconstruct intent and evidence;
2. derive a causal failure class and invariant;
3. search structural siblings across the organization;
4. prove exposures and safe controls using trusted evaluators;
5. preserve provenance in an append-only hash-linked ledger;
6. attach preventive controls to future changes; and
7. convert the lesson into shared ownership and human development.

## Why it is innovative

- **Causal propagation, not keyword matching:** the full structural mechanism must match.
- **External answer-key benchmark:** judges need not trust our narrative; the later Kubernetes
  patch independently validates scope.
- **Models propose, evidence decides:** Gemini cannot write the verification result.
- **Learning acts on the future:** every verified lesson creates enforceable controls and
  capability interventions.
- **Immutable institutional history:** corrections append; earlier evidence and reasoning are
  never silently overwritten.
- **Human growth without surveillance:** measure knowledge coverage and transfer, not employee
  intelligence or blame.

## Google technology

- Gemini 3.5 Flash on Vertex AI;
- Google Agent Development Kit 2.8 with five structured specialist agents;
- Cloud Run;
- Firebase Hosting;
- Firestore Native;
- Pub/Sub;
- Cloud Build and Artifact Registry.

## Responsible AI

- The fixing PR is programmatically excluded from the agent packet.
- Agent outputs are bounded, typed, and attributable.
- A deterministic evaluator decides structural equivalence and the interleaving result.
- Candidate lessons remain non-binding until verified.
- Synthetic and real evidence are labeled separately.
- The product refuses individual competence scoring and punitive inference.
- It does not claim to have discovered a new Kubernetes defect.
- It does not claim universal prevention or business ROI from one benchmark.

## What is real vs synthetic

The Kubernetes issue, code paths, commits, and fixing PR are real public evidence. Gemini calls,
ADK execution, deterministic proof, tests, hash chain, APIs, browser experience, and cloud
infrastructure are real. Northstar Engineering, its metrics, and future PR `NSTR-204` are
synthetic concept data and labeled as such.

## Judging anchors

- **Impact:** one team's verified lesson becomes protection and capability for the whole
  organization.
- **Technical execution:** genuine five-agent ADK orchestration, sealed evidence boundary,
  deterministic proof, cryptographic ledger, persistent cloud workflow, and responsive product.
- **Innovation:** independently recover and verify causal blast radius, then propagate it into
  future decisions.
- **Responsible AI:** evidence before confidence, explicit uncertainty, proof/model separation,
  no surveillance, and honest claim boundaries.
- **Demo clarity:** one real issue, three hidden siblings, one 4/4 answer-key reveal, one permanent
  learning chain.

## Suggested assets

1. Organization overview screenshot with the Kubernetes benchmark and propagation flow.
2. Completed assurance screenshot showing 4/4, proof checks, and answer-key reveal.
3. Learning ledger screenshot with the verified hash chain.
4. Two-minute narrated walkthrough from `docs/demo-script.md`.
5. Architecture diagram generated from `docs/architecture.md`.
6. Public repository and Firebase Hosting URL.

## Closing line

AI will keep changing. GroundTruth's principle is timeless: an excellent organization turns
experience into verified shared capability, protects value, and helps its people develop the
judgment to build better systems next time.
