from __future__ import annotations

from typing import Any

from app.kubernetes_evidence import PUBLIC_ISSUE, allowed_evidence_packet

ORGANIZATION: dict[str, Any] = {
    "id": "northstar-engineering",
    "name": "Northstar Engineering",
    "description": "AI-native product organization · 4 portfolios · 11 engineering teams",
    "mode": "Concept organization · public Kubernetes evidence · real agent execution",
    "period": "Learning system · last 90 days",
    "metrics": [
        {
            "label": "AI-assisted change velocity",
            "value": "+38%",
            "trend": "Output is accelerating",
            "tone": "warning",
        },
        {
            "label": "Verified value",
            "value": "+9%",
            "trend": "Value is not keeping pace",
            "tone": "neutral",
        },
        {
            "label": "Known lessons enforced",
            "value": "71%",
            "trend": "+12 points this quarter",
            "tone": "good",
        },
        {
            "label": "Silent recurrences",
            "value": "4.8%",
            "trend": "Target: zero",
            "tone": "danger",
        },
    ],
    "teams": [
        {"name": "Runtime Platform", "product": "Compute Fabric", "coverage": 84, "risk": "low"},
        {"name": "Developer Platform", "product": "Build Cloud", "coverage": 67, "risk": "medium"},
        {"name": "Data Infrastructure", "product": "Event Mesh", "coverage": 58, "risk": "high"},
        {"name": "Reliability", "product": "Control Plane", "coverage": 76, "risk": "medium"},
    ],
}


CHANGES: list[dict[str, Any]] = [
    {
        "id": "K8S-29297",
        "title": "Blind replay: Kubernetes wrapped-volume race",
        "team": "Public evidence benchmark",
        "product": "kubernetes/kubernetes",
        "repository": "kubernetes/kubernetes",
        "author": "GroundTruth five-agent assurance team",
        "risk": 96,
        "status": "Ready to run",
        "decision": "SEALED",
        "files": 5,
        "tests": "Historical fix withheld",
        "value": "Prove one failure can protect the entire structural family",
        "updated": "Evidence pinned",
        "real": True,
    },
    {
        "id": "NSTR-204",
        "title": "Reuse a package-level wrapper template",
        "team": "Runtime Platform",
        "product": "Compute Fabric",
        "repository": "northstar/runtime-plugins",
        "author": "Engineer + coding agent",
        "risk": 88,
        "status": "Blocked by learned control",
        "decision": "BLOCK",
        "files": 3,
        "tests": "42 / 42 passing",
        "value": "Reduce allocation overhead",
        "updated": "After benchmark",
        "real": False,
    },
    {
        "id": "CHG-1187",
        "title": "Add idempotent event replay keys",
        "team": "Data Infrastructure",
        "product": "Event Mesh",
        "repository": "northstar/event-mesh",
        "author": "Priya + coding agent",
        "risk": 44,
        "status": "Control satisfied",
        "decision": "PASS",
        "files": 7,
        "tests": "108 / 108 passing",
        "value": "Prevent duplicate downstream effects",
        "updated": "2 hours ago",
        "real": False,
    },
    {
        "id": "CHG-1181",
        "title": "Clarify SDK migration guide",
        "team": "Developer Platform",
        "product": "Build Cloud",
        "repository": "northstar/developer-docs",
        "author": "Mina Patel",
        "risk": 4,
        "status": "Auto-passed",
        "decision": "PASS",
        "files": 2,
        "tests": "Documentation checks passing",
        "value": "Reduce migration time",
        "updated": "Yesterday",
        "real": False,
    },
]


