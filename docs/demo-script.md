# Judge demo script

Target duration: 2 minutes. Keep a completed Firestore-backed run available as the guaranteed
path; optionally start a fresh run to demonstrate live progress.

## 0:00–0:20 — The organizational contradiction

Open **Organization Overview**.

“AI-assisted change velocity is up 38%, but verified value is up only 9%. The larger problem is
that organizations still pay repeatedly to learn the same engineering lesson. Postmortems
remember; they do not reliably change every future decision.”

Point to **Known lessons enforced**, **Silent recurrences**, and the propagation flow.

## 0:20–0:35 — The product thesis

“GroundTruth turns every verified failure into organization-wide memory, protection, and human
capability. One team learns; the whole organization gets stronger.”

Open **Blind replay**.

## 0:35–0:55 — Real evidence and a fair test

“This is not a fabricated incident. It is Kubernetes issue #29297. Agents receive the original
issue and source before the fix. The eventual merged PR, the maintainer discussion, and its
four-file scope are sealed as an answer key.”

Point to the two protocol columns and pinned commit. Click **Start blind replay** if latency and
network conditions permit.

## 0:55–1:20 — Agents reason; evaluators prove

“Five Google ADK agents separate evidence, derive the nested-pointer concurrency mechanism,
search structural siblings, design a falsifier, and create an institutional response. Gemini
does the interpretation. It cannot declare the evidence verified.”

Point to:

- the five-agent trace;
- ConfigMap as the observed component;
- Secret, Downward API, and GitRepo as proactive sibling exposures; and
- the vulnerable interleaving where Mount A changes from `wrapped_config-a` to
  `wrapped_config-b`.

“Trusted deterministic code makes every proof decision. The fresh-object control passes.”

## 1:20–1:40 — Reveal the answer key

Scroll to **Historical answer key unsealed**.

“Only now do we reveal Kubernetes PR #29641. GroundTruth independently found exactly the four
paths humans later changed: 100% precision, 100% recall. This is a retrospective benchmark, not
a claim of discovering a new Kubernetes bug.”

Pause on the side-by-side exact match. This is the central “aha.”

## 1:40–1:58 — Institutional memory acts

“The result does not die in a report. GroundTruth appends four hash-linked learning events,
creates a shared mutable-template control, blocks a future Northstar PR carrying the same
causal pattern, and creates a Go pointer-ownership teach-back.”

Point to the ledger, `NSTR-204`, and the capability action.

## 1:58–2:00 — Close

“AI increases the rate of change. GroundTruth makes the rate of verified learning compound with
it.”

## Demo reliability

- Start with the latest completed run automatically loaded from Firestore.
- A fresh Gemini run normally takes tens of seconds; the UI polls and shows each stage.
- `ENABLE_GEMINI=false` exercises the complete grounded continuity path with identical trusted
  evaluators and a transparent `grounded-local-fallback` label.
- Never imply a fallback run used Gemini.
- Never claim the synthetic Northstar future PR is a real production incident.

## Likely judge questions

### Did GroundTruth discover a new Kubernetes bug?

No. It performs a blind retrospective replay at a pre-fix commit. The later merged patch is an
independent answer key proving the system recovered the correct causal scope.

### Isn't this just code search?

No. Text search can locate a symbol; GroundTruth requires a complete causal signature, executes
a falsifier and safe control, verifies against external evidence, records provenance, creates a
future control, and connects the lesson to organizational capability and value.

### Could the LLM fake the 4/4 result?

No. The agent proposes candidates. Deterministic code scans the bounded source packet, executes
the nested-object interleaving, computes precision/recall against the withheld paths, and
verifies the ledger chain.

### Why use a historical issue?

Because novelty is not a trustworthy evaluation metric. A historical fix gives an independent,
public answer key. It lets judges verify the product's reasoning without trusting our narrative.

### Why an append-only ledger?

Institutional memory must preserve who believed what, based on which evidence, and how the
lesson evolved. Corrections append; history is not silently rewritten.

### How does this develop people?

GroundTruth turns verified cases into teach-backs, practice labs, pairing, and shared ownership.
It measures knowledge coverage and transfer—not individual intelligence, blame, or “AI scores.”
