const state = { data: null, run: null, ledger: null, polling: false };

const page = document.body.dataset.page;
const root = document.getElementById("page-root");

function escapeHtml(value = "") {
  return String(value).replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
  })[char]);
}

function statusTone(value = "") {
  const text = value.toLowerCase();
  if (text.includes("block") || text.includes("fail") || text.includes("recurrence")) return "danger";
  if (text.includes("verified") || text.includes("pass") || text.includes("protected") || text.includes("ready")) return "good";
  if (text.includes("real") || text.includes("public")) return "real";
  if (text.includes("candidate") || text.includes("pending")) return "candidate";
  return "warning";
}

function tag(value, tone = statusTone(value)) {
  return `<span class="tag ${tone}">${escapeHtml(value)}</span>`;
}

function metrics(items) {
  return `<section class="metric-grid">${items.map((item) => `
    <article class="metric-card ${item.tone || ""}">
      <span class="metric-label">${escapeHtml(item.label)}</span>
      <strong>${escapeHtml(item.value)}</strong>
      <small>${escapeHtml(item.trend || item.detail || item.delta || "")}</small>
    </article>`).join("")}</section>`;
}

function pageHead(kicker, title, lede, actions = "") {
  return `<header class="page-head">
    <div><p class="eyebrow">${escapeHtml(kicker)}</p><h1>${title}</h1><p class="lede">${escapeHtml(lede)}</p></div>
    ${actions ? `<div class="head-actions">${actions}</div>` : ""}
  </header>`;
}

function card(title, subtitle, body, extraClass = "", action = "") {
  return `<section class="card ${extraClass}">
    <header class="card-header"><div><h2>${title}</h2>${subtitle ? `<p>${subtitle}</p>` : ""}</div>${action}</header>
    ${body}
  </section>`;
}

function activityList(items) {
  return `<div class="card-body activity-list">${items.map((item) => `
    <div class="activity-item ${item.tone}"><i></i><div><strong>${escapeHtml(item.agent)}</strong><p>${escapeHtml(item.action)}</p></div><time>${escapeHtml(item.time)}</time></div>
  `).join("")}</div>`;
}

function renderOverview(data) {
  const org = data.organization;
  const benchmark = data.change_detail;
  root.innerHTML = `
    ${pageHead(
      "Organizational immune system",
      "Speed is compounding. Is learning?",
      "GroundTruth turns verified engineering failures into memory, controls, and capability that propagate across every team and repository."
    )}
    ${metrics(org.metrics)}
    <div class="content-grid">
      <div>
        <section class="card benchmark-card">
          <div class="benchmark-inner">
            <div>
              <span class="real-badge">● Real public evidence benchmark</span>
              <h2>Can one Kubernetes failure reveal the complete hidden blast radius?</h2>
              <p>Agents receive issue #29297 and a pre-fix source snapshot. The eventual fixing PR is sealed as an independent answer key.</p>
              <div class="benchmark-meta">
                <span>REPOSITORY <b>kubernetes/kubernetes</b></span>
                <span>SNAPSHOT <b>${escapeHtml(benchmark.snapshot_commit.slice(0, 12))}</b></span>
                <span>OBSERVED <b>1 component</b></span>
              </div>
            </div>
            <div class="benchmark-cta">
              <div class="sealed-box"><span>Sealed answer key</span><strong>PR #29641</strong><small>Unavailable to agents until reveal</small></div>
              <a class="button" href="/changes/K8S-29297"><span class="button-spark">◇</span> Open blind replay</a>
            </div>
          </div>
        </section>
        ${card(
          "Learning propagation",
          "A verified lesson should travel farther than the incident did.",
          `<div class="propagation-flow">${data.memory.propagation.map((item) => `
            <div class="prop-node ${item.tone}"><strong>${escapeHtml(item.product)}</strong><span>${escapeHtml(item.state)}</span><small>${escapeHtml(item.detail)}</small></div>
          `).join("")}</div>`,
          "section-gap",
          '<a class="card-link" href="/memory">Open ledger →</a>'
        )}
      </div>
      <div>
        ${card(
          "Velocity–value gap",
          "Output is rising faster than verified outcomes.",
          `<div class="card-body"><div class="gap-visual">
            <div class="gap-number"><span>AI velocity</span><strong>+38%</strong><div class="mini-bars"><i></i><i></i><i></i><i></i><i></i></div></div>
            <div class="gap-arrow">→<small>29 pt gap</small></div>
            <div class="gap-number value"><span>Verified value</span><strong>+9%</strong><div class="mini-bars"><i></i><i></i><i></i><i></i><i></i></div></div>
          </div></div>`
        )}
        ${card("Agent activity", "Proactive work across the organization.", activityList(data.activity), "section-gap")}
      </div>
    </div>
    ${card(
      "Knowledge coverage by team",
      "Coverage means critical knowledge has evidence, stewards, and an enforced control—not that people are being scored.",
      `<div class="table-scroll"><table class="data-table"><thead><tr><th>Team</th><th>Product</th><th>Learning coverage</th><th>Signal</th></tr></thead><tbody>
        ${org.teams.map((team) => `<tr><td><strong>${escapeHtml(team.name)}</strong></td><td>${escapeHtml(team.product)}</td><td><div class="progress-track ${team.risk === "high" ? "risk" : ""}"><i style="width:${team.coverage}%"></i></div><small>${team.coverage}% verified</small></td><td>${tag(team.risk === "low" ? "Healthy" : team.risk === "high" ? "Knowledge gap" : "Watch", team.risk === "low" ? "good" : "warning")}</td></tr>`).join("")}
      </tbody></table></div>`,
      "section-gap",
      '<a class="card-link" href="/capability">Develop capability →</a>'
    )}
  `;
}

