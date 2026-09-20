#!/usr/bin/env python3
"""
run_all_e2e_tests.py
====================
Master Test Runner for Curriculum Completion End-to-End Test Suite.

Executes all 4 Milestone E2E suites across the 4-Tier Test Design Methodology:
  - M1: Deep Learning Lessons & Neural Networks (test_deep_learning_e2e.py)
  - M2: Mathematics & Game AI Implementations (test_math_game_ai_e2e.py)
  - M3: Level 6 Networking & TensorFlow Fundamentals (test_networking_tf_e2e.py)
  - M4: Capstones & Simulink Dynamic Modeling (test_capstones_simulink_e2e.py)

Outputs:
  - Formatted Unicode / ASCII Summary Tables by Milestone and by Tier
  - Granular timing metrics and pass/fail counts
  - Returns exit code 0 on 100% PASS, 1 on any failure.
"""

import argparse
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TESTS_E2E_DIR = REPO_ROOT / "tests" / "e2e"

SUITES = [
    {
        "id": "M1",
        "name": "Deep Learning & Neural Networks",
        "file": "test_deep_learning_e2e.py",
        "scope": "BatchNorm, Dropout, Deep MLP Fault Classifier, PyTorch Lessons",
    },
    {
        "id": "M2",
        "name": "Mathematics & Game AI",
        "file": "test_math_game_ai_e2e.py",
        "scope": "NumPy PCA, Logistic Regression GD, Checkers Engine, MCTS, Tabular Q-Learning",
    },
    {
        "id": "M3",
        "name": "Networking & TensorFlow",
        "file": "test_networking_tf_e2e.py",
        "scope": "TCP/UDP Sockets, HTTP Clients/Servers, FastAPI Telemetry, TF Autodiff & Keras",
    },
    {
        "id": "M4",
        "name": "Capstones & Simulink",
        "file": "test_capstones_simulink_e2e.py",
        "scope": "Industrial ML Capstone, Reversi AI Engine, Simulink ODE45 Companions & Motor Control",
    },
]


@dataclass
class SuiteResult:
    milestone: str
    name: str
    file_name: str
    total: int
    passed: int
    failed: int
    skipped: int
    duration_s: float
    return_code: int
    stdout: str
    stderr: str

    @property
    def is_success(self) -> bool:
        return self.return_code == 0 and self.failed == 0


