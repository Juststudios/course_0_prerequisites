"""Verification script for NEAT XOR project.

Validates that the evolved champion neural network satisfies the XOR truth table
within tight non-linear classification tolerances.
"""

import os
import pickle
import sys

# Ensure repository root is on sys.path
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.network import FeedForwardNetwork

try:
    from train_xor import XOR_DATA, train_xor
except ImportError:
    import importlib
    _train_mod = importlib.import_module("neat.projects.01_xor.train_xor")
    XOR_DATA = _train_mod.XOR_DATA
    train_xor = _train_mod.train_xor


def verify_xor() -> None:
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    champion_path = os.path.join(output_dir, "champion_xor.pkl")

    if not os.path.exists(champion_path):
        print("No pre-trained champion found. Running training first...")
        champion, _ = train_xor(output_dir=output_dir)
    else:
        with open(champion_path, "rb") as f:
            champion = pickle.load(f)

    net = FeedForwardNetwork.create(champion)

    print("\n--- Verifying XOR Predictions ---")
    results = []
    for inputs, target in XOR_DATA:
        pred = net.activate(inputs)[0]
        results.append((inputs, target, pred))
        print(f"Input: {inputs} -> Target: {target}, Prediction: {pred:.4f}")

    p00 = results[0][2]
    p01 = results[1][2]
    p10 = results[2][2]
    p11 = results[3][2]

    # Verification assertions
    assert p00 < 0.25, f"Expected XOR(0, 0) < 0.25, got {p00:.4f}"
    assert p01 > 0.75, f"Expected XOR(0, 1) > 0.75, got {p01:.4f}"
    assert p10 > 0.75, f"Expected XOR(1, 0) > 0.75, got {p10:.4f}"
    assert p11 < 0.25, f"Expected XOR(1, 1) < 0.25, got {p11:.4f}"

    print("\n[SUCCESS] All 4 XOR truth table cases successfully verified!")


if __name__ == "__main__":
    verify_xor()
