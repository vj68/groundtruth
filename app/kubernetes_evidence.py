from __future__ import annotations

import hashlib
import json
import re
from copy import copy
from dataclasses import dataclass
from typing import Any

PRE_FIX_COMMIT = "d7150bfaeae642efc08c8ede0ed2ec8ecb340c8e"
INTRODUCING_COMMIT = "3567b1f9c48bb6879fbe7d36b8c634e849f59438"


PUBLIC_ISSUE: dict[str, Any] = {
    "id": "kubernetes/kubernetes#29297",
    "title": "Mounting configmap as volume sometimes causes FailedMount error",
    "url": "https://github.com/kubernetes/kubernetes/issues/29297",
    "opened": "2016-07-20",
    "repository": "kubernetes/kubernetes",
    "reported_component": "ConfigMap volume plugin",
    "symptom": (
        "Pods intermittently remain in ContainerCreating while simultaneous ConfigMap "
        "volumes fail to mount."
    ),
    "signal": "Error creating atomic writer: no such file or directory",
}


SOURCE_SNAPSHOTS: list[dict[str, Any]] = [
    {
        "component": "ConfigMap",
        "path": "pkg/volume/configmap/configmap.go",
        "declaration_line": 125,
        "call_line": 140,
        "source": """var wrappedVolumeSpec = volume.Spec{
    Volume: &api.Volume{VolumeSource: api.VolumeSource{
        EmptyDir: &api.EmptyDirVolumeSource{},
    }},
}

wrapped, err := b.plugin.host.NewWrapperMounter(
    b.volName, wrappedVolumeSpec, &b.pod, *b.opts,
)""",
    },
    {
        "component": "Secret",
        "path": "pkg/volume/secret/secret.go",
        "declaration_line": 48,
        "call_line": 153,
        "source": """var wrappedVolumeSpec = volume.Spec{
    Volume: &api.Volume{VolumeSource: api.VolumeSource{
        EmptyDir: &api.EmptyDirVolumeSource{Medium: api.StorageMediumMemory},
    }},
}

wrapped, err := b.plugin.host.NewWrapperMounter(
    b.volName, wrappedVolumeSpec, &b.pod, *b.opts,
)""",
    },
    {
        "component": "Downward API",
        "path": "pkg/volume/downwardapi/downwardapi.go",
        "declaration_line": 52,
        "call_line": 147,
        "source": """var wrappedVolumeSpec = volume.Spec{
    Volume: &api.Volume{VolumeSource: api.VolumeSource{
        EmptyDir: &api.EmptyDirVolumeSource{Medium: api.StorageMediumMemory},
    }},
}

wrapped, err := b.plugin.host.NewWrapperMounter(
    b.volName, wrappedVolumeSpec, b.pod, *b.opts,
)""",
    },
    {
        "component": "GitRepo",
        "path": "pkg/volume/git_repo/git_repo.go",
        "declaration_line": 44,
        "call_line": 158,
        "source": """var wrappedVolumeSpec = volume.Spec{
    Volume: &api.Volume{VolumeSource: api.VolumeSource{
        EmptyDir: &api.EmptyDirVolumeSource{},
    }},
}

wrapped, err := b.plugin.host.NewWrapperMounter(
    b.volName, wrappedVolumeSpec, &b.pod, b.opts,
)""",
    },
]


MUTATION_SITE: dict[str, Any] = {
    "path": "pkg/kubelet/volume_host.go",
    "line": 87,
    "source": """func (kvh *kubeletVolumeHost) NewWrapperMounter(
    volName string, spec volume.Spec, pod *api.Pod, opts volume.VolumeOptions,
) (volume.Mounter, error) {
    wrapperVolumeName := "wrapped_" + volName
    if spec.Volume != nil {
        spec.Volume.Name = wrapperVolumeName
    }
    return kvh.kubelet.newVolumeMounterFromPlugins(&spec, pod, opts)
}""",
    "explanation": (
        "The outer volume.Spec is copied by value, but spec.Volume remains a shared pointer. "
        "Each concurrent mount mutates the same nested api.Volume.Name."
    ),
}


WITHHELD_GROUND_TRUTH: dict[str, Any] = {
    "id": "kubernetes/kubernetes#29641",
    "title": "Fix wrapped volume race",
    "url": "https://github.com/kubernetes/kubernetes/pull/29641",
    "merged": "2016-07-27",
    "expected_components": ["ConfigMap", "Secret", "Downward API", "GitRepo"],
    "expected_paths": [item["path"] for item in SOURCE_SNAPSHOTS],
    "remediation": (
        "Replace each package-level shared spec with a function that returns a fresh "
        "volume.Spec and nested api.Volume for every mount."
    ),
    "disclosure": (
        "This fixing PR and its discussion are withheld from the agent packet and used only "
        "after analysis as an independent historical answer key."
    ),
}