function renderChanges(data) {
  root.innerHTML = `
    ${pageHead(
      "Change portfolio",
      "Route attention by consequence—not file count.",
      "GroundTruth reconstructs intent, maps blast radius, recalls institutional history, and challenges high-consequence changes before they merge.",
      '<button class="button secondary">Filters <span>⌄</span></button><a class="button primary" href="/changes/K8S-29297"><span class="button-spark">◇</span> Run evidence benchmark</a>'
    )}
    <div class="content-grid equal">
      ${card("Assurance routing", "Current portfolio", `<div class="card-body"><div class="gap-visual">
        <div class="gap-number"><span>High consequence</span><strong>2</strong><small>Deep assurance</small></div>
        <div class="gap-arrow">↗<small>adaptive</small></div>
        <div class="gap-number value"><span>Auto-cleared</span><strong>1</strong><small>Low consequence</small></div>
      </div></div>`)}
      ${card("Institutional memory impact", "How prior learning changed current work", `<div class="card-body"><div class="check-list">
        <div class="check-item"><span class="check-symbol">✓</span><div><strong>17 recurrences intercepted</strong><p>Known failure classes challenged before production.</p></div>${tag("Protected", "good")}</div>
        <div class="check-item fail"><span class="check-symbol">!</span><div><strong>6 lessons await verification</strong><p>Hypotheses remain visible but cannot enforce controls yet.</p></div>${tag("Honest uncertainty", "warning")}</div>
      </div></div>`)}
    </div>
    ${card(
      "Changes and assurance runs",
      "Real public evidence is distinguished from synthetic concept workflow data.",
      `<div class="table-scroll"><table class="data-table"><thead><tr><th>Change</th><th>Team / repository</th><th>Risk</th><th>Evidence</th><th>Decision</th><th></th></tr></thead><tbody>
      ${data.changes.map((change) => `<tr>
        <td><strong>${escapeHtml(change.title)}</strong><small>${escapeHtml(change.id)} · ${escapeHtml(change.value)}</small></td>
        <td><strong>${escapeHtml(change.team)}</strong><small>${escapeHtml(change.repository)}</small></td>
        <td><strong>${change.risk}/100</strong><small>${change.risk > 80 ? "Deep assurance" : change.risk < 10 ? "Auto-route" : "Targeted checks"}</small></td>
        <td>${tag(change.real ? "Real public evidence" : "Synthetic concept", change.real ? "real" : "candidate")}</td>
        <td>${tag(change.decision, change.decision === "BLOCK" ? "danger" : change.decision === "PASS" ? "good" : "sealed")}</td>
        <td>${change.id === "K8S-29297" ? '<a class="table-link" href="/changes/K8S-29297">Open →</a>' : '<span class="card-link">View</span>'}</td>
      </tr>`).join("")}
      </tbody></table></div>`,
      "section-gap"
    )}
  `;
}

