"""
End-to-End Test Suite for Milestone M3: Level 6 Networking & TensorFlow Fundamentals.
Verifies TCP/IP Sockets, UDP Messaging, Concurrent Multi-Client Servers, HTTP Clients,
Python http.server, FastAPI REST Services, ML Model Serving, and TensorFlow/Keras Core.
Adheres to the 4-Tier Test Design Methodology.
"""

import importlib.util
import json
import os
import socket
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pytest
from starlette.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NETWORKING_DIR = REPO_ROOT / "networking"
TF_DIR = REPO_ROOT / "machine-learning" / "08_tensorflow_fundamentals"

# Ensure TF compatibility engine and networking modules are discoverable
if str(TF_DIR) not in sys.path:
    sys.path.insert(0, str(TF_DIR))
if str(NETWORKING_DIR) not in sys.path:
    sys.path.insert(0, str(NETWORKING_DIR))

import tf_compat  # noqa: F401
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def _load_submodule(rel_path: str, module_name: str):
    full_path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(module_name, str(full_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# =====================================================================
# TIER 1: FEATURE COVERAGE (Isolation & Primary Contracts)
# =====================================================================

@pytest.mark.tier1
@pytest.mark.m3
class TestTier1TCPServerClient:
    """Tier 1: Isolated TCP Echo Server and Client communication contracts."""

    def test_tcp_server_starts_and_binds_ephemeral_port(self):
        """TCPEchoServer bound to port 0 resolves to a positive ephemeral port."""
        server_mod = _load_submodule("networking/01_tcp_ip/01_tcp_server.py", "tcp_server_mod")
        server = server_mod.TCPEchoServer(port=0)
        port = server.start()
        try:
            assert port > 1024, f"Expected ephemeral port > 1024, got {port}"
            assert server.port == port
        finally:
            server.stop()

    def test_tcp_echo_round_trip_message(self):
        """TCPClient sends a framed message to TCPEchoServer and receives exact echo."""
        server_mod = _load_submodule("networking/01_tcp_ip/01_tcp_server.py", "tcp_server_mod_rt")
        client_mod = _load_submodule("networking/01_tcp_ip/02_tcp_client.py", "tcp_client_mod_rt")

        server = server_mod.TCPEchoServer(port=0)
        port = server.start()
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        try:
            with client_mod.TCPClient(host="127.0.0.1", port=port, timeout=3.0) as client:
                payload = b"Hello Industrial Edge Network!"
                echoed = client.send_and_receive(payload)
                assert echoed == payload
        finally:
            server.stop()

    def test_tcp_multi_message_framing(self):
        """Sequential framed messages on a single connection are preserved without boundary loss."""
        server_mod = _load_submodule("networking/01_tcp_ip/01_tcp_server.py", "tcp_server_mod_multi")
        client_mod = _load_submodule("networking/01_tcp_ip/02_tcp_client.py", "tcp_client_mod_multi")

        server = server_mod.TCPEchoServer(port=0)
        port = server.start()
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        try:
            with client_mod.TCPClient(host="127.0.0.1", port=port, timeout=3.0) as client:
                for i in range(5):
                    msg = f"Telemetry packet {i} - sensor_val={i*1.5}".encode("utf-8")
                    echoed = client.send_and_receive(msg)
                    assert echoed == msg
        finally:
            server.stop()


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1UDPSockets:
    """Tier 1: Isolated UDP Server and Client datagram telemetry contracts."""

    def test_udp_server_start_and_bind(self):
        """UDPServer binds to ephemeral port and reflects state."""
        udp_mod = _load_submodule("networking/01_tcp_ip/03_udp_sockets.py", "udp_mod_start")
        server = udp_mod.UDPServer(port=0)
        port = server.start()
        try:
            assert port > 1024
            assert server.port == port
        finally:
            server.stop()

    def test_udp_telemetry_send_and_ack(self):
        """UDPClient transmits sensor telemetry and receives valid ACK response."""
        udp_mod = _load_submodule("networking/01_tcp_ip/03_udp_sockets.py", "udp_mod_ack")
        server = udp_mod.UDPServer(port=0)
        port = server.start()
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        try:
            client = udp_mod.UDPClient(target_host="127.0.0.1", target_port=port, timeout=2.0)
            ack = client.send_telemetry(sensor_id="vibe_01", value=42.12, seq=7)
            assert ack is not None
            assert ack.get("status") == "ACK"
            assert ack.get("seq") == 7
            client.close()
        finally:
            server.stop()


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1ConcurrentServer:
    """Tier 1: Concurrent multi-threaded TCP server handling multiple simultaneous clients."""

    def test_concurrent_server_multiple_simultaneous_clients(self):
        """Multiple concurrent client threads send payloads simultaneously without data corruption."""
        conc_mod = _load_submodule("networking/01_tcp_ip/04_concurrent_server.py", "conc_server_mod")
        server = conc_mod.ConcurrentTCPServer(port=0)
        port = server.start()
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        errors = []
        num_workers = 6

        def worker(worker_id: int):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4.0)
                s.connect(("127.0.0.1", port))
                msg = f"Worker payload {worker_id}".encode("utf-8")
                header = struct.pack("!I", len(msg))
                s.sendall(header + msg)

                # Read response header
                resp_hdr = s.recv(4)
                resp_len = struct.unpack("!I", resp_hdr)[0]
                resp_body = s.recv(resp_len)
                if resp_body != msg:
                    errors.append(f"Worker {worker_id} echo mismatch: {resp_body} != {msg}")
                s.close()
            except Exception as e:
                errors.append(f"Worker {worker_id} exception: {e}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_workers)]
        for th in threads:
            th.start()
        for th in threads:
            th.join(timeout=5.0)

        server.stop()
        assert len(errors) == 0, f"Concurrent workers experienced errors: {errors}"


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1HTTPComponents:
    """Tier 1: Raw socket HTTP client and standard library Python http.server."""

    def test_raw_http_client_request_construction_and_parsing(self):
        """RawHTTPClient formats RFC 9112 HTTP/1.1 request and parses status line & headers."""
        raw_mod = _load_submodule("networking/02_http_protocols/01_raw_http_client.py", "raw_client_mod")
        client = raw_mod.RawHTTPClient(timeout=2.0)
        assert client.timeout == 2.0

        # Verify HTTPResponse data structure
        resp = raw_mod.HTTPResponse(
            status_code=200,
            status_message="OK",
            headers={"Content-Type": "application/json"},
            body=b'{"status": "ready"}'
        )
        assert resp.status_code == 200
        assert resp.text == '{"status": "ready"}'
        assert "200 OK" in repr(resp)

    def test_python_http_server_endpoints(self):
        """PythonHTTPServer handles GET /health, GET /api/items, and POST /api/items."""
        pyhttp_mod = _load_submodule("networking/02_http_protocols/02_python_http_server.py", "pyhttp_mod")
        import urllib.request

        server = pyhttp_mod.PythonHTTPServer(port=0)
        port = server.start()
        base_url = f"http://127.0.0.1:{port}"

        try:
            # 1. GET /health
            with urllib.request.urlopen(f"{base_url}/health") as r:
                assert r.status == 200
                data = json.loads(r.read().decode())
                assert data.get("status") == "ok"

            # 2. GET /api/items
            with urllib.request.urlopen(f"{base_url}/api/items") as r:
                assert r.status == 200
                data = json.loads(r.read().decode())
                assert "items" in data
                assert len(data["items"]) >= 2

            # 3. POST /api/items
            req = urllib.request.Request(
                f"{base_url}/api/items",
                data=json.dumps({"name": "Optic Sensor", "status": "active"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req) as r:
                assert r.status == 201
                created = json.loads(r.read().decode())
                assert created["name"] == "Optic Sensor"
                assert "id" in created
        finally:
            server.stop()


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1FastAPIEndpoints:
    """Tier 1: FastAPI telemetry gateway endpoints tested via TestClient."""

    @pytest.fixture
    def api_client(self):
        mod = _load_submodule("networking/03_rest_apis/02_fastapi_endpoints.py", "fastapi_ep_mod")
        return TestClient(mod.app), mod

    def test_fastapi_health_endpoint(self, api_client):
        """GET /health returns 200 with healthy status and registered sensor count."""
        client, _ = api_client
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"
        assert "registered_sensors" in body

    def test_fastapi_sensor_crud_lifecycle(self, api_client):
        """Register new sensor (POST), retrieve by ID (GET), update (PUT), and delete (DELETE)."""
        client, _ = api_client

        # CREATE
        payload = {
            "name": "Shaft Encoder Beta",
            "sensor_type": "optical",
            "sampling_rate_hz": 5000,
            "location": "Shaft Assembly",
        }
        res_create = client.post("/sensors", json=payload)
        assert res_create.status_code == 201
        created_data = res_create.json()
        sensor_id = created_data["id"]
        assert created_data["name"] == "Shaft Encoder Beta"

        # READ
        res_get = client.get(f"/sensors/{sensor_id}")
        assert res_get.status_code == 200
        assert res_get.json()["location"] == "Shaft Assembly"

        # UPDATE
        res_put = client.put(f"/sensors/{sensor_id}", json={"sampling_rate_hz": 8000})
        assert res_put.status_code == 200
        assert res_put.json()["sampling_rate_hz"] == 8000

        # DELETE
        res_del = client.delete(f"/sensors/{sensor_id}")
        assert res_del.status_code == 204

        # CONFIRM DELETED
        res_after = client.get(f"/sensors/{sensor_id}")
        assert res_after.status_code == 404

    def test_fastapi_query_filtering(self, api_client):
        """GET /sensors filters correctly by sensor_type and active status."""
        client, _ = api_client
        resp = client.get("/sensors?sensor_type=vibration&is_active=true")
        assert resp.status_code == 200
        sensors = resp.json()
        assert isinstance(sensors, list)
        for s in sensors:
            assert s["sensor_type"] == "vibration"
            assert s["is_active"] is True


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1MLModelServing:
    """Tier 1: ML Model Serving microservice with BearingFaultModel and FastAPI."""

    @pytest.fixture
    def ml_client(self):
        mod = _load_submodule("networking/03_rest_apis/03_ml_model_serving.py", "ml_serving_mod")
        return TestClient(mod.app), mod

    def test_bearing_fault_model_standalone_predictions(self, ml_client):
        """BearingFaultModel computes probabilities and returns binary classification."""
        _, mod = ml_client
        model = mod.BearingFaultModel()
        assert model.is_ready is True
        assert len(model.feature_names) == 4

        # Healthy nominal sample: [Temp, Vib, Acoustic, RPM]
        healthy_features = [40.0, 1.2, 30.0, 1800.0]
        pred_h, prob_h = model.predict(healthy_features)
        assert pred_h == 0
        assert prob_h < 0.50

        # Faulty anomaly sample: high vibration & acoustic
        fault_features = [95.0, 6.5, 65.0, 1750.0]
        pred_f, prob_f = model.predict(fault_features)
        assert pred_f == 1
        assert prob_f > 0.50

    def test_bearing_fault_api_single_inference(self, ml_client):
        """POST /predict validates payload, executes inference, and tracks latency."""
        client, _ = ml_client
        payload = {
            "machine_id": "PUMP-402",
            "temperature_c": 52.0,
            "vibration_rms": 2.1,
            "acoustic_peak_db": 38.0,
            "rotational_speed_rpm": 1800.0
        }
        res = client.post("/predict", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["machine_id"] == "PUMP-402"
        assert "anomaly_detected" in data
        assert "fault_probability" in data
        assert "inference_latency_ms" in data
        assert data["inference_latency_ms"] >= 0.0

    def test_bearing_fault_api_batch_inference(self, ml_client):
        """POST /predict/batch scores multiple telemetry vectors and returns summary."""
        client, _ = ml_client
        samples = [
            {"machine_id": "M1", "temperature_c": 40.0, "vibration_rms": 1.0, "acoustic_peak_db": 25.0, "rotational_speed_rpm": 1800.0},
            {"machine_id": "M2", "temperature_c": 92.0, "vibration_rms": 6.8, "acoustic_peak_db": 60.0, "rotational_speed_rpm": 1720.0},
        ]
        res = client.post("/predict/batch", json={"samples": samples})
        assert res.status_code == 200
        data = res.json()
        assert data["total_samples"] == 2
        assert len(data["predictions"]) == 2
        assert data["predictions"][0]["anomaly_detected"] is False
        assert data["predictions"][1]["anomaly_detected"] is True

    def test_bearing_fault_api_probes_and_info(self, ml_client):
        """Liveness (/healthz), Readiness (/readyz), and Model Info (/model/info) respond accurately."""
        client, _ = ml_client
        assert client.get("/healthz").status_code == 200
        assert client.get("/readyz").status_code == 200

        info = client.get("/model/info").json()
        assert info["model_name"] == "industrial_bearing_fault_classifier"
        assert info["training_accuracy"] > 0.90
        assert len(info["feature_names"]) == 4


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1TensorFlowTensorsAndAutodiff:
    """Tier 1: TensorFlow tensors, Variables, and GradientTape automatic differentiation."""

    def test_tf_constant_properties_and_immutability(self):
        """tf.constant creates immutable multi-dimensional tensors with correct dtypes."""
        t_scalar = tf.constant(42.0, dtype=tf.float32)
        assert t_scalar.ndim == 0
        assert t_scalar.shape == ()

        t_mat = tf.constant([[1.0, 2.0], [3.0, 4.0]], dtype=tf.float32)
        assert t_mat.shape == (2, 2)
        assert t_mat.ndim == 2

        # Cast
        t_int = tf.cast(t_mat, tf.int32)
        assert t_int.dtype == tf.int32

    def test_tf_variable_mutable_operations(self):
        """tf.Variable supports in-place assign, assign_add, and assign_sub."""
        v = tf.Variable(10.0, dtype=tf.float32)
        assert np.isclose(v.numpy(), 10.0)

        v.assign(25.0)
        assert np.isclose(v.numpy(), 25.0)

        v.assign_add(5.0)
        assert np.isclose(v.numpy(), 30.0)

        v.assign_sub(12.0)
        assert np.isclose(v.numpy(), 18.0)

    def test_tf_gradient_tape_scalar_derivative(self):
        """GradientTape evaluates exact analytical derivative dy/dx = 2x."""
        x = tf.Variable(3.5, dtype=tf.float32)
        with tf.GradientTape() as tape:
            y = x * x
        grad = tape.gradient(y, x)
        assert np.isclose(grad.numpy(), 7.0, atol=1e-4)

    def test_tf_gradient_tape_multivariable_gradients(self):
        """GradientTape evaluates multi-variable gradients dz/du = 6u^2, dz/dv = 2v."""
        u = tf.Variable(2.0, dtype=tf.float32)
        v = tf.Variable(5.0, dtype=tf.float32)
        with tf.GradientTape() as tape:
            z = 2.0 * (u * u * u) + (v * v)
        du, dv = tape.gradient(z, [u, v])
        assert np.isclose(du.numpy(), 24.0, atol=1e-4)
        assert np.isclose(dv.numpy(), 10.0, atol=1e-4)

    def test_tf_gradient_tape_watch_constant(self):
        """tape.watch() tracks non-Variable constant tensors during differentiation."""
        c = tf.constant(4.0, dtype=tf.float32)
        with tf.GradientTape() as tape:
            tape.watch(c)
            y = c * c * c  # dy/dc = 3 c^2 = 3 * 16 = 48
        grad = tape.gradient(y, c)
        assert np.isclose(grad.numpy(), 48.0, atol=1e-4)


@pytest.mark.tier1
@pytest.mark.m3
class TestTier1TensorFlowKerasModels:
    """Tier 1: Keras Sequential, Functional, and Subclassed model architectures."""

    def test_keras_sequential_model_build_and_forward(self):
        """Sequential model chains layers and computes correct forward activation shapes."""
        model = keras.Sequential([
            layers.Dense(16, activation="relu"),
            layers.Dense(4, activation="softmax")
        ])
        x = tf.constant(np.random.randn(8, 10).astype(np.float32))
        out = model(x)
        assert out.shape == (8, 4)
        # Softmax outputs must sum to 1.0 along class dimension
        row_sums = np.sum(out.numpy(), axis=1)
        assert np.allclose(row_sums, 1.0, atol=1e-4)

    def test_keras_functional_model_residual_connection(self):
        """Functional API supports residual skip connections (output = F(x) + x)."""
        inputs = keras.Input(shape=(8,))
        h1 = layers.Dense(8, activation="relu")(inputs)
        h2 = layers.Dense(8, activation="relu")(h1)
        outputs = h2 + inputs
        res_model = keras.Model(inputs=inputs, outputs=outputs)

        x = tf.constant(np.ones((4, 8), dtype=np.float32))
        out = res_model(x)
        assert out.shape == (4, 8)

    def test_keras_subclassed_model_custom_call(self):
        """Subclassed Keras model overrides call() with explicit training parameter."""
        class CustomClassifier(keras.Model):
            def __init__(self, units=16, num_classes=3):
                super().__init__()
                self.dense = layers.Dense(units, activation="relu")
                self.dropout = layers.Dropout(0.2)
                self.out = layers.Dense(num_classes, activation="softmax")

            def call(self, inputs, training=False):
                h = self.dense(inputs)
                h = self.dropout(h, training=training)
                return self.out(h)

        model = CustomClassifier(units=12, num_classes=3)
        x = tf.constant(np.random.randn(5, 6).astype(np.float32))
        out_eval = model(x, training=False)
        out_train = model(x, training=True)
        assert out_eval.shape == (5, 3)
        assert out_train.shape == (5, 3)

    def test_keras_losses_and_optimizer_step(self):
        """Loss computation and optimizer.apply_gradients updates model parameters."""
        w = tf.Variable([[2.0], [3.0]], dtype=tf.float32)
        b = tf.Variable([1.0], dtype=tf.float32)
        optimizer = keras.optimizers.SGD(learning_rate=0.1)

        x = tf.constant([[1.0, 2.0]], dtype=tf.float32)
        y_true = tf.constant([[15.0]], dtype=tf.float32)
        mse_loss_fn = keras.losses.MeanSquaredError()

        with tf.GradientTape() as tape:
            y_pred = tf.matmul(x, w) + b
            loss = mse_loss_fn(y_true, y_pred)

        grads = tape.gradient(loss, [w, b])
        initial_w = w.numpy().copy()
        optimizer.apply_gradients(zip(grads, [w, b]))
        # Weights should have shifted towards reducing error
        assert not np.allclose(w.numpy(), initial_w)


# =====================================================================
# TIER 2: BOUNDARIES & CORNER CASES
# =====================================================================

@pytest.mark.tier2
@pytest.mark.m3
class TestTier2NetworkingTFBoundaries:
    """Tier 2: Boundary values, empty payloads, timeouts, and extreme tensor shapes."""

    def test_tcp_empty_payload_framing(self):
        """TCP server ignores empty payload without error, subsequent framed message succeeds."""
        server_mod = _load_submodule("networking/01_tcp_ip/01_tcp_server.py", "tcp_srv_empty")
        client_mod = _load_submodule("networking/01_tcp_ip/02_tcp_client.py", "tcp_cli_empty")

        server = server_mod.TCPEchoServer(port=0)
        port = server.start()
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        try:
            with client_mod.TCPClient(host="127.0.0.1", port=port, timeout=2.0) as client:
                # Send empty framed payload: server safely skips echo for 0-length without crashing
                client.send_framed(b"")
                # Immediately follow with a valid framed message
                resp = client.send_and_receive(b"Resilient Edge Sensor")
                assert resp == b"Resilient Edge Sensor"
        finally:
            server.stop()

    def test_tcp_large_payload_framing(self):
        """TCP framing transmits large payload (64 KB) across multiple socket packets."""
        server_mod = _load_submodule("networking/01_tcp_ip/01_tcp_server.py", "tcp_srv_large")
        client_mod = _load_submodule("networking/01_tcp_ip/02_tcp_client.py", "tcp_cli_large")

        server = server_mod.TCPEchoServer(port=0)
        port = server.start()
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()

        try:
            with client_mod.TCPClient(host="127.0.0.1", port=port, timeout=4.0) as client:
                large_msg = b"Z" * (64 * 1024)  # 64 KB
                resp = client.send_and_receive(large_msg)
                assert len(resp) == 64 * 1024
                assert resp == large_msg
        finally:
            server.stop()

    def test_tcp_client_connection_timeout(self):
        """Connecting to an unreachable port raises socket timeout or connection failure."""
        client_mod = _load_submodule("networking/01_tcp_ip/02_tcp_client.py", "tcp_cli_timeout")
        # Find a free port and do NOT listen on it
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            unused_port = s.getsockname()[1]

        with pytest.raises((ConnectionRefusedError, socket.timeout, TimeoutError, OSError)):
            with client_mod.TCPClient(host="127.0.0.1", port=unused_port, timeout=0.5) as client:
                client.send_and_receive(b"Hello?")

    def test_fastapi_schema_boundary_validation(self):
        """FastAPI endpoints return 422 Unprocessable Entity on schema validation violations."""
        mod = _load_submodule("networking/03_rest_apis/02_fastapi_endpoints.py", "fastapi_bnd_mod")
        client = TestClient(mod.app)

        # Name too short (< 2 chars)
        res_short_name = client.post("/sensors", json={
            "name": "X",
            "sensor_type": "vibe",
            "sampling_rate_hz": 100
        })
        assert res_short_name.status_code == 422

        # Sampling rate out of bounds (> 100,000 Hz)
        res_excess_hz = client.post("/sensors", json={
            "name": "Ultra Fast",
            "sensor_type": "vibe",
            "sampling_rate_hz": 500000
        })
        assert res_excess_hz.status_code == 422

    def test_ml_serving_empty_batch_boundary(self):
        """POST /predict/batch with empty sample list triggers 422 due to min_length=1."""
        mod = _load_submodule("networking/03_rest_apis/03_ml_model_serving.py", "ml_srv_bnd_mod")
        client = TestClient(mod.app)
        res = client.post("/predict/batch", json={"samples": []})
        assert res.status_code == 422

    def test_tf_extreme_tensor_shapes(self):
        """Tensor operations handle 0-D scalar, 1-element, and large high-dimensional tensors."""
        # 0-D scalar
        s = tf.constant(9.99)
        assert s.shape == ()
        assert s.ndim == 0
        assert np.isclose(s.numpy(), 9.99)

        # 1-element (1, 1, 1)
        cube = tf.constant([[[7.5]]])
        assert cube.shape == (1, 1, 1)
        assert np.isclose(cube.numpy()[0, 0, 0], 7.5)

        # Large batch (1000, 20)
        large = tf.constant(np.ones((1000, 20), dtype=np.float32))
        assert large.shape == (1000, 20)
        reduced = tf.reduce_mean(large, axis=0)
        assert reduced.shape == (20,)
        assert np.allclose(reduced.numpy(), 1.0)


# =====================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS (Pairwise & Integration)
# =====================================================================

@pytest.mark.tier3
@pytest.mark.m3
class TestTier3NetworkingTFCrossFeatures:
    """Tier 3: Pairwise combinations across Networking and TensorFlow components."""

    def test_raw_http_client_against_live_python_http_server(self):
        """RawHTTPClient executes GET and POST over raw TCP socket against PythonHTTPServer."""
        raw_mod = _load_submodule("networking/02_http_protocols/01_raw_http_client.py", "raw_client_cross")
        pyhttp_mod = _load_submodule("networking/02_http_protocols/02_python_http_server.py", "pyhttp_cross")

        server = pyhttp_mod.PythonHTTPServer(port=0)
        port = server.start()
        client = raw_mod.RawHTTPClient(timeout=3.0)

        try:
            # 1. GET /health
            resp_health = client.request("GET", "127.0.0.1", port, path="/health")
            assert resp_health.status_code == 200
            data_health = json.loads(resp_health.text)
            assert data_health.get("status") == "ok"

            # 2. POST /api/items
            item_body = json.dumps({"name": "Cross-Feature Piezo Sensor", "status": "active"}).encode("utf-8")
            resp_post = client.request(
                "POST", "127.0.0.1", port, path="/api/items",
                headers={"Content-Type": "application/json"},
                body=item_body
            )
            assert resp_post.status_code == 201
            data_post = json.loads(resp_post.text)
            assert data_post["name"] == "Cross-Feature Piezo Sensor"
            assert "id" in data_post
        finally:
            server.stop()

    def test_keras_model_served_over_fastapi_rest_service(self):
        """Trained Keras model encapsulated in a FastAPI microservice and queried via TestClient."""
        from fastapi import FastAPI
        from pydantic import BaseModel

        # 1. Define and train miniature Keras model
        nn_model = keras.Sequential([
            layers.Dense(12, activation="relu"),
            layers.Dense(2, activation="softmax")
        ])
        # Warm up weights
        dummy = tf.constant(np.random.randn(4, 4).astype(np.float32))
        _ = nn_model(dummy)

        # 2. Wrap in a FastAPI service
        app = FastAPI(title="Keras Neural Network Inference Service")

        class SensorFeatures(BaseModel):
            features: List[float]

        @app.post("/predict_nn")
        def predict_nn(data: SensorFeatures):
            if len(data.features) != 4:
                return {"error": "Expected 4 features", "status": 400}
            t_in = tf.constant(np.array(data.features, dtype=np.float32).reshape(1, 4))
            probs = nn_model(t_in).numpy()[0]
            predicted_class = int(np.argmax(probs))
            return {
                "predicted_class": predicted_class,
                "probabilities": [float(p) for p in probs]
            }

        # 3. Test through TestClient
        client = TestClient(app)
        res = client.post("/predict_nn", json={"features": [1.5, -0.8, 2.3, 0.4]})
        assert res.status_code == 200
        body = res.json()
        assert "predicted_class" in body
        assert body["predicted_class"] in [0, 1]
        assert len(body["probabilities"]) == 2
        assert np.isclose(sum(body["probabilities"]), 1.0, atol=1e-4)

    def test_tf_gradient_tape_training_loop_with_keras_layers(self):
        """Custom GradientTape training loop optimizing Keras Sequential layers decreases loss."""
        np.random.seed(42)
        X = tf.constant(np.random.randn(100, 4).astype(np.float32))
        y = tf.constant((X.numpy()[:, 0] > 0).astype(np.float32).reshape(-1, 1))

        model = keras.Sequential([
            layers.Dense(8, activation="relu"),
            layers.Dense(1, activation="sigmoid")
        ])
        optimizer = keras.optimizers.Adam(learning_rate=0.05)
        loss_fn = keras.losses.BinaryCrossentropy()

        # Measure initial loss
        initial_loss = loss_fn(y, model(X)).numpy()

        # Run 15 optimization steps
        for _ in range(15):
            with tf.GradientTape() as tape:
                preds = model(X, training=True)
                step_loss = loss_fn(y, preds)
            grads = tape.gradient(step_loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

        final_loss = loss_fn(y, model(X)).numpy()
        assert final_loss < initial_loss, f"Loss did not decrease: {final_loss} >= {initial_loss}"


# =====================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (End-to-End Pipelines)
# =====================================================================

@pytest.mark.tier4
@pytest.mark.m3
class TestTier4NetworkingTFRealWorldScenarios:
    """Tier 4: End-to-end production pipelines and reference solutions execution."""

    def test_end_to_end_industrial_iot_serving_workflow(self):
        """Simulate edge IoT telemetry client streaming sensor packets to ML serving service."""
        mod = _load_submodule("networking/03_rest_apis/03_ml_model_serving.py", "ml_srv_e2e_mod")
        client = TestClient(mod.app)

        latencies = []
        anomaly_count = 0

        # Simulate 20 successive telemetry payloads
        for i in range(20):
            t_start = time.perf_counter()
            # Alternating between normal operation and bearing degradation
            is_faulty = (i % 5 == 0)
            payload = {
                "machine_id": f"TURBINE-EDGE-{i:03d}",
                "temperature_c": 85.0 if is_faulty else 48.0,
                "vibration_rms": 5.5 if is_faulty else 1.8,
                "acoustic_peak_db": 55.0 if is_faulty else 32.0,
                "rotational_speed_rpm": 1780.0
            }
            resp = client.post("/predict", json=payload)
            dt_ms = (time.perf_counter() - t_start) * 1000.0
            latencies.append(dt_ms)

            assert resp.status_code == 200
            data = resp.json()
            if data["anomaly_detected"]:
                anomaly_count += 1

        # Performance & logic assertions
        p95_latency = np.percentile(latencies, 95)
        assert p95_latency < 50.0, f"P95 inference latency {p95_latency:.2f} ms exceeded 50 ms budget"
        assert anomaly_count > 0, "Expected anomalies detected during simulated degraded operations"

    def test_tf_end_to_end_mlp_classifier_workflow(self):
        """Execute complete TensorFlow MLP classifier training, evaluation, and weight saving."""
        np.random.seed(1337)
        # Synthetic binary classification dataset
        X = np.random.randn(200, 6).astype(np.float32)
        y = ((X[:, 0] + X[:, 1] * 1.2 - X[:, 2] * 0.7) > 0).astype(np.float32).reshape(-1, 1)

        model = keras.Sequential([
            layers.Dense(16, activation="relu"),
            layers.Dropout(0.1),
            layers.Dense(1, activation="sigmoid")
        ])
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.02),
            loss=keras.losses.BinaryCrossentropy(),
            metrics=["accuracy"]
        )

        history = model.fit(X, y, epochs=15, batch_size=32, verbose=0)
        assert "loss" in history.history

        # Evaluate performance on training set
        preds = model(tf.constant(X)).numpy()
        pred_labels = (preds >= 0.5).astype(np.float32)
        acc = float(np.mean(pred_labels == y))
        assert acc >= 0.75, f"Expected training accuracy >= 75%, got {acc*100:.2f}%"

    def test_networking_reference_solutions_execution(self):
        """Execute Level 6 Networking reference solutions and verify 100% PASS outputs."""
        solutions = [
            NETWORKING_DIR / "solutions" / "tcp_ip_solutions.py",
            NETWORKING_DIR / "solutions" / "http_solutions.py",
            NETWORKING_DIR / "solutions" / "rest_api_solutions.py",
        ]
        for script in solutions:
            assert script.exists(), f"Reference solution script {script} missing"
            res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
            assert res.returncode == 0, f"Solution {script.name} failed with stderr: {res.stderr}"
            assert "verified successfully" in res.stdout, f"Solution {script.name} output missing success message"

    def test_tensorflow_fundamentals_reference_solutions_execution(self):
        """Execute TensorFlow Fundamentals reference solution and verify 100% PASS output."""
        tf_solution = REPO_ROOT / "machine-learning" / "solutions" / "tensorflow_fundamentals_solutions.py"
        assert tf_solution.exists(), f"TensorFlow solution script {tf_solution} missing"
        res = subprocess.run([sys.executable, str(tf_solution)], capture_output=True, text=True)
        assert res.returncode == 0, f"Solution {tf_solution.name} failed with stderr: {res.stderr}"
        assert "All Module 8 Solutions verified successfully" in res.stdout
