"""
02_fastapi_endpoints.py
=======================
Production-grade RESTful API service built with FastAPI and Pydantic.

Demonstrates:
- FastAPI application initialization with OpenAPI metadata
- Pydantic models for request validation and response serialization
- HTTP verbs with accurate status codes (200, 201, 204, 404, 422)
- Query parameters with type constraints (ge, le)
- Path parameters with validation
- Asynchronous request timing middleware
- Direct executability via uvicorn and testability via Starlette TestClient
"""

import time
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status, Query, Request, Response
from pydantic import BaseModel, Field


# ============================================================================
# Pydantic Data Models
# ============================================================================
class SensorCreate(BaseModel):
    """Schema for registering a new sensor."""
    name: str = Field(..., min_length=2, max_length=64, description="Sensor descriptor")
    sensor_type: str = Field(..., description="E.g. vibration, temperature, acoustic")
    sampling_rate_hz: int = Field(100, ge=1, le=100000, description="Sampling frequency in Hz")
    location: str = Field("Main Bearing", description="Physical installation point")


class SensorUpdate(BaseModel):
    """Schema for updating an existing sensor."""
    name: Optional[str] = Field(None, min_length=2, max_length=64)
    sampling_rate_hz: Optional[int] = Field(None, ge=1, le=100000)
    location: Optional[str] = None
    is_active: Optional[bool] = None


class SensorResponse(BaseModel):
    """Schema for serialized sensor resource."""
    id: int
    name: str
    sensor_type: str
    sampling_rate_hz: int
    location: str
    is_active: bool
    created_at: float


# ============================================================================
# FastAPI Application & State
# ============================================================================
app = FastAPI(
    title="Industrial IoT Telemetry Sensor Gateway",
    description="REST API for registering, monitoring, and managing edge telemetry sensors.",
    version="1.0.0",
)

# In-memory storage for sensors
sensors_db: Dict[int, Dict[str, Any]] = {
    1: {
        "id": 1,
        "name": "Turbine Primary Vibrometer",
        "sensor_type": "vibration",
        "sampling_rate_hz": 1000,
        "location": "Turbine Stage 1",
        "is_active": True,
        "created_at": 1726580000.0,
    },
    2: {
        "id": 2,
        "name": "Cooling Line Pyrometer",
        "sensor_type": "temperature",
        "sampling_rate_hz": 10,
        "location": "Cooling Circuit B",
        "is_active": True,
        "created_at": 1726581000.0,
    },
}
next_sensor_id = 3


# ============================================================================
# Middleware: Request Timing
# ============================================================================
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000.0
    response.headers["X-Process-Time-Ms"] = f"{process_time:.3f}"
    return response


# ============================================================================
# Endpoints
# ============================================================================
@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Liveness probe returning service health."""
    return {"status": "healthy", "registered_sensors": len(sensors_db)}


@app.post(
    "/sensors",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Sensors"],
)
async def create_sensor(sensor_in: SensorCreate):
    """Registers a new sensor into the catalog."""
    global next_sensor_id
    sensor_id = next_sensor_id
    next_sensor_id += 1

    record = {
        "id": sensor_id,
        "name": sensor_in.name,
        "sensor_type": sensor_in.sensor_type,
        "sampling_rate_hz": sensor_in.sampling_rate_hz,
        "location": sensor_in.location,
        "is_active": True,
        "created_at": time.time(),
    }
    sensors_db[sensor_id] = record
    return record


@app.get("/sensors", response_model=List[SensorResponse], tags=["Sensors"])
async def list_sensors(
    sensor_type: Optional[str] = Query(None, description="Filter by sensor type"),
    is_active: Optional[bool] = Query(None, description="Filter active status"),
    skip: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, ge=1, le=100, description="Limit per page"),
):
    """Retrieves a paginated list of registered sensors with optional filters."""
    results = list(sensors_db.values())

    if sensor_type is not None:
        results = [s for s in results if s["sensor_type"].lower() == sensor_type.lower()]
    if is_active is not None:
        results = [s for s in results if s["is_active"] == is_active]

    return results[skip : skip + limit]


@app.get("/sensors/{sensor_id}", response_model=SensorResponse, tags=["Sensors"])
async def get_sensor(sensor_id: int):
    """Retrieves single sensor details by ID."""
    if sensor_id not in sensors_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id {sensor_id} does not exist.",
        )
    return sensors_db[sensor_id]


@app.put("/sensors/{sensor_id}", response_model=SensorResponse, tags=["Sensors"])
async def update_sensor(sensor_id: int, updates: SensorUpdate):
    """Updates fields of an existing sensor."""
    if sensor_id not in sensors_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id {sensor_id} does not exist.",
        )

    sensor = sensors_db[sensor_id]
    update_data = updates.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        sensor[key] = val

    return sensor


@app.delete(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Sensors"],
)
async def delete_sensor(sensor_id: int):
    """Deletes a sensor from the catalog."""
    if sensor_id not in sensors_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id {sensor_id} does not exist.",
        )
    del sensors_db[sensor_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============================================================================
# Demo Runner using Starlette TestClient (Zero-Socket Binding)
# ============================================================================
def run_demo() -> None:
    print("=" * 60)
    print("FASTAPI SENSOR GATEWAY DEMO (VIA TESTCLIENT)")
    print("=" * 60)
    from starlette.testclient import TestClient

    client = TestClient(app)

    # 1. Test Health
    resp_health = client.get("/health")
    print(f"1. GET /health -> {resp_health.status_code}: {resp_health.json()}")

    # 2. Test Create
    new_sensor_payload = {
        "name": "Gearbox Acoustic Emission",
        "sensor_type": "acoustic",
        "sampling_rate_hz": 5000,
        "location": "High-Speed Shaft",
    }
    resp_create = client.post("/sensors", json=new_sensor_payload)
    print(f"2. POST /sensors -> {resp_create.status_code}: {resp_create.json()}")
    created_id = resp_create.json()["id"]

    # 3. Test List
    resp_list = client.get("/sensors?limit=5")
    print(f"3. GET /sensors?limit=5 -> {resp_list.status_code}: {len(resp_list.json())} sensors returned")

    # 4. Test Update
    resp_upd = client.put(f"/sensors/{created_id}", json={"sampling_rate_hz": 8000})
    print(f"4. PUT /sensors/{created_id} -> {resp_upd.status_code}: new rate = {resp_upd.json()['sampling_rate_hz']}")

    # 5. Test Delete
    resp_del = client.delete(f"/sensors/{created_id}")
    print(f"5. DELETE /sensors/{created_id} -> {resp_del.status_code} (Empty content)")

    # 6. Verify Deleted
    resp_404 = client.get(f"/sensors/{created_id}")
    print(f"6. GET /sensors/{created_id} (after delete) -> {resp_404.status_code}: {resp_404.json()}")
    print("[*] FastAPI demo completed successfully!")


if __name__ == "__main__":
    run_demo()
