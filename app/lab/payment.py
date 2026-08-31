from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from uuid import uuid4

from app.domain import Capture, ScenarioResult, TraceEvent


@dataclass
class PaymentProvider:
    """A deterministic provider simulator with real idempotency semantics."""

    captures: list[Capture] = field(default_factory=list)
    by_idempotency_key: dict[str, Capture] = field(default_factory=dict)
    trace: list[TraceEvent] = field(default_factory=list)

    def record(self, event: str, detail: str) -> None:
        self.trace.append(TraceEvent(sequence=len(self.trace) + 1, event=event, detail=detail))

    def capture(self, *, order_id: str, amount: int, idempotency_key: str) -> Capture:
        self.record(
            "provider.capture.requested",
            f"order={order_id} amount={amount} key={idempotency_key}",
        )
        if idempotency_key in self.by_idempotency_key:
            capture = self.by_idempotency_key[idempotency_key]
            self.record(
                "provider.capture.deduplicated",
                f"returned existing capture={capture.capture_id} for key={idempotency_key}",
            )
            return capture

        capture = Capture(
            capture_id=f"cap_{uuid4().hex[:8]}",
            order_id=order_id,
            amount=amount,
            idempotency_key=idempotency_key,
        )
        self.captures.append(capture)
        self.by_idempotency_key[idempotency_key] = capture
        self.record(
            "provider.capture.succeeded",
            f"created capture={capture.capture_id} key={idempotency_key}",
        )
        return capture

    def captures_for(self, order_id: str) -> list[Capture]:
        return [capture for capture in self.captures if capture.order_id == order_id]


def _decision(observed: int, expected: str, limit: int = 1) -> tuple[bool, str]:
    invariant_holds = observed <= limit
    decision = "PASS" if invariant_holds else "BLOCK"
    return decision == expected, decision


def run_scenario(case_id: str) -> ScenarioResult:
    """Execute a demo case against the real provider state machine."""

    started = perf_counter()
    provider = PaymentProvider()
    order_id = "order-481"
    amount = 5000

    if case_id in {"known_bad", "exact_recurrence"}:
        label = "AI retry patch: acknowledgement-loss recurrence"
        expected = "BLOCK"
        provider.record("order.capture.started", "payment worker starts the initial capture")
        provider.capture(
            order_id=order_id,
            amount=amount,
            idempotency_key=f"{order_id}:attempt-1",
        )
        provider.record(
            "network.acknowledgement.lost",
            "provider succeeded, but the worker did not receive the acknowledgement",
        )
        provider.record("retry.scheduled", "worker schedules retry after ambiguous timeout")
        provider.capture(
            order_id=order_id,
            amount=amount,
            idempotency_key=f"{order_id}:attempt-2",
        )

    elif case_id == "corrected":
        label = "Corrected retry: stable logical-operation key"
        expected = "PASS"
        stable_key = f"payment-capture:{order_id}"
        provider.record("order.capture.started", "payment worker starts the initial capture")
        provider.capture(order_id=order_id, amount=amount, idempotency_key=stable_key)
        provider.record(
            "network.acknowledgement.lost",
            "provider succeeded, but the worker did not receive the acknowledgement",
        )
        provider.record("retry.scheduled", "worker retries with the same logical-operation key")
        provider.capture(order_id=order_id, amount=amount, idempotency_key=stable_key)

    elif case_id == "held_out_variant":
        label = "Held-out variant: consumer crash and queue redelivery"
        expected = "BLOCK"
        provider.record("queue.delivery.received", "delivery=evt-9001 attempt=1")
        provider.capture(
            order_id=order_id,
            amount=amount,
            idempotency_key="evt-9001:delivery-1",
        )
        provider.record(
            "consumer.crashed",
            "consumer terminated after provider capture and before completion was persisted",
        )
        provider.record("queue.delivery.redelivered", "delivery=evt-9001 attempt=2")
        provider.capture(
            order_id=order_id,
            amount=amount,
            idempotency_key="evt-9001:delivery-2",
        )

    elif case_id == "safe_change":
        label = "Safe retry change: redelivery with stable operation key"
        expected = "PASS"
        stable_key = f"payment-capture:{order_id}"
        provider.record("queue.delivery.received", "delivery=evt-9001 attempt=1")
        provider.capture(order_id=order_id, amount=amount, idempotency_key=stable_key)
        provider.record(
            "consumer.crashed",
            "consumer terminated after provider capture and before completion was persisted",
        )
        provider.record("queue.delivery.redelivered", "delivery=evt-9001 attempt=2")
        provider.capture(order_id=order_id, amount=amount, idempotency_key=stable_key)

    elif case_id == "normal_success":
        label = "Baseline: normal successful payment"
        expected = "PASS"
        provider.record("order.capture.started", "normal request path")
        provider.capture(
            order_id=order_id,
            amount=amount,
            idempotency_key=f"payment-capture:{order_id}",
        )

    else:
        raise ValueError(f"Unknown scenario: {case_id}")

    observed = len(provider.captures_for(order_id))
    passed, decision = _decision(observed, expected)
    provider.record(
        "groundtruth.invariant.evaluated",
        f"successful captures={observed}; required <=1; decision={decision}",
    )
    duration_ms = max(1, int((perf_counter() - started) * 1000))
    return ScenarioResult(
        case_id=case_id,
        label=label,
        expected_decision=expected,
        observed_captures=observed,
        passed=passed,
        decision=decision,
        trace=provider.trace,
        captures=provider.captures,
        duration_ms=duration_ms,
    )


def certification_matrix() -> list[ScenarioResult]:
    return [run_scenario("known_bad"), run_scenario("corrected")]


def held_out_matrix() -> list[ScenarioResult]:
    return [
        run_scenario("exact_recurrence"),
        run_scenario("held_out_variant"),
        run_scenario("safe_change"),
    ]

