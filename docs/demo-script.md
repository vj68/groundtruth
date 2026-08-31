# Judge demo script

Target duration: 90 seconds, with a pre-warmed completed run available as backup.

## 0:00–0:15 — The contradiction

“This AI-generated reliability patch passed 48 tests and human review. But when the payment
provider captured the money and its acknowledgement was lost, the retry used a new identity.
One ₹5,000 order became two successful captures.”

Point to the dark ledger card. Do not open with architecture.

## 0:15–0:25 — The thesis

“A postmortem would record this. GroundTruth makes it harder to happen again. It converts one
experience into an executable organizational capability.”

Click **Run GroundTruth**.

## 0:25–0:48 — Agents with boundaries

“Three Google ADK agents investigate cited evidence, generalize the defect, and design an
evaluation. Gemini 3.5 Flash is doing the interpretation—but it is not allowed to declare
the change safe.”

Point to the causal chain, evidence IDs, failure class, and invariant.

## 0:48–1:12 — The proof

“The isolated evaluator reproduces real state transitions. The original patch is blocked.
The corrected stable-key path passes. Now the important part: a held-out consumer-crash and
queue-redelivery implementation is also blocked, even though it looks different.”

Point to capture counts, not just red/green labels.

## 1:12–1:25 — No innovation tax

“A safe redelivery change still passes. GroundTruth learns the behavioral boundary, not a
regex over yesterday's code.”

## 1:25–1:30 — Close

“AI increases the rate of change. GroundTruth makes the rate of learning compound with it:
evidence before confidence, behavior before prose, growth before blame.”

## If Gemini latency is high

Keep the current run visible for up to two minutes; the interface continues polling. If the
venue network is unreliable, show a previously completed Firestore-backed run and then run
`uv run python -m app.cli evaluate` locally. Never imply the continuity path was Gemini; the
run's mode label states exactly what executed.

## Likely judge questions

**Is the incident real?** No. The scenario and company data are transparently synthetic.
The Gemini/ADK calls, evaluator execution, tests, persistence, and cloud deployment are real.

**Is this just better test generation?** No. Tests are one possible enforcement artifact.
The product model is evidence → failure class → behavioral invariant → certification →
durable memory → future gate.

**Could the LLM fake the result?** No. It cannot write `ScenarioResult.decision`. The
deterministic provider simulator derives the decision from actual capture state.

**Why is the held-out case meaningful?** It changes the mechanism from timeout retry to queue
redelivery after a crash while preserving the causal structure: an ambiguous successful
external side effect followed by a retry under a different identity.

**How does this develop people?** Reviewers see evidence-linked causal reasoning, explicit
unknowns, invariant design, and counterexample-based proof. The product improves shared
judgment; it does not score individual “AI competence.”