def allowed_evidence_packet() -> dict[str, Any]:
    """Evidence visible to agents during the blind replay; no answer-key fields are included."""

    return {
        "benchmark": "Kubernetes blind historical replay",
        "repository": PUBLIC_ISSUE["repository"],
        "snapshot_commit": PRE_FIX_COMMIT,
        "issue": PUBLIC_ISSUE,
        "source_snapshots": SOURCE_SNAPSHOTS,
        "mutation_site": MUTATION_SITE,
        "constraints": [
            "Treat wording similarity as a lead, never as proof.",
            "Report only source locations satisfying the complete causal signature.",
            "Do not assume the eventual fix or its scope.",
        ],
    }


def discover_exposures(packet: dict[str, Any]) -> list[dict[str, Any]]:
    """Trusted structural evaluator for the benchmark's complete causal signature."""

    declaration = re.compile(r"var\s+wrappedVolumeSpec\s*=\s*volume\.Spec")
    unsafe_use = re.compile(r"NewWrapperMounter\([\s\S]*?wrappedVolumeSpec")
    findings: list[dict[str, Any]] = []
    for snapshot in packet["source_snapshots"]:
        source = snapshot["source"]
        declaration_match = bool(declaration.search(source))
        use_match = bool(unsafe_use.search(source))
        if declaration_match and use_match:
            findings.append(
                {
                    "component": snapshot["component"],
                    "path": snapshot["path"],
                    "declaration_line": snapshot["declaration_line"],
                    "call_line": snapshot["call_line"],
                    "signature": "shared-template + nested-pointer + mutating-wrapper-call",
                    "decision": "EXPOSURE VERIFIED",
                }
            )
    return findings


@dataclass
class _Volume:
    name: str = "template"


@dataclass
class _Spec:
    volume: _Volume


def run_aliasing_reproducer() -> dict[str, Any]:
    """Deterministically demonstrates the pointer alias that makes the race possible."""

    shared = _Spec(volume=_Volume())
    mount_a = copy(shared)
    mount_b = copy(shared)
    mount_a.volume.name = "wrapped_config-a"
    a_before_interleave = mount_a.volume.name
    mount_b.volume.name = "wrapped_config-b"
    a_after_interleave = mount_a.volume.name

    fixed_a = _Spec(volume=_Volume())
    fixed_b = _Spec(volume=_Volume())
    fixed_a.volume.name = "wrapped_config-a"
    fixed_b.volume.name = "wrapped_config-b"

    return {
        "check": "Nested pointer isolation under interleaved mounts",
        "trusted": True,
        "vulnerable": {
            "a_before_interleave": a_before_interleave,
            "a_after_interleave": a_after_interleave,
            "b_after_interleave": mount_b.volume.name,
            "same_nested_object": mount_a.volume is mount_b.volume,
            "decision": "FAIL",
        },
        "remediated": {
            "a_after_interleave": fixed_a.volume.name,
            "b_after_interleave": fixed_b.volume.name,
            "same_nested_object": fixed_a.volume is fixed_b.volume,
            "decision": "PASS",
        },
        "falsifier": "Mount A observes Mount B's wrapper name after an interleaving.",
    }


def compare_with_withheld_ground_truth(findings: list[dict[str, Any]]) -> dict[str, Any]:
    discovered_paths = sorted(item["path"] for item in findings)
    expected_paths = sorted(WITHHELD_GROUND_TRUTH["expected_paths"])
    precision = len(set(discovered_paths) & set(expected_paths)) / max(len(discovered_paths), 1)
    recall = len(set(discovered_paths) & set(expected_paths)) / len(expected_paths)
    return {
        "answer_key": WITHHELD_GROUND_TRUTH,
        "revealed_after_analysis": True,
        "discovered_paths": discovered_paths,
        "exact_scope_match": discovered_paths == expected_paths,
        "precision": precision,
        "recall": recall,
        "verdict": "INDEPENDENTLY VERIFIED"
        if discovered_paths == expected_paths
        else "PARTIAL MATCH",
    }


def evidence_digest() -> str:
    canonical = json.dumps(allowed_evidence_packet(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()
