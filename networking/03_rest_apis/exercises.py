"""
exercises.py
============
Level 6 Networking — Module 3: REST APIs & ML Model Serving
4-Tier Progressive Exercises:
- Tier 1: Recall & Architectural Constraints
- Tier 2: Understanding & Debugging (FastAPI Route Shadowing & Pydantic Bugs)
- Tier 3: Application (Telemetry Ingestion & Aggregation API)
- Tier 4: Challenge (Token Bucket Rate-Limited ML Inference Gateway)
"""

import time
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

print("=" * 70)
print("LEVEL 6 NETWORKING — MODULE 3: REST APIS & ML SERVING EXERCISES")
print("=" * 70)

# ============================================================================
# TIER 1: RECALL & ARCHITECTURAL CONSTRAINTS
# ============================================================================
"""
Questions:
1. What are the 6 architectural constraints defined by Roy Fielding for REST?
2. What are the 4 levels of the Richardson Maturity Model?
3. Why should a REST endpoint use nouns ('/models') instead of verbs ('/getModels')?
4. What is the difference between a Liveness probe (/healthz) and a Readiness probe (/readyz)
   in Kubernetes when deploying a Machine Learning inference microservice?
5. When should an API return HTTP 422 Unprocessable Entity instead of HTTP 400 Bad Request?
"""

def demo_tier1():
    print("\n--- TIER 1 DEMO: Richardson Maturity Model ---")
    levels = [
        "Level 0: The Swamp of POX (Single URI, single HTTP POST, RPC dispatch)",
        "Level 1: Resources (Individual URIs per entity, e.g. /models/1, /models/2)",
        "Level 2: HTTP Verbs & Status (Correct use of GET, POST, DELETE, 200, 201, 404)",
        "Level 3: Hypermedia Controls / HATEOAS (Self-descriptive navigable next steps)",
    ]
    for lvl in levels:
        print(f"  {lvl}")

demo_tier1()


# ============================================================================
# TIER 2: UNDERSTANDING & DEBUGGING
# ============================================================================
"""
The FastAPI snippet below contains 3 subtle API design and framework bugs:
- Bug 1: Route shadowing: '/sensors/{sensor_id}' is defined BEFORE '/sensors/statistics',
  causing requests to '/sensors/statistics' to fail validation because 'statistics' is
  parsed as an integer sensor_id!
- Bug 2: Python mutable default argument 'tags: list = []' in route definition.
- Bug 3: Using status_code=200 on a POST creation endpoint instead of 201 Created.
"""

buggy_fastapi_snippet = """
@app.get("/sensors/{sensor_id}")          # Bug 1: Route defined before static /sensors/statistics
def get_sensor(sensor_id: int):
    return {"id": sensor_id}

@app.get("/sensors/statistics")           # Shadowed by {sensor_id}! Never reached!
def get_sensor_statistics():
    return {"mean_temp": 42.0}

@app.post("/sensors", status_code=200)    # Bug 3: Should be 201 Created
def create_sensor(data: dict, tags: list = []):  # Bug 2: Mutable default argument
    return {"created": True}
"""

# Exercise 2 Starter:
def fix_route_ordering_explanation() -> str:
    """
    TODO for Student:
    Explain how FastAPI/Starlette evaluates routes (sequential declaration order)
    and why static path routes must be declared before parameterized path routes.
    """
    pass


# ============================================================================
# TIER 3: APPLICATION — TELEMETRY INGESTION & AGGREGATION REST API
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
    In-memory store ingesting sensor readings and computing live summary stats.
    """

    def __init__(self):
        self._readings: Dict[str, List[float]] = {}

    def ingest(self, record: TelemetryRecord) -> None:
        """TODO: Append reading to sensor_id list."""
        pass

    def get_stats(self, sensor_id: str) -> Optional[SensorStats]:
        """
        TODO: Compute count, min, max, mean for sensor_id.
        Return None if sensor_id has no readings.
        """
        pass


# ============================================================================
# TIER 4: CHALLENGE — TOKEN BUCKET RATE-LIMITED INFERENCE GATEWAY
# ============================================================================
class TokenBucketRateLimiter:
    """
    A Token Bucket rate limiter to protect ML model inference endpoints.
    - Capacity: maximum burst tokens allowed in the bucket.
    - Refill Rate: tokens added per second.
    """

    def __init__(self, capacity: int = 10, refill_rate: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def acquire(self, tokens_required: int = 1) -> bool:
        """
        TODO for Student:
        1. Calculate time passed since last_refill.
        2. Refill tokens: min(capacity, tokens + elapsed * refill_rate).
        3. If tokens >= tokens_required: deduct and return True.
        4. Else return False (rate limited / HTTP 429).
        """
        pass


if __name__ == "__main__":
    print("\n[!] Module 3 exercise templates loaded.")
    print("Refer to networking/solutions/rest_api_solutions.py for complete reference implementations.")