def run_suite(suite_info: dict, extra_args: Optional[List[str]] = None) -> SuiteResult:
    """Execute a single pytest suite file and parse results."""
    test_path = TESTS_E2E_DIR / suite_info["file"]
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test_path),
        "-v",
        "--tb=short",
    ]
    if extra_args:
        cmd.extend(extra_args)

    env = os.environ.copy()
    env["MKL_SERVICE_FORCE_INTEL"] = "1"
    env["MKL_THREADING_LAYER"] = "GNU"
    env["MPLBACKEND"] = "Agg"
    env["OMP_NUM_THREADS"] = "2"

    t0 = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    duration = time.perf_counter() - t0

    out = proc.stdout
    # Parse pytest summary line: e.g., "37 passed, 1 warning in 4.58s" or "28 passed in 9.00s"
    passed = 0
    failed = 0
    skipped = 0

    m_pass = re.search(r"(\d+)\s+passed", out)
    if m_pass:
        passed = int(m_pass.group(1))

    m_fail = re.search(r"(\d+)\s+failed", out)
    if m_fail:
        failed = int(m_fail.group(1))

    m_skip = re.search(r"(\d+)\s+skipped", out)
    if m_skip:
        skipped = int(m_skip.group(1))

    total = passed + failed + skipped

    return SuiteResult(
        milestone=suite_info["id"],
        name=suite_info["name"],
        file_name=suite_info["file"],
        total=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        duration_s=duration,
        return_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def run_tier(tier_marker: str) -> Tuple[int, int, int, float]:
    """Execute tests for a specific tier marker and return (total, passed, failed, duration)."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(TESTS_E2E_DIR),
        "-m",
        tier_marker,
        "-q",
        "--no-header",
    ]
    env = os.environ.copy()
    env["MKL_SERVICE_FORCE_INTEL"] = "1"
    env["MKL_THREADING_LAYER"] = "GNU"
    env["MPLBACKEND"] = "Agg"

    t0 = time.perf_counter()
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, env=env)
    dur = time.perf_counter() - t0

    out = proc.stdout
    passed = 0
    failed = 0
    m_pass = re.search(r"(\d+)\s+passed", out)
    if m_pass:
        passed = int(m_pass.group(1))
    m_fail = re.search(r"(\d+)\s+failed", out)
    if m_fail:
        failed = int(m_fail.group(1))

    return (passed + failed, passed, failed, dur)


def print_banner():
    print("=" * 86)
    print("      CURRICULUM COMPLETION PROJECT — MASTER E2E TEST RUNNER")
    print("       Full 7-Level Engineering Courseware End-to-End Verification")
    print("=" * 86)
    print()


def print_suite_table(results: List[SuiteResult]):
    header = f"┌─────┬──────────────────────────────────────┬───────┬────────┬────────┬──────────┬────────┐"
    titles = f"│ MS  │ Test Suite Module                    │ Total │ Passed │ Failed │ Time (s) │ Status │"
    divider = f"├─────┼──────────────────────────────────────┼───────┼────────┼────────┼──────────┼────────┤"
    bottom = f"└─────┴──────────────────────────────────────┴───────┴────────┴────────┴──────────┴────────┘"

    print(header)
    print(titles)
    print(divider)

    tot_tests = 0
    tot_pass = 0
    tot_fail = 0
    tot_time = 0.0

    for r in results:
        tot_tests += r.total
        tot_pass += r.passed
        tot_fail += r.failed
        tot_time += r.duration_s

        status_str = " PASS " if r.is_success else " FAIL "
        print(
            f"│ {r.milestone:3s} │ {r.name:36s} │ {r.total:5d} │ {r.passed:6d} │ {r.failed:6d} │ {r.duration_s:8.2f} │ {status_str} │"
        )

    print(divider)
    all_success = tot_fail == 0
    grand_status = " PASS " if all_success else " FAIL "
    print(
        f"│ ALL │ TOTAL E2E TEST SUITES ({len(results)} SUITES)      │ {tot_tests:5d} │ {tot_pass:6d} │ {tot_fail:6d} │ {tot_time:8.2f} │ {grand_status} │"
    )
    print(bottom)
    print()


def print_tier_breakdown():
    print("─" * 86)
    print("  4-TIER PROGRESSION METHODOLOGY BREAKDOWN")
    print("─" * 86)

    tiers = [
        ("tier1", "Tier 1: Isolated Feature & Contract Coverage", "Verifies primary behavioral contracts and nominal execution in isolation."),
        ("tier2", "Tier 2: Boundary & Corner Condition Stress", "Evaluates ephemeral ports, zero payloads, saturation limits, empty batches."),
        ("tier3", "Tier 3: Pairwise Cross-Feature Integration", "Tests HTTP against REST APIs, Keras via FastAPI, depth scaling, numerical ODEs."),
        ("tier4", "Tier 4: End-to-End Autonomous Real-World Workflows", "Runs full 60-turn Reversi self-play, closed-loop motor PI, full ML capstones."),
    ]

    header = f"┌──────────────────────────────────────────────────────────────┬───────┬────────┬────────┐"
    titles = f"│ Test Methodology Tier                                        │ Total │ Passed │ Failed │"
    divider = f"├──────────────────────────────────────────────────────────────┼───────┼────────┼────────┤"
    bottom = f"└──────────────────────────────────────────────────────────────┴───────┴────────┴────────┘"

    print(header)
    print(titles)
    print(divider)

    for marker, title, desc in tiers:
        tot, p, f, dur = run_tier(marker)
        print(f"│ {title:60s} │ {tot:5d} │ {p:6d} │ {f:6d} │")

    print(bottom)
    print()


def main():
    parser = argparse.ArgumentParser(description="Master E2E Test Suite Runner")
    parser.add_argument("--milestone", choices=["M1", "M2", "M3", "M4", "all"], default="all",
                        help="Filter execution to specific milestone")
    parser.add_argument("--skip-tier-breakdown", action="store_true",
                        help="Skip 4-tier breakdown rerun")
    args = parser.parse_args()

    print_banner()

    suites_to_run = SUITES if args.milestone == "all" else [s for s in SUITES if s["id"] == args.milestone]

    results: List[SuiteResult] = []
    print(f"[*] Executing {len(suites_to_run)} End-to-End Test Suites...\n")

    for s in suites_to_run:
        print(f"  -> Executing {s['id']}: {s['name']} ({s['file']})...", end="", flush=True)
        res = run_suite(s)
        status_label = "PASS" if res.is_success else "FAIL"
        print(f" [{status_label}] ({res.passed}/{res.total} passed in {res.duration_s:.2f}s)")
        results.append(res)

    print()
    print_suite_table(results)

    if not args.skip_tier_breakdown and args.milestone == "all":
        print_tier_breakdown()

    # Executive Summary & Exit Code
    all_passed = all(r.is_success for r in results)
    total_count = sum(r.total for r in results)
    passed_count = sum(r.passed for r in results)
    failed_count = sum(r.failed for r in results)

    print("=" * 86)
    if all_passed:
        print(f"  EXECUTIVE VERDICT: 100% READY FOR CURRICULUM CERTIFICATION")
        print(f"  All {total_count} End-to-End Tests Across Milestones M1-M4 Passed Cleanly.")
        print("=" * 86)
        sys.exit(0)
    else:
        print(f"  EXECUTIVE VERDICT: TEST FAILURES DETECTED ({failed_count} tests failed)")
        print("=" * 86)
        sys.exit(1)


if __name__ == "__main__":
    main()
