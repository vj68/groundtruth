# Submission material

## Project name

GroundTruth

## Tagline

A postmortem remembers what happened. GroundTruth changes what happens next.

## Short description

GroundTruth turns production incidents into verified executable defenses. A Google ADK team
uses Gemini 3.5 Flash to investigate evidence, generalize a failure class, and design an
evaluation; a deterministic truth gate proves the lesson before Firestore applies it to
future changes.

## Track

Taskmaster.

## Problem

AI accelerates software output faster than organizations convert experience into judgment.
Postmortems decay into prose, action items become reminders, and the next AI-generated change
can repeat the same causal failure through different code.

## Solution

GroundTruth converts an incident into cited causal knowledge, a reusable behavioral
invariant, and an executable gate. It certifies against known-bad and corrected behavior,
tests a held-out variant, and tests a safe change to avoid overblocking.

## Google technology

Gemini 3.5 Flash, Vertex AI, Google ADK, Cloud Run, Firebase Hosting, Firestore, Pub/Sub,
Cloud Build, and Artifact Registry.

## What is real vs synthetic

The duplicate-payment organization and incident are synthetic and labeled on the first
screen. The agent execution, model calls, ADK state handoff, evaluator, tests, persistence,
deployment, and results are real.

## Suggested submission assets

1. Hero screenshot with the incident and double-charge ledger.
2. Completed-run screenshot showing the invariant and five evaluation rows.
3. Architecture diagram from `docs/architecture.md`.
4. 90-second narrated demo following `docs/demo-script.md`.
5. Public GitHub repository and live Firebase Hosting URL backed by Cloud Run.

## Judging anchors

- **Impact:** organizational learning compounds instead of incident prose accumulating.
- **Technical execution:** genuine structured multi-agent ADK workflow with deterministic
  proof and real cloud persistence.
- **Innovation:** learned behavioral boundary catches a causally equivalent held-out variant.
- **Responsible AI:** evidence citations, explicit unknowns, model/proof separation,
  overblocking test, and synthetic-data disclosure.
- **Demo clarity:** visible contradiction, one button, five inspectable outcomes.
