const startButton = document.querySelector("#start-run");
const workspace = document.querySelector("#workspace");
const emptyState = document.querySelector("#empty-state");
const results = document.querySelector("#results");
const runState = document.querySelector("#run-state");

const stageRank = {
  received: 0,
  investigating: 1,
  generalizing: 2,
  verifying: 3,
  learned: 3,
  evaluating: 3,
  complete: 4,
  failed: 4,
};

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value ?? "";
  return div.innerHTML;
}

function updatePipeline(status) {
  const current = stageRank[status] ?? 0;
  document.querySelectorAll(".pipeline-step").forEach((step) => {
    const rank = stageRank[step.dataset.stage];
    step.classList.toggle("done", current > rank || status === "complete");
    step.classList.toggle("active", current === rank && status !== "complete");
  });
  document.querySelectorAll(".pipeline-line").forEach((line, index) => {
    line.classList.toggle("done", current > index + 1);
  });
}

function renderInvestigation(run) {
  if (!run.investigation) return;
  document.querySelector("#investigation-summary").textContent = run.investigation.summary;
  document.querySelector("#evidence-count").textContent = `${run.investigation.evidence.length} evidence`;
  document.querySelector("#causal-chain").innerHTML = run.investigation.causal_chain
    .map((step) => `
      <li>
        <span>${String(step.order).padStart(2, "0")}</span>
        <div><p>${escapeHtml(step.claim)}</p><small>${step.evidence_ids.map(escapeHtml).join(" · ")}</small></div>
      </li>`)
    .join("");
}

function renderLearning(run) {
  if (!run.learning) return;
  document.querySelector("#failure-class").textContent = run.learning.failure_class;
  document.querySelector("#invariant").textContent = run.learning.invariant;
  const badge = document.querySelector("#learning-status");
  badge.textContent = run.learning.status === "verified" ? "Verified" : "Candidate";
  badge.classList.toggle("verified", run.learning.status === "verified");
}

function resultDescription(item) {
  if (item.case_id === "known_bad") return "Original AI retry patch";
  if (item.case_id === "corrected") return "Stable logical-operation key";
  if (item.case_id === "exact_recurrence") return "Exact recurrence in a future change";
  if (item.case_id === "held_out_variant") return "Held-out crash + redelivery variant";
  return "Safe related change";
}

function renderEvaluations(run) {
  const list = document.querySelector("#evaluation-list");
  list.innerHTML = run.evaluations.map((item) => `
    <div class="evaluation-row ${item.decision.toLowerCase()}">
      <span class="decision-icon">${item.decision === "BLOCK" ? "×" : "✓"}</span>
      <div class="evaluation-name"><strong>${escapeHtml(resultDescription(item))}</strong><small>${escapeHtml(item.label)}</small></div>
      <div class="capture-count"><small>Captures</small><strong>${item.observed_captures}</strong></div>
      <span class="decision-pill">${item.decision}</span>
    </div>`).join("");
  document.querySelector("#matrix-score").textContent = `${run.evaluations.filter((x) => x.passed).length} / 5 verified`;
}

function renderRun(run) {
  updatePipeline(run.status);
  runState.innerHTML = `<span></span>${run.status === "complete" ? "Learning complete" : escapeHtml(run.status.replaceAll("_", " "))}`;
  runState.classList.toggle("complete", run.status === "complete");
  runState.classList.toggle("failed", run.status === "failed");
  renderInvestigation(run);
  renderLearning(run);
  renderEvaluations(run);

  if (run.status === "complete") {
    const verdict = document.querySelector("#final-verdict");
    verdict.className = "final-verdict success";
    verdict.innerHTML = `<span class="verdict-mark">✓</span><div><small>Organizational memory updated</small><strong>2 recurrences blocked · 1 safe change allowed</strong><em>${escapeHtml(run.mode)}</em></div>`;
  } else if (run.status === "failed") {
    const verdict = document.querySelector("#final-verdict");
    verdict.className = "final-verdict failure";
    verdict.innerHTML = `<span class="verdict-mark">!</span><div><small>Run needs attention</small><strong>${escapeHtml(run.error)}</strong></div>`;
  }
}

async function poll(runId) {
  for (let attempt = 0; attempt < 180; attempt += 1) {
    const response = await fetch(`/api/runs/${encodeURIComponent(runId)}`);
    if (!response.ok) throw new Error("Could not load the GroundTruth run.");
    const run = await response.json();
    renderRun(run);
    if (["complete", "failed"].includes(run.status)) return run;
    await new Promise((resolve) => window.setTimeout(resolve, 700));
  }
  throw new Error("The run did not finish within the demo window.");
}

startButton.addEventListener("click", async () => {
  startButton.disabled = true;
  startButton.querySelector("span").textContent = "GroundTruth is learning…";
  workspace.classList.remove("is-idle");
  emptyState.hidden = true;
  results.hidden = false;
  workspace.scrollIntoView({ behavior: "smooth", block: "start" });
  try {
    const response = await fetch("/api/runs", { method: "POST" });
    if (!response.ok) throw new Error("Could not start the GroundTruth run.");
    const started = await response.json();
    await poll(started.run_id);
    startButton.querySelector("span").textContent = "Run again";
  } catch (error) {
    runState.className = "run-state failed";
    runState.textContent = error.message;
    startButton.querySelector("span").textContent = "Try again";
  } finally {
    startButton.disabled = false;
  }
});
