from __future__ import annotations

import argparse
import json

from app.lab.payment import certification_matrix, held_out_matrix


def evaluate() -> int:
    results = certification_matrix() + held_out_matrix()
    print("GROUNDTRUTH VERIFIED-LEARNING EVALUATION")
    print("=" * 48)
    for result in results:
        print(
            f"{result.case_id:22} observed={result.observed_captures} "
            f"decision={result.decision:5} expected={result.expected_decision:5} "
            f"verified={'YES' if result.passed else 'NO'}"
        )
    print("=" * 48)
    print(json.dumps({"all_verified": all(result.passed for result in results)}, indent=2))
    return 0 if all(result.passed for result in results) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="GroundTruth command line")
    parser.add_argument("command", choices=["evaluate"])
    args = parser.parse_args()
    if args.command == "evaluate":
        return evaluate()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