BENCHMARK = allowed_evidence_packet()
CHANGE_DETAIL: dict[str, Any] = {
    "change": CHANGES[0],
    "issue": PUBLIC_ISSUE,
    "protocol": {
        "question": (
            "Can GroundTruth start with one reported ConfigMap failure and independently recover "
            "the complete causal blast radius?"
        ),
        "allowed": [
            "Original public issue #29297",
            "Pre-fix source snapshot at d7150bfaeae6",
            "The wrapper mutation call path",
        ],
        "withheld": [
            "Fixing PR #29641",
            "Maintainer comment identifying three more locations",
            "The eventual four-file patch scope",
        ],
        "success": [
            "Explain the pointer-aliasing causal chain",
            "Find every equivalent source location without answer-key leakage",
            "Prove the interleaving and safe control deterministically",
            "Match the withheld historical fix with no false positives",
        ],
    },
    "source_snapshots": BENCHMARK["source_snapshots"],
    "mutation_site": BENCHMARK["mutation_site"],
    "snapshot_commit": BENCHMARK["snapshot_commit"],
    "system_graph": {
        "nodes": [
            {"id": "issue", "label": "Issue #29297", "kind": "issue"},
            {"id": "configmap", "label": "ConfigMap", "kind": "observed"},
            {"id": "template", "label": "wrappedVolumeSpec", "kind": "cause"},
            {"id": "host", "label": "NewWrapperMounter", "kind": "mutation"},
            {"id": "secret", "label": "Secret", "kind": "candidate"},
            {"id": "downward", "label": "Downward API", "kind": "candidate"},
            {"id": "gitrepo", "label": "GitRepo", "kind": "candidate"},
        ],
        "edges": [
            ["issue", "configmap"],
            ["configmap", "template"],
            ["template", "host"],
            ["template", "secret"],
            ["template", "downward"],
            ["template", "gitrepo"],
        ],
        "blast_radius": "1 reported component · 3 sibling candidates · 1 reusable invariant",
    },
}


MEMORY: dict[str, Any] = {
    "metrics": [
        {"label": "Verified learning packages", "value": "38", "delta": "+1 from benchmark"},
        {"label": "Cross-team applications", "value": "94", "delta": "2.5× reuse"},
        {"label": "Recurrences intercepted", "value": "17", "delta": "before production"},
        {"label": "Ledger integrity", "value": "100%", "delta": "hash chain verified"},
    ],
    "failure_classes": [
        {
            "id": "GT-K8S-0001",
            "name": "Shared mutable nested state across concurrent operations",
            "origin": "kubernetes/kubernetes#29297",
            "invariant": (
                "Request-specific operations must not mutate pointer-reachable state shared by "
                "another concurrent request."
            ),
            "status": "Verified by blind replay",
            "applications": 5,
            "teams": ["SIG Storage", "Runtime Platform", "Developer Platform"],
            "recurrences": 1,
            "last_used": "Future PR NSTR-204 blocked",
            "provenance": (
                "Public issue + pre-fix source + deterministic proof + withheld answer key"
            ),
        },
        {
            "id": "GT-0017",
            "name": "Retry after ambiguous external side effect",
            "origin": "Northstar Payments · INC-481",
            "invariant": "One logical operation must produce at most one committed side effect.",
            "status": "Verified",
            "applications": 11,
            "teams": ["Payments", "Checkout", "Fulfilment"],
            "recurrences": 0,
            "last_used": "3 days ago",
            "provenance": "Internal incident + execution trace + regression suite",
        },
        {
            "id": "GT-0021",
            "name": "Partial cache invalidation across regional writers",
            "origin": "Catalog · INC-509",
            "invariant": "Readers must not observe a mixed-version aggregate.",
            "status": "Candidate—not yet enforced",
            "applications": 2,
            "teams": ["Catalog", "Search"],
            "recurrences": 0,
            "last_used": "Awaiting proof",
            "provenance": "Incident hypothesis; evaluator pending",
        },
    ],
    "propagation": [
        {
            "product": "ConfigMap",
            "team": "SIG Storage",
            "state": "Observed failure",
            "tone": "source",
            "detail": "Issue #29297",
        },
        {
            "product": "Secret",
            "team": "SIG Storage",
            "state": "Sibling exposure",
            "tone": "warning",
            "detail": "Same complete signature",
        },
        {
            "product": "Downward API",
            "team": "SIG Storage",
            "state": "Sibling exposure",
            "tone": "warning",
            "detail": "Same complete signature",
        },
        {
            "product": "GitRepo",
            "team": "SIG Storage",
            "state": "Sibling exposure",
            "tone": "warning",
            "detail": "Same complete signature",
        },
        {
            "product": "Compute Fabric",
            "team": "Runtime Platform",
            "state": "Future recurrence blocked",
            "tone": "blocked",
            "detail": "NSTR-204",
        },
    ],
}


