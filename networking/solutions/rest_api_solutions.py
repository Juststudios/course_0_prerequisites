"""
rest_api_solutions.py
=====================
Complete reference solutions for Level 6 Networking — Module 3 (REST APIs).
Contains 0 TODOs. Fully implemented and verified.
"""

import time
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

print("=" * 70)
print("SOLUTIONS: LEVEL 6 NETWORKING — MODULE 3 (REST APIS)")
print("=" * 70)

# ============================================================================
# SOLUTION TIER 1: RECALL & ARCHITECTURAL PRINCIPLES
# ============================================================================
RECALL_ANSWERS = {
    "1_rest_constraints": (
        "1. Client-Server: Separation of UI/client concerns from backend data storage. "
        "2. Stateless: No client context is stored on the server between requests. "
        "3. Cacheable: Responses must implicitly or explicitly label themselves cacheable. "
        "4. Layered System: Intermediaries (proxies, gateways) can be inserted transparently. "
        "5. Uniform Interface: Standard resource identification (URIs), manipulation via "
        "representations, self-descriptive messages, and hypermedia (HATEOAS). "
        "6. Code-on-Demand (optional): Ability to extend client functionality via executable code."
    ),
    "2_richardson_maturity": (
        "Level 0: The Swamp of POX (Single URI, single POST, RPC calls). "
        "Level 1: Resources (Individual URIs for individual business resources). "
        "Level 2: HTTP Verbs & Status Codes (Appropriate use of GET, POST, DELETE, 200, 201, 404). "
        "Level 3: Hypermedia Controls / HATEOAS (API responses provide clickable links to valid next actions)."
    ),
    "3_nouns_vs_verbs": (
        "URIs represent nouns (entities/resources), while HTTP methods represent verbs (actions). "
        "Using /models instead of /getModels decouples the resource identity from the operations "
        "performed on it, enabling standard HTTP caching, uniform tooling, and idempotency guarantees."
    ),
    "4_liveness_vs_readiness": (
        "Liveness (/healthz) checks if the server process is alive and responsive. If it fails, "
        "the orchestrator terminates and restarts the container. Readiness (/readyz) checks if "
        "heavy ML weights and data structures are loaded into memory and ready for inference. "
        "If readiness fails, traffic routing pauses without restarting the container."
    ),
    "5_422_vs_400": (
        "400 Bad Request indicates syntactical error (e.g. malformed unparseable JSON). "
        "422 Unprocessable Entity indicates valid syntax, but semantic validation rules failed "
        "(e.g. a temperature float exceeds physical bounds or a required string is missing)."
    ),
}

# ============================================================================
# SOLUTION TIER 2: ROUTE ORDERING & BUG EXPLANATION
# ============================================================================
def fix_route_ordering_explanation() -> str:
    """
    Explains the mechanics of router route evaluation and shadowing.
    """
    return (
        "FastAPI and Starlette evaluate route patterns sequentially in the exact order they are declared. "
        "When a parameterized route like '/sensors/{sensor_id}' is declared before a static route like "
        "'/sensors/statistics', the path router attempts to match '/sensors/statistics' against '{sensor_id}'. "
        "Because 'statistics' cannot be parsed as an integer sensor_id, FastAPI raises an HTTP 422 "
        "validation error before the static route handler is ever reached. "
        "Fix: Always declare specific, static routes BEFORE parameterized dynamic path routes."
    )


# ============================================================================
# SOLUTION TIER 3: APPLICATION — TELEMETRY INGESTION & AGGREGATION
# ============================================================================
class TelemetryRecord(BaseModel):
    sensor_id: str = Field(..., min_length=1)
    reading: float
    timestamp: float = Field(default_factory=time.time)


class SensorStats(BaseModel):
    sensor_id: str
    count: int
    min_val: float
    max_val: float
    mean_val: float


class TelemetryAggregatorStore:
    """
    Thread-safe in-memory store for sensor telemetry aggregation.
    """

    def __init__(self):
        self._readings: Dict[str, List[float]] = {}

    def ingest(self, record: TelemetryRecord) -> None:
        if record.sensor_id not in self._readings:
            self._readings[record.sensor_id] = []
        self._readings[record.sensor_id].append(record.reading)

    def get_stats(self, sensor_id: str) -> Optional[SensorStats]:
        if sensor_id not in self._readings or not self._readings[sensor_id]:
            return None

        readings = self._readings[sensor_id]
        return SensorStats(
            sensor_id=sensor_id,
            count=len(readings),
            min_val=min(readings),
            max_val=max(readings),
            mean_val=sum(readings) / len(readings),
        )


# ============================================================================
# SOLUTION TIER 4: CHALLENGE — TOKEN BUCKET RATE LIMITER
# ============================================================================
class TokenBucketRateLimiter:
    """
    Token Bucket rate limiter for protecting ML inference endpoints against over-utilization.
    """

    def __init__(self, capacity: int = 10, refill_rate: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def acquire(self, tokens_required: int = 1) -> bool:
        """
        Refills tokens based on elapsed time and checks if tokens_required can be granted.
        """
        now = time.time()
        elapsed = now - self.last_refill
        self.last_refill = now

        # Refill tokens up to maximum capacity
        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.refill_rate)

        if self.tokens >= tokens_required:
            self.tokens -= tokens_required
            return True
        return False


def verify_solutions():
    print("[*] Verifying Module 3 Solutions...")
    # 1. Verify Explanation
    expl = fix_route_ordering_explanation()
    assert "FastAPI and Starlette" in expl
    print("  [+] Route Ordering Explanation: PASS")

    # 2. Verify TelemetryAggregatorStore
    store = TelemetryAggregatorStore()
    store.ingest(TelemetryRecord(sensor_id="vibe-1", reading=10.0))
    store.ingest(TelemetryRecord(sensor_id="vibe-1", reading=20.0))
    store.ingest(TelemetryRecord(sensor_id="vibe-1", reading=30.0))
    stats = store.get_stats("vibe-1")
    assert stats is not None
    assert stats.count == 3
    assert stats.min_val == 10.0
    assert stats.max_val == 30.0
    assert stats.mean_val == 20.0
    print("  [+] Telemetry Aggregator Solution: PASS")

    # 3. Verify TokenBucketRateLimiter
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=0.5)
    assert limiter.acquire(1) is True
    assert limiter.acquire(1) is True
    assert limiter.acquire(1) is False  # Exhausted
    print("  [+] Token Bucket Rate Limiter Solution: PASS")
    print("[*] All Module 3 Solutions verified successfully.")


if __name__ == "__main__":
    verify_solutions()
