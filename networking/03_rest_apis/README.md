# Module 3: REST APIs & ML Model Serving

## 1. Introduction: REST & Modern Distributed APIs

Representational State Transfer (REST) is an architectural style defined in 2000 by Roy Fielding in his doctoral dissertation (*"Architectural Styles and the Design of Network-based Software Architectures"*). REST leverages the existing semantics and infrastructure of HTTP to build scalable, loosely-coupled distributed systems.

In machine learning and data engineering, REST APIs are the standard interface for:
- Serving model predictions to web and mobile clients
- Microservice communication in ML pipelines (feature extraction -> inference -> monitoring)
- Administering model registries (MLflow, BentoML, TorchServe)
- Telemetry and metrics streaming

---

## 2. The 6 REST Architectural Constraints

To be considered truly "RESTful", a system must adhere to 6 constraints:

```
┌─────────────────────────────────────────────────────────────┐
│                 6 REST Architectural Constraints            │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Client-Server             │ Strict separation of UI and  │
│                              │ data storage concerns        │
├──────────────────────────────┼──────────────────────────────┤
│ 2. Statelessness             │ No client session context on │
│                              │ server; every request self-  │
│                              │ contained                    │
├──────────────────────────────┼──────────────────────────────┤
│ 3. Cacheability              │ Responses explicitly marked  │
│                              │ cacheable or non-cacheable   │
├──────────────────────────────┼──────────────────────────────┤
│ 4. Layered System            │ Client cannot tell if talking│
│                              │ to end server or proxy/CDN   │
├──────────────────────────────┼──────────────────────────────┤
│ 5. Uniform Interface         │ Resource URIs, representations,│
│                              │ self-descriptive messages,   │
│                              │ HATEOAS hypermedia links     │
├──────────────────────────────┼──────────────────────────────┤
│ 6. Code-on-Demand (Optional) │ Server can temporarily extend│
│                              │ client via executable scripts│
└──────────────────────────────┴──────────────────────────────┘
```

---

## 3. The Richardson Maturity Model

Leonard Richardson developed a 4-tier model assessing the RESTful maturity of an API:

```
Level 3: Hypermedia Controls (HATEOAS)
         Responses include links to related valid next actions
         ▲
Level 2: HTTP Verbs & Status Codes
         Correct semantic use of GET, POST, PUT, DELETE, 200, 201, 404
         ▲
Level 1: Resources
         Individual URIs for individual entities (/models/1, /models/2)
         ▲
Level 0: The Swamp of POX (Plain Old XML/JSON)
         Single URI endpoint (/api), single verb (POST), RPC-style dispatch
```

Most modern production APIs operate at **Level 2**, with specialized systems implementing Level 3.

---

## 4. RESTful URL Design & Resource Modeling

### 4.1 URL Conventions
- **Use Nouns, Not Verbs**: Resources are entities, not actions.
  - Good: `POST /api/v1/models`
  - Bad: `POST /api/v1/createNewModel`
- **Use Plural Nouns for Collections**:
  - `GET /api/v1/sensors` (List sensors)
  - `GET /api/v1/sensors/42` (Retrieve sensor 42)
  - `POST /api/v1/sensors/42/readings` (Nested sub-resource)
- **Use Query Parameters for Filtering, Sorting, and Pagination**:
  - `GET /api/v1/sensors?status=active&sort=desc&limit=20&offset=40`

---

## 5. Modern API Frameworks: Why FastAPI?

Python offers multiple web frameworks (Flask, Django, FastAPI). For high-performance backend and ML serving, **FastAPI** has become the industry benchmark:

| Dimension | Flask | Django REST Framework | FastAPI |
|---|---|---|---|
| **Architecture** | Synchronous (WSGI) | Synchronous (WSGI) | Asynchronous (ASGI) |
| **Concurrency** | Thread-bound | Thread-bound | Native `async`/`await` event loop |
| **Validation** | Manual / Marshmallow | Serializer classes | **Pydantic** type annotations |
| **Documentation** | Manual plugins | Manual schema generation | **Automatic interactive OpenAPI / Swagger** |
| **Throughput** | Moderate | Moderate | High (on par with Go & NodeJS) |

---

## 6. Pydantic Data Validation

FastAPI relies on Pydantic to enforce data schemas at runtime. Pydantic parses incoming JSON payloads, validates data types and constraints, and produces structured error messages (HTTP 422) if validation fails:

```python
from pydantic import BaseModel, Field

class TelemetryInput(BaseModel):
    sensor_id: str = Field(..., min_length=3, max_length=32)
    temperature: float = Field(..., ge=-50.0, le=150.0, description="Celsius")
    vibration_hz: float = Field(..., ge=0.0, description="Vibration frequency")
```

---

## 7. REST Architecture for Machine Learning Serving

Serving ML models via REST requires careful engineering considerations:

```
Client (Web/Edge)
      │
      ▼ HTTP POST /v1/predict {"features": [1.2, 0.4, 3.1]}
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application Gateway               │
│                                                             │
│  1. Pydantic Schema Validation (Check types, bounds)        │
│  2. Security & Rate-Limiting (Token bucket)                 │
│  3. Middleware: Request Timer & Latency Metric Logging       │
│  4. Inference Execution (NumPy / Torch / Scikit-Learn)      │
│  5. Response Serialization & Headers Injection              │
└─────────────────────────────────────────────────────────────┘
      │
      ▼ HTTP 200 OK {"prediction": 1, "confidence": 0.96, "latency_ms": 1.4}
Client (Receives Prediction)
```

### Health Probes in Containerized Environments (Kubernetes)
- **`GET /healthz` (Liveness Probe)**: Verifies the web server process is alive and responsive. If it fails, the container is restarted.
- **`GET /readyz` (Readiness Probe)**: Verifies the ML model weights have been loaded into memory and the service is ready to process traffic.

---

## 8. Error Handling & Standard Error Envelopes

Never return raw internal Python tracebacks to API clients. A well-designed REST API returns a consistent error envelope:

```json
{
  "error": "ResourceNotFound",
  "detail": "Model with ID 'resnet-50' is not registered.",
  "status_code": 404,
  "timestamp": 1726588800.0
}
```

---

## 9. Next Steps
- Study `01_rest_principles.py` for from-scratch resource store concepts.
- Review `02_fastapi_endpoints.py` for production FastAPI practices.
- Explore `03_ml_model_serving.py` for serving an actual trained ML model.