INCIDENTS: list[dict[str, Any]] = [
    {
        "id": "K8S-29297",
        "title": PUBLIC_ISSUE["title"],
        "team": "Kubernetes SIG Storage",
        "severity": "Important—soon",
        "date": "20 Jul 2016",
        "status": "Public evidence · historically fixed",
        "real": True,
        "dimensions": {
            "technical": (
                "A shallow value copy retained a shared nested pointer that was mutated per mount."
            ),
            "testing": (
                "Functional paths passed; concurrent multi-mount ownership was not asserted."
            ),
            "process": (
                "The immediate change was reviewed locally before the invariant became "
                "reusable knowledge."
            ),
            "organizational": "The same construction existed in four sibling plugins.",
            "human": (
                "A subtle Go ownership model needed to become collective capability—not "
                "individual blame."
            ),
        },
        "interventions": [
            {
                "type": "Code",
                "text": "Fresh spec factory per mount",
                "status": "Historically merged",
            },
            {
                "type": "Control",
                "text": "Shared mutable template structural check",
                "status": "Generated",
            },
            {"type": "Test", "text": "Concurrent aliasing falsifier", "status": "Verified"},
            {"type": "Capability", "text": "Pointer ownership teach-back", "status": "Ready"},
        ],
    },
    {
        "id": "INC-481",
        "title": "Duplicate payment after provider acknowledgement loss",
        "team": "Payments",
        "severity": "SEV-1",
        "date": "14 May",
        "status": "Learning verified",
        "real": False,
    },
    {
        "id": "INC-509",
        "title": "Mixed-version catalog visible during regional invalidation",
        "team": "Catalog",
        "severity": "SEV-2",
        "date": "03 Aug",
        "status": "Verification pending",
        "real": False,
    },
]


CAPABILITY: dict[str, Any] = {
    "headline": "Grow collective capability—not individual surveillance.",
    "coverage": [
        {
            "area": "Concurrency ownership",
            "coverage": 61,
            "owners": 3,
            "gap": "Nested-pointer isolation inconsistently reviewed",
            "tone": "risk",
        },
        {
            "area": "Failure-class modeling",
            "coverage": 74,
            "owners": 5,
            "gap": "Two teams still capture symptoms only",
            "tone": "warning",
        },
        {
            "area": "Adversarial test design",
            "coverage": 68,
            "owners": 4,
            "gap": "Deterministic interleavings underused",
            "tone": "warning",
        },
        {
            "area": "Learning transfer",
            "coverage": 82,
            "owners": 7,
            "gap": "One portfolio has no backup steward",
            "tone": "good",
        },
    ],
    "interventions": [
        {
            "title": "Go shallow-copy and pointer-aliasing teach-back",
            "audience": "Runtime + Developer Platform",
            "reason": "The verified Kubernetes case makes a subtle ownership rule concrete.",
            "evidence": "GT-K8S-0001 · deterministic A/B interleaving",
            "status": "Ready",
            "growth": "Understand → challenge → transfer",
        },
        {
            "title": "Cross-repository pattern-scout rotation",
            "audience": "Reliability guild",
            "reason": "A local fix must trigger a structural sibling search.",
            "evidence": "Four Kubernetes exposures from one issue",
            "status": "Recommended",
            "growth": "Local expertise → organizational capability",
        },
        {
            "title": "Deterministic concurrency lab",
            "audience": "All platform teams",
            "reason": "Happy-path suites did not reveal the ownership violation.",
            "evidence": "CHECK-ALIAS / CHECK-CONTROL",
            "status": "Created",
            "growth": "Practice with verified evidence",
        },
    ],
    "principles": [
        "Improve the system of work before judging the people inside it.",
        "Treat mistakes as learning opportunities; treat repeated known mistakes as "
        "systemic signals.",
        "Keep high-consequence judgment and accountability human.",
        "Measure knowledge coverage and transfer—never employee intelligence scores.",
    ],
}