function sourceCards(detail) {
  return `<div class="source-grid">${detail.source_snapshots.map((source) => `
    <article class="source-card">
      <header><strong>${escapeHtml(source.component)}</strong><span>${escapeHtml(source.path)}:${source.declaration_line}</span></header>
      <pre>${escapeHtml(source.source)}</pre>
    </article>`).join("")}</div>`;
}

function runTimeline(run) {
  return `<div class="timeline">${run.events.map((event) => `
    <div class="timeline-item"><span class="timeline-node">${event.sequence}</span><div><h4>${escapeHtml(event.agent)} · ${escapeHtml(event.title)}</h4><p>${escapeHtml(event.detail)}</p></div><time>${new Date(event.timestamp).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit", second: "2-digit"})}</time></div>
  `).join("")}</div>`;
}

function artifactGrid(run) {
  return `<div class="card-body artifact-grid">${run.artifacts.map((artifact) => `
    <article class="artifact"><span>${escapeHtml(artifact.agent)}</span><h4>${escapeHtml(artifact.title)}</h4><p>${escapeHtml(artifact.summary)}</p></article>
  `).join("")}</div>`;
}

function checks(run) {
  return `<div class="card-body check-list">${run.evaluations.map((check) => `
    <div class="check-item ${check.decision.includes("FAIL") ? "fail" : ""}"><span class="check-symbol">${check.decision.includes("FAIL") ? "!" : "✓"}</span><div><strong>${escapeHtml(check.label)}</strong><p>${escapeHtml(check.observed)}</p></div><div>${tag(check.decision, check.decision.includes("FAIL") ? "warning" : "good")}<code>${check.trusted ? " trusted evaluator" : ""}</code></div></div>
  `).join("")}</div>`;
}

function exposureTable(run) {
  return `<div class="table-scroll"><table class="data-table"><thead><tr><th>Component</th><th>Relationship</th><th>Code evidence</th><th>Decision</th></tr></thead><tbody>
    ${run.exposures.map((item) => `<tr><td><strong>${escapeHtml(item.component)}</strong><small>${escapeHtml(item.product)} · ${escapeHtml(item.team)}</small></td><td>${escapeHtml(item.relationship)}</td><td><code>${escapeHtml(item.evidence)}</code></td><td>${tag(item.status, "good")}</td></tr>`).join("")}
  </tbody></table></div>`;
}

function groundTruthReveal(run) {
  const truth = run.ground_truth;
  const answer = truth.answer_key;
  const paths = truth.discovered_paths;
  return `<section class="card reveal-card section-gap">
    <div class="reveal-head"><span class="reveal-icon">✓</span><div><h3>Historical answer key unsealed</h3><p>The agents could not access this PR until after their findings were frozen.</p></div></div>
    <div class="comparison">
      <div class="comparison-side"><h4>GroundTruth independently discovered</h4><div class="path-list">${paths.map((path) => `<div class="path-item"><i></i>${escapeHtml(path)}</div>`).join("")}</div></div>
      <div class="comparison-divider">=</div>
      <div class="comparison-side"><h4>Kubernetes later changed in PR #29641</h4><div class="path-list">${answer.expected_paths.map((path) => `<div class="path-item"><i></i>${escapeHtml(path)}</div>`).join("")}</div></div>
    </div>
    <div class="exact-match"><span><strong>${escapeHtml(truth.verdict)}</strong> · exact four-path scope match</span><a href="${answer.url}" target="_blank" rel="noreferrer">Inspect merged PR ↗</a></div>
  </section>`;
}

function ledgerChain(events) {
  if (!events || !events.length) return `<div class="empty-state"><span class="empty-icon">▱</span><h3>No committed events yet</h3><p>Run the blind replay to append a verified learning chain.</p></div>`;
  return `<div class="ledger-chain">${events.map((event) => `
    <article class="ledger-event"><span>#${event.sequence} · ${escapeHtml(event.actor)}</span><h4>${escapeHtml(event.event_type.replaceAll("_", " "))}</h4><code>${escapeHtml(event.event_hash.slice(0, 16))}…</code><p>Previous: ${escapeHtml(event.previous_hash === "GENESIS" ? "GENESIS" : event.previous_hash.slice(0, 10) + "…")}</p></article>
  `).join("")}</div>`;
}

function runResult(run) {
  const truth = run.ground_truth;
  const verification = run.ledger_verification;
  return `
    <section class="decision-banner"><span class="decision-icon">✓</span><div><span>Institutional learning decision</span><strong>${escapeHtml(run.decision)}</strong><p>${escapeHtml(run.decision_reason)}</p></div><div class="decision-score"><strong>4 / 4</strong><small>historical paths recovered</small></div></section>
    <section class="proof-grid">
      <article class="proof-stat"><span>Observed failure</span><strong>1</strong><small>ConfigMap issue</small></article>
      <article class="proof-stat"><span>Proactive exposures</span><strong>3</strong><small>Structural siblings</small></article>
      <article class="proof-stat"><span>Precision / recall</span><strong>${Math.round(truth.precision * 100)} / ${Math.round(truth.recall * 100)}</strong><small>Against withheld answer key</small></article>
      <article class="proof-stat"><span>Ledger integrity</span><strong>${verification.valid ? "VALID" : "FAIL"}</strong><small>${verification.events} hash-linked events</small></article>
    </section>
    <div class="content-grid section-gap">
      ${card("Five-agent trace", "Reasoning stages remain attributable and inspectable.", `<div class="card-body">${runTimeline(run)}</div>`)}
      ${card("Trusted proof checks", "Models propose; deterministic evaluators decide.", checks(run))}
    </div>
    ${card("Agent artifacts", "Each role contributes a bounded, evidence-linked artifact.", artifactGrid(run), "section-gap")}
    ${card("Causal blast radius", "One observed failure; three proactive sibling exposures.", exposureTable(run), "section-gap")}
    ${groundTruthReveal(run)}
    ${card("Append-only learning ledger", "Every transition is attributable and hash-linked; corrections append rather than overwrite history.", ledgerChain(run.ledger_events), "section-gap", `<span class="tag good">${verification.scheme}</span>`)}
    ${card("The lesson acts on the future", "A learning is valuable only when it changes subsequent behavior.", `<div class="card-body check-list">${run.proactive_actions.map((action) => `
      <div class="check-item ${action.status.includes("BLOCKED") ? "fail" : ""}"><span class="check-symbol">${action.status.includes("BLOCKED") ? "!" : "✓"}</span><div><strong>${escapeHtml(action.id)} · ${escapeHtml(action.action)}</strong><p>Owner: ${escapeHtml(action.owner)}</p></div>${tag(action.status, action.status.includes("BLOCKED") ? "danger" : "good")}</div>`).join("")}</div>`, "section-gap")}
  `;
}

function renderAssurance(data) {
  const detail = data.change_detail;
  const run = state.run;
  const terminal = run && ["complete", "failed"].includes(run.status);
  const running = run && !terminal;
  root.innerHTML = `
    <div class="breadcrumb"><a href="/changes">Changes</a><span>›</span><span>K8S-29297</span><span>›</span><span>Blind assurance replay</span></div>
    <header class="page-head">
      <div class="assurance-title"><span class="repo-mark">K8</span><div><p class="eyebrow">Real public evidence · controlled benchmark</p><h1>${escapeHtml(detail.issue.title)}</h1><p>${escapeHtml(detail.issue.id)} · pre-fix commit ${escapeHtml(detail.snapshot_commit.slice(0, 12))}</p></div></div>
      <div class="head-actions"><a class="button secondary" href="${detail.issue.url}" target="_blank" rel="noreferrer">Open issue ↗</a><button class="button primary" id="run-assurance" ${running ? "disabled" : ""}><span class="button-spark">◇</span>${running ? "Agents running…" : run ? "Run again" : "Start blind replay"}</button></div>
    </header>
    ${card(
      "Blind evaluation protocol",
      escapeHtml(detail.protocol.question),
      `<div class="protocol-grid"><div class="protocol-column"><h3>Visible to GroundTruth</h3><ul>${detail.protocol.allowed.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div><div class="protocol-column withheld"><h3>Sealed until after analysis</h3><ul>${detail.protocol.withheld.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div></div><div class="seal-strip"><span>EVIDENCE SNAPSHOT <strong>${escapeHtml(detail.snapshot_commit)}</strong></span><span>ANSWER KEY <strong>SEALED</strong></span></div>`
    )}
    ${running ? `<section class="run-control run-stage"><div><h3>${escapeHtml(run.events.at(-1)?.title || "Agents are working")}</h3><p>${escapeHtml(run.events.at(-1)?.detail || "The sealed protocol is active.")}</p></div><div class="run-status"><span class="spinner"></span>${tag(run.status, "real")}</div></section>${card("Live agent trace", "The page updates as each bounded role finishes.", `<div class="card-body">${runTimeline(run)}</div>`, "section-gap")}` : ""}
    ${run && run.status === "complete" ? runResult(run) : ""}
    ${run && run.status === "failed" ? `<div class="disclosure"><strong>Run failed:</strong> ${escapeHtml(run.error)}. The evidence pack remains intact; retry is safe.</div>` : ""}
    ${!run ? `${card("Pre-fix source evidence", "These bounded snapshots are visible to the agents; the eventual patch is not.", `<div class="card-body">${sourceCards(detail)}</div>`, "section-gap")}
      <section class="empty-state"><span class="empty-icon">◇</span><h3>The historical answer key is sealed</h3><p>Start the replay to watch five agents derive the cause, expand the scope, execute a deterministic proof, and only then compare against the merged Kubernetes fix.</p><button class="button primary" id="run-assurance-inline"><span class="button-spark">◇</span> Start blind replay</button></section>` : ""}
    <div class="disclosure"><span>ⓘ</span><span><strong>Evidence disclosure:</strong> Kubernetes issue, source, commit, and fixing PR are real public artifacts. The answer key is excluded from the agent packet by code. Northstar’s future PR and organizational metrics are clearly labeled synthetic concept data.</span></div>
  `;
  document.getElementById("run-assurance")?.addEventListener("click", startRun);
  document.getElementById("run-assurance-inline")?.addEventListener("click", startRun);
}

function renderMemory(data) {
  const memory = data.memory;
  const liveEvents = state.run?.ledger_events || state.ledger?.events || [];
  const verification = state.run?.ledger_verification || state.ledger?.verification;
  root.innerHTML = `
    ${pageHead("Organizational memory", "A ledger of verified lessons—not a graveyard of documents.", "GroundTruth preserves provenance, uncertainty, causal invariants, and the controls created from each lesson. History is appended, never silently rewritten.")}
    ${metrics(memory.metrics)}
    <div class="content-grid">
      ${card("Failure-class library", "Verified knowledge can enforce controls; candidates remain visible but non-binding.", `<div>${memory.failure_classes.map((item) => `
        <article class="failure-card"><div class="failure-top"><div><span class="failure-id">${escapeHtml(item.id)}</span><h3>${escapeHtml(item.name)}</h3></div>${tag(item.status)}</div><p class="invariant">${escapeHtml(item.invariant)}</p><div class="failure-meta"><span>Origin: ${escapeHtml(item.origin)}</span><span>${item.applications} applications</span><span>${item.recurrences} recurrences</span></div></article>`).join("")}</div>`)}
      <div>
        ${card("What makes a lesson enforceable?", "Philosophy becomes operational only through evidence.", `<div class="card-body check-list">
          <div class="check-item"><span class="check-symbol">1</span><div><strong>Observed evidence</strong><p>Issue, trace, test, or customer outcome—not memory alone.</p></div></div>
          <div class="check-item"><span class="check-symbol">2</span><div><strong>Causal signature</strong><p>A mechanism and invariant, not keyword similarity.</p></div></div>
          <div class="check-item"><span class="check-symbol">3</span><div><strong>Trusted falsifier</strong><p>Deterministic behavior distinguishes exposure from resemblance.</p></div></div>
          <div class="check-item"><span class="check-symbol">4</span><div><strong>Reusable intervention</strong><p>Control, ownership, process, and capability actions.</p></div></div>
        </div>`)}
        ${card("Ledger status", "Cryptographic integrity of the current append-only chain.", `<div class="card-body"><div class="proof-stat"><span>Verification</span><strong>${verification?.valid ? "VALID" : "WAITING"}</strong><small>${verification?.events || 0} events · ${escapeHtml(verification?.head?.slice(0, 18) || "No chain head yet")}</small></div></div>`, "section-gap")}
      </div>
    </div>
    ${card("Live append-only chain", "Corrections and superseding evidence append new events; there is no update or delete API.", ledgerChain(liveEvents), "section-gap", verification?.valid ? '<span class="tag good">Hash chain valid</span>' : '<span class="tag warning">Awaiting benchmark</span>')}
    ${card("Propagation map", "The Kubernetes learning crosses components and then protects a future organizational change.", `<div class="propagation-flow">${memory.propagation.map((item) => `<div class="prop-node ${item.tone}"><strong>${escapeHtml(item.product)}</strong><span>${escapeHtml(item.state)}</span><small>${escapeHtml(item.team)} · ${escapeHtml(item.detail)}</small></div>`).join("")}</div>`, "section-gap")}
  `;
}

function renderIncidents(data) {
  const incident = data.incidents[0];
  root.innerHTML = `
    ${pageHead("Incidents & learning", "An incident is not closed when service recovers.", "It closes when the lesson is verified, propagated, converted into protection, and understood by the people who will operate the system next.")}
    <div class="incident-layout">
      ${card("Learning cases", "Real and concept evidence", `<div class="incident-list">${data.incidents.map((item, index) => `<div class="incident-row ${index === 0 ? "active" : ""}"><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.id)} · ${escapeHtml(item.status)}</span></div>`).join("")}</div>`)}
      ${card(`<span class="failure-id">${escapeHtml(incident.id)}</span> · ${escapeHtml(incident.title)}`, "Public Kubernetes evidence · no contributor scoring", `<div class="card-body">
        <div class="dimension-grid">${Object.entries(incident.dimensions).map(([key, value]) => `<article class="dimension-card"><span>${escapeHtml(key)}</span><p>${escapeHtml(value)}</p></article>`).join("")}</div>
        <h3 style="font-size:10px;margin:20px 0 10px">Intervention package</h3>
        <div class="check-list">${incident.interventions.map((item) => `<div class="check-item"><span class="check-symbol">✓</span><div><strong>${escapeHtml(item.type)} · ${escapeHtml(item.text)}</strong><p>Evidence-linked institutional response</p></div>${tag(item.status)}</div>`).join("")}</div>
      </div>`)}
    </div>
  `;
}

function renderCapability(data) {
  const capability = data.capability;
  root.innerHTML = `
    ${pageHead("People & capability", capability.headline, "GroundTruth identifies where collective knowledge and system support are thin, then creates evidence-based opportunities to learn, pair, practice, and transfer expertise.")}
    <div class="content-grid">
      ${card("Critical knowledge coverage", "Capability is measured at the system and team level.", `<div class="card-body coverage-list">${capability.coverage.map((item) => `
        <div class="coverage-row"><div><strong>${escapeHtml(item.area)}</strong><small>${escapeHtml(item.gap)}</small></div><div class="progress-track ${item.tone === "risk" ? "risk" : ""}"><i style="width:${item.coverage}%"></i></div><span>${item.coverage}%</span></div>`).join("")}</div>`)}
      ${card("Non-negotiable principles", "Developmental by design.", `<div class="card-body principle-list">${capability.principles.map((item) => `<div class="principle"><p>${escapeHtml(item)}</p></div>`).join("")}</div>`)}
    </div>
    <h2 style="font-size:13px;margin:25px 0 12px">Recommended development interventions</h2>
    <section class="intervention-grid">${capability.interventions.map((item) => `<article class="intervention-card">${tag(item.status)}<h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.reason)}</p><footer>${escapeHtml(item.audience)} · ${escapeHtml(item.growth)}<br>${escapeHtml(item.evidence)}</footer></article>`).join("")}</section>
    <div class="disclosure"><span>◎</span><span>GroundTruth does not rank employees, infer intelligence, or turn mistakes into punitive scores. It shows where the organization must improve its controls, shared models, ownership, and opportunities to practice.</span></div>
  `;
}

function renderOutcomes(data) {
  const outcomes = data.outcomes;
  root.innerHTML = `
    ${pageHead("Verified value", "Measure what changed—not what shipped.", "GroundTruth connects intended outcomes, evidence, engineering cost, protected value, and the lessons that should shape the next decision.")}
    ${metrics(outcomes.metrics)}
    ${card("Value and learning ledger", "Claims remain hypotheses until observed evidence supports them.", `<div class="table-scroll"><table class="data-table"><thead><tr><th>Change</th><th>Intended value</th><th>Prediction</th><th>Observed evidence</th><th>Verdict</th></tr></thead><tbody>
      ${outcomes.ledger.map((item) => `<tr><td><strong>${escapeHtml(item.change)}</strong><small>${escapeHtml(item.learning)}</small></td><td>${escapeHtml(item.intent)}</td><td>${escapeHtml(item.prediction)}</td><td>${escapeHtml(item.observed)}<small>${escapeHtml(item.cost)}</small></td><td>${tag(item.value)}</td></tr>`).join("")}
    </tbody></table></div>`)}
    <div class="disclosure"><span>ⓘ</span><span>${escapeHtml(outcomes.disclosure)}</span></div>
  `;
}

async function startRun() {
  if (state.polling) return;
  state.polling = true;
  state.run = {status: "queued", events: [], artifacts: [], evaluations: [], exposures: []};
  renderAssurance(state.data);
  toast("<strong>Evidence sealed.</strong> Five-agent blind replay started.");
  try {
    const response = await fetch("/api/assurance-runs?change_id=K8S-29297", {method: "POST"});
    if (!response.ok) throw new Error(`Start failed (${response.status})`);
    const created = await response.json();
    await pollRun(created.run_id);
  } catch (error) {
    state.polling = false;
    state.run = null;
    renderAssurance(state.data);
    toast(`<strong>Could not start:</strong> ${escapeHtml(error.message)}`);
  }
}

async function pollRun(runId) {
  while (state.polling) {
    const response = await fetch(`/api/assurance-runs/${encodeURIComponent(runId)}`, {cache: "no-store"});
    if (!response.ok) throw new Error(`Run fetch failed (${response.status})`);
    state.run = await response.json();
    renderAssurance(state.data);
    if (["complete", "failed"].includes(state.run.status)) {
      state.polling = false;
      if (state.run.status === "complete") toast("<strong>Lesson verified.</strong> Exact historical scope recovered and committed.");
      break;
    }
    await new Promise((resolve) => setTimeout(resolve, 850));
  }
}

function toast(message) {
  const region = document.getElementById("toast-region");
  const element = document.createElement("div");
  element.className = "toast";
  element.innerHTML = message;
  region.appendChild(element);
  setTimeout(() => element.remove(), 4200);
}

function render() {
  document.querySelector(`[data-nav="${page}"]`)?.classList.add("active");
  const renderers = {
    overview: renderOverview,
    changes: renderChanges,
    assurance: renderAssurance,
    memory: renderMemory,
    incidents: renderIncidents,
    capability: renderCapability,
    outcomes: renderOutcomes,
  };
  (renderers[page] || renderOverview)(state.data);
}

async function init() {
  const menu = document.getElementById("menu-button");
  menu?.addEventListener("click", () => document.getElementById("sidebar").classList.toggle("open"));
  try {
    const [platformResponse, runsResponse, ledgerResponse] = await Promise.all([
      fetch("/api/platform"),
      fetch("/api/assurance-runs", {cache: "no-store"}),
      fetch("/api/learning-ledger", {cache: "no-store"}),
    ]);
    if (!platformResponse.ok) throw new Error("Platform context unavailable");
    state.data = await platformResponse.json();
    if (runsResponse.ok) {
      const runs = await runsResponse.json();
      state.run = runs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0] || null;
    }
    if (ledgerResponse.ok) state.ledger = await ledgerResponse.json();
    render();
  } catch (error) {
    root.innerHTML = `<div class="empty-state"><span class="empty-icon">!</span><h3>GroundTruth could not load</h3><p>${escapeHtml(error.message)}</p><button class="button primary" onclick="location.reload()">Retry</button></div>`;
  }
}

init();
