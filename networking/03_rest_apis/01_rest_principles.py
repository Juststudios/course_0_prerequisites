"""
01_rest_principles.py
=====================
Foundational demonstration of REST (Representational State Transfer) principles,
resource modeling, CRUD operations, and HTTP status code mappings in pure Python.

Demonstrates:
- Resource URI structuring and plural collection naming
- HTTP Verbs: GET (safe/idempotent), POST (unsafe/non-idempotent),
  PUT (unsafe/idempotent), PATCH (unsafe/non-idempotent), DELETE (unsafe/idempotent)
- Proper status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request,
  404 Not Found, 409 Conflict
- Standard JSON error envelope formatting
- Filtering, sorting, and pagination on collections
"""

import time
from typing import Dict, Any, List, Optional, Tuple


class RESTResponse:
    """Encapsulates status code, headers, and body of a simulated REST response."""

    def __init__(self, status_code: int, data: Any = None, headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code
        self.data = data
        self.headers = headers or {}

    def __repr__(self) -> str:
        return f"<RESTResponse [{self.status_code}] data={self.data}>"


class ModelRegistryStore:
    """
    An in-memory RESTful repository managing registered Machine Learning models.
    Demonstrates pure REST semantics without framework overhead.
    """

    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {
            "mod-001": {
                "id": "mod-001",
                "name": "vibration_anomaly_rf",
                "framework": "scikit-learn",
                "version": "1.0.0",
                "status": "production",
                "accuracy": 0.942,
                "created_at": 1726580000.0,
            },
            "mod-002": {
                "id": "mod-002",
                "name": "bearing_fault_mlp",
                "framework": "pytorch",
                "version": "0.9.1",
                "status": "staging",
                "accuracy": 0.915,
                "created_at": 1726584000.0,
            },
        }

    # =========================================================================
    # 1. GET /models - List & Filter Collection (Safe, Idempotent)
    # =========================================================================
    def list_models(
        self,
        framework: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> RESTResponse:
        """Retrieves a paginated list of models with optional filters."""
        results = list(self._models.values())

        if framework:
            results = [m for m in results if m["framework"].lower() == framework.lower()]
        if status:
            results = [m for m in results if m["status"].lower() == status.lower()]

        total_count = len(results)
        paginated = results[offset : offset + limit]

        body = {
            "items": paginated,
            "total": total_count,
            "limit": limit,
            "offset": offset,
        }
        return RESTResponse(status_code=200, data=body)

    # =========================================================================
    # 2. POST /models - Create New Resource (Unsafe, Non-idempotent)
    # =========================================================================
    def create_model(self, payload: Dict[str, Any]) -> RESTResponse:
        """Creates a new model resource."""
        required_fields = ["id", "name", "framework"]
        for field in required_fields:
            if field not in payload:
                return RESTResponse(
                    status_code=400,
                    data={"error": "ValidationError", "detail": f"Missing required field: {field}"},
                )

        model_id = payload["id"]
        if model_id in self._models:
            return RESTResponse(
                status_code=409,  # Conflict
                data={"error": "ConflictError", "detail": f"Model with ID '{model_id}' already exists."},
            )

        new_resource = {
            "id": model_id,
            "name": payload["name"],
            "framework": payload["framework"],
            "version": payload.get("version", "0.1.0"),
            "status": payload.get("status", "draft"),
            "accuracy": payload.get("accuracy", 0.0),
            "created_at": time.time(),
        }
        self._models[model_id] = new_resource

        headers = {"Location": f"/api/v1/models/{model_id}"}
        return RESTResponse(status_code=201, data=new_resource, headers=headers)

    # =========================================================================
    # 3. GET /models/{id} - Retrieve Single Resource (Safe, Idempotent)
    # =========================================================================
    def get_model(self, model_id: str) -> RESTResponse:
        """Retrieves a single model by unique identifier."""
        if model_id not in self._models:
            return RESTResponse(
                status_code=404,
                data={"error": "NotFoundError", "detail": f"Model '{model_id}' does not exist."},
            )
        return RESTResponse(status_code=200, data=self._models[model_id])

    # =========================================================================
    # 4. PUT /models/{id} - Complete Replacement (Unsafe, Idempotent)
    # =========================================================================
    def replace_model(self, model_id: str, payload: Dict[str, Any]) -> RESTResponse:
        """Completely replaces existing model resource or creates it if allowed."""
        if model_id not in self._models:
            return RESTResponse(
                status_code=404,
                data={"error": "NotFoundError", "detail": f"Model '{model_id}' does not exist."},
            )

        updated_resource = {
            "id": model_id,
            "name": payload.get("name", ""),
            "framework": payload.get("framework", "unknown"),
            "version": payload.get("version", "1.0.0"),
            "status": payload.get("status", "staging"),
            "accuracy": payload.get("accuracy", 0.0),
            "updated_at": time.time(),
        }
        self._models[model_id] = updated_resource
        return RESTResponse(status_code=200, data=updated_resource)

    # =========================================================================
    # 5. PATCH /models/{id} - Partial Modification (Unsafe, Non-idempotent)
    # =========================================================================
    def update_model_partial(self, model_id: str, updates: Dict[str, Any]) -> RESTResponse:
        """Modifies specific fields of an existing model resource."""
        if model_id not in self._models:
            return RESTResponse(
                status_code=404,
                data={"error": "NotFoundError", "detail": f"Model '{model_id}' does not exist."},
            )

        resource = self._models[model_id]
        for key, val in updates.items():
            if key != "id":  # Immutable primary key
                resource[key] = val

        resource["updated_at"] = time.time()
        return RESTResponse(status_code=200, data=resource)

    # =========================================================================
    # 6. DELETE /models/{id} - Remove Resource (Unsafe, Idempotent)
    # =========================================================================
    def delete_model(self, model_id: str) -> RESTResponse:
        """Deletes a model resource."""
        if model_id not in self._models:
            return RESTResponse(
                status_code=404,
                data={"error": "NotFoundError", "detail": f"Model '{model_id}' does not exist."},
            )
        del self._models[model_id]
        # 204 No Content has no body
        return RESTResponse(status_code=204, data=None)


def run_demo() -> None:
    print("=" * 60)
    print("REST ARCHITECTURAL PRINCIPLES DEMO")
    print("=" * 60)
    store = ModelRegistryStore()

    # 1. GET /models
    resp1 = store.list_models(status="production")
    print(f"1. GET /models?status=production -> {resp1.status_code}")
    print(f"   Items: {resp1.data['items']}")

    # 2. POST /models
    new_model = {"id": "mod-003", "name": "pump_seal_leak_xgb", "framework": "xgboost"}
    resp2 = store.create_model(new_model)
    print(f"\n2. POST /models -> {resp2.status_code} (Location: {resp2.headers.get('Location')})")
    print(f"   Created: {resp2.data}")

    # 3. PATCH /models/mod-003
    resp3 = store.update_model_partial("mod-003", {"accuracy": 0.961, "status": "production"})
    print(f"\n3. PATCH /models/mod-003 -> {resp3.status_code}")
    print(f"   Updated status: {resp3.data['status']}, accuracy: {resp3.data['accuracy']}")

    # 4. DELETE /models/mod-003
    resp4 = store.delete_model("mod-003")
    print(f"\n4. DELETE /models/mod-003 -> {resp4.status_code} No Content")

    # 5. GET /models/mod-003 (Should now be 404)
    resp5 = store.get_model("mod-003")
    print(f"\n5. GET /models/mod-003 (after delete) -> {resp5.status_code}")
    print(f"   Error Envelope: {resp5.data}")


if __name__ == "__main__":
    run_demo()