OUTCOMES: dict[str, Any] = {
    "metrics": [
        {
            "label": "Benchmark precision",
            "value": "100%",
            "detail": "4 discovered / 4 historical paths",
            "tone": "good",
        },
        {
            "label": "Benchmark recall",
            "value": "100%",
            "detail": "No historical exposure missed",
            "tone": "good",
        },
        {
            "label": "Protected components",
            "value": "4 + future",
            "detail": "One observed, three propagated, future guard",
            "tone": "good",
        },
        {
            "label": "Unverified value claims",
            "value": "0",
            "detail": "Synthetic metrics remain explicitly labeled",
            "tone": "neutral",
        },
    ],
    "ledger": [
        {
            "change": "K8S-29297",
            "intent": "Recover the complete causal blast radius",
            "prediction": "Find structurally equivalent sibling components",
            "observed": "Exact match to four-path withheld answer key",
            "cost": "One bounded assurance run",
            "value": "Independently verified",
            "learning": "GT-K8S-0001 created and hash-linked",
        },
        {
            "change": "NSTR-204",
            "intent": "Reduce wrapper-allocation overhead",
            "prediction": "Small performance improvement",
            "observed": "Known failure class intercepted before merge",
            "cost": "Automated control execution",
            "value": "Protected",
            "learning": "A public lesson transferred into a future organizational guard",
        },
        {
            "change": "CHG-1187",
            "intent": "Prevent duplicate downstream effects",
            "prediction": "Zero duplicate commits during replay",
            "observed": "Control passed across 10,000 fault-injected deliveries",
            "cost": "4 engineer-days",
            "value": "Verified",
            "learning": "Existing institutional pattern reused instead of rediscovered",
        },
    ],
    "disclosure": (
        "Kubernetes issue, source locations, commit identifiers, and fixing PR are public real "
        "evidence. Northstar organization, people, financial, and portfolio metrics are synthetic "
        "concept data. Agent execution and deterministic evaluator results are real."
    ),
}


ACTIVITY: list[dict[str, Any]] = [
    {
        "time": "Now",
        "agent": "Ground-Truth Judge",
        "action": "Sealed PR #29641 as the blind answer key",
        "tone": "memory",
    },
    {
        "time": "1 min",
        "agent": "Pattern Scout",
        "action": "Expanded one ConfigMap issue to four structural candidates",
        "tone": "map",
    },
    {
        "time": "2 min",
        "agent": "Adversary",
        "action": "Prepared deterministic aliasing interleaving",
        "tone": "warning",
    },
    {
        "time": "8 min",
        "agent": "Learning Architect",
        "action": "Attached future shared-template control",
        "tone": "growth",
    },
    {
        "time": "1 hr",
        "agent": "Outcome Judge",
        "action": "Rejected an unverified avoidance estimate",
        "tone": "value",
    },
]


def platform_payload() -> dict[str, Any]:
    return {
        "organization": ORGANIZATION,
        "changes": CHANGES,
        "change_detail": CHANGE_DETAIL,
        "memory": MEMORY,
        "incidents": INCIDENTS,
        "capability": CAPABILITY,
        "outcomes": OUTCOMES,
        "activity": ACTIVITY,
    }
