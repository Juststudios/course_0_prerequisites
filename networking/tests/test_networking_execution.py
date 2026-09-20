"""
test_networking_execution.py
============================
Live execution and functional tests for Level 6 Networking.
Uses ephemeral ports (port 0) for all socket and HTTP server tests to guarantee
collision-free execution, and Starlette TestClient for FastAPI services.
"""

import importlib.util
import socket
import struct
import threading
import time
from pathlib import Path
import pytest
from starlette.testclient import TestClient

NETWORKING_ROOT = Path(__file__).resolve().parent.parent


def _import_by_path(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ============================================================================
# 1. TCP Server and Client Tests
# ============================================================================
def test_tcp_server_and_client():
    server_mod = _import_by_path(NETWORKING_ROOT / "01_tcp_ip" / "01_tcp_server.py", "tcp_server")
    client_mod = _import_by_path(NETWORKING_ROOT / "01_tcp_ip" / "02_tcp_client.py", "tcp_client")

    server = server_mod.TCPEchoServer(port=0)
    bound_port = server.start()
    assert bound_port > 0, "Server failed to bind to an ephemeral port"

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        with client_mod.TCPClient(port=bound_port, timeout=3.0) as client:
            test_msg = b"Hello Pytest TCP"
            resp = client.send_and_receive(test_msg)
            assert resp == test_msg, f"Echo mismatch: {resp} != {test_msg}"

            test_large = b"X" * 10000
            resp_large = client.send_and_receive(test_large)
            assert resp_large == test_large, "Failed large payload framed transfer"
    finally:
        server.stop()


# ============================================================================
# 2. UDP Sockets Tests
# ============================================================================
def test_udp_sockets():
    udp_mod = _import_by_path(NETWORKING_ROOT / "01_tcp_ip" / "03_udp_sockets.py", "udp_sockets")

    server = udp_mod.UDPServer(port=0)
    bound_port = server.start()
    assert bound_port > 0

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        client = udp_mod.UDPClient(target_port=bound_port, timeout=2.0)
        ack = client.send_telemetry(sensor_id="test_sensor", value=99.9, seq=1)
        assert ack is not None
        assert ack.get("status") == "ACK"
        assert ack.get("seq") == 1
        client.close()
    finally:
        server.stop()


# ============================================================================
# 3. Concurrent Multi-Client Server Tests
# ============================================================================
def test_concurrent_tcp_server():
    conc_mod = _import_by_path(NETWORKING_ROOT / "01_tcp_ip" / "04_concurrent_server.py", "concurrent_server")

    server = conc_mod.ConcurrentTCPServer(port=0)
    port = server.start()
    assert port > 0

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    errors = []

    def client_task(client_id: int):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", port))
            msg = f"Worker {client_id}".encode()
            frame = struct.pack("!I", len(msg)) + msg
            s.sendall(frame)

            hdr = s.recv(4)
            (length,) = struct.unpack("!I", hdr)
            reply = s.recv(length)
            if reply != msg:
                errors.append(f"Mismatch for client {client_id}: {reply} != {msg}")
            s.close()
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=client_task, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    server.stop()
    assert len(errors) == 0, f"Concurrent clients experienced errors: {errors}"
    assert server.total_connections >= 5


# ============================================================================
# 4. Raw HTTP Client Tests
# ============================================================================
def test_raw_http_client():
    raw_mod = _import_by_path(NETWORKING_ROOT / "02_http_protocols" / "01_raw_http_client.py", "raw_http")

    port_box = []
    stop_event = threading.Event()
    t = threading.Thread(target=raw_mod._run_mock_http_server, args=(port_box, stop_event), daemon=True)
    t.start()
    time.sleep(0.1)

    port = port_box[0]
    client = raw_mod.RawHTTPClient()

    try:
        resp = client.get("127.0.0.1", port, "/health")
        assert resp.status_code == 200
        assert "healthy" in resp.text

        post_body = b"Payload data"
        resp_post = client.post("127.0.0.1", port, "/echo", body=post_body)
        assert resp_post.status_code == 201
        assert resp_post.body == post_body
    finally:
        stop_event.set()


# ============================================================================
# 5. Python HTTP Server Tests
# ============================================================================
def test_python_http_server():
    py_server_mod = _import_by_path(NETWORKING_ROOT / "02_http_protocols" / "02_python_http_server.py", "py_http_server")
    import requests

    server = py_server_mod.PythonHTTPServer(port=0)
    port = server.start()
    base_url = f"http://127.0.0.1:{port}"

    try:
        # GET /health
        res_health = requests.get(f"{base_url}/health", timeout=3.0)
        assert res_health.status_code == 200
        assert res_health.json()["status"] == "ok"

        # POST /api/items
        res_post = requests.post(f"{base_url}/api/items", json={"name": "Pressure Sensor"}, timeout=3.0)
        assert res_post.status_code == 201
        created_id = res_post.json()["id"]

        # GET /api/items/<id>
        res_get = requests.get(f"{base_url}/api/items/{created_id}", timeout=3.0)
        assert res_get.status_code == 200
        assert res_get.json()["name"] == "Pressure Sensor"
    finally:
        server.stop()


# ============================================================================
# 6. REST Principles ModelRegistryStore Tests
# ============================================================================
def test_rest_principles_store():
    rest_mod = _import_by_path(NETWORKING_ROOT / "03_rest_apis" / "01_rest_principles.py", "rest_principles")
    store = rest_mod.ModelRegistryStore()

    # List
    res_list = store.list_models()
    assert res_list.status_code == 200
    assert res_list.data["total"] >= 2

    # Create
    create_payload = {"id": "pytest-model", "name": "Test Model", "framework": "scikit-learn"}
    res_create = store.create_model(create_payload)
    assert res_create.status_code == 201
    assert "Location" in res_create.headers

    # Read
    res_read = store.get_model("pytest-model")
    assert res_read.status_code == 200
    assert res_read.data["name"] == "Test Model"

    # Delete
    res_del = store.delete_model("pytest-model")
    assert res_del.status_code == 204

    # Verify Not Found
    res_404 = store.get_model("pytest-model")
    assert res_404.status_code == 404


# ============================================================================
# 7. FastAPI Sensor Gateway Endpoints Tests (via Starlette TestClient)
# ============================================================================
def test_fastapi_sensor_endpoints():
    app_mod = _import_by_path(NETWORKING_ROOT / "03_rest_apis" / "02_fastapi_endpoints.py", "fastapi_app")
    client = TestClient(app_mod.app)

    # Health
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "healthy"
    assert "X-Process-Time-Ms" in r_health.headers

    # Create Sensor
    sensor_data = {
        "name": "Optical Strain Gauge",
        "sensor_type": "optical",
        "sampling_rate_hz": 200,
        "location": "Wing Box Spar",
    }
    r_create = client.post("/sensors", json=sensor_data)
    assert r_create.status_code == 201
    s_id = r_create.json()["id"]

    # Get Sensor
    r_get = client.get(f"/sensors/{s_id}")
    assert r_get.status_code == 200
    assert r_get.json()["name"] == "Optical Strain Gauge"

    # Delete Sensor
    r_del = client.delete(f"/sensors/{s_id}")
    assert r_del.status_code == 204


# ============================================================================
# 8. ML Model Serving Microservice Tests (via Starlette TestClient)
# ============================================================================
def test_ml_model_serving_microservice():
    ml_mod = _import_by_path(NETWORKING_ROOT / "03_rest_apis" / "03_ml_model_serving.py", "ml_serving")
    client = TestClient(ml_mod.app)

    # Health & Readiness
    r_health = client.get("/healthz")
    assert r_health.status_code == 200

    r_ready = client.get("/readyz")
    assert r_ready.status_code == 200
    assert r_ready.json()["status"] == "ready"

    # Model Info
    r_info = client.get("/model/info")
    assert r_info.status_code == 200
    assert "feature_names" in r_info.json()
    assert r_info.json()["training_accuracy"] > 0.9

    # Single Inference (Normal Sample)
    sample_normal = {
        "machine_id": "M_TEST_01",
        "temperature_c": 35.0,
        "vibration_rms": 1.2,
        "acoustic_peak_db": 22.0,
        "rotational_speed_rpm": 1800.0,
    }
    r_pred = client.post("/predict", json=sample_normal)
    assert r_pred.status_code == 200
    data = r_pred.json()
    assert data["machine_id"] == "M_TEST_01"
    assert data["anomaly_detected"] is False
    assert "inference_latency_ms" in data

    # Batch Inference
    sample_anom = {
        "machine_id": "M_TEST_02",
        "temperature_c": 98.0,
        "vibration_rms": 12.0,
        "acoustic_peak_db": 85.0,
        "rotational_speed_rpm": 1750.0,
    }
    r_batch = client.post("/predict/batch", json={"samples": [sample_normal, sample_anom]})
    assert r_batch.status_code == 200
    b_data = r_batch.json()
    assert b_data["total_samples"] == 2
    assert len(b_data["predictions"]) == 2
    assert b_data["predictions"][1]["anomaly_detected"] is True


# ============================================================================
# 9. Reference Solutions Verification Tests
# ============================================================================
def test_all_solutions_execute_cleanly():
    tcp_sol = _import_by_path(NETWORKING_ROOT / "solutions" / "tcp_ip_solutions.py", "sol_tcp")
    tcp_sol.verify_solutions()

    http_sol = _import_by_path(NETWORKING_ROOT / "solutions" / "http_solutions.py", "sol_http")
    http_sol.verify_solutions()

    rest_sol = _import_by_path(NETWORKING_ROOT / "solutions" / "rest_api_solutions.py", "sol_rest")
    rest_sol.verify_solutions()
