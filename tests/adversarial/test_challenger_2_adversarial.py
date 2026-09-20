"""
test_challenger_2_adversarial.py
================================
Adversarial Stress Testing & Empirical Verification Suite authored by Challenger 2.

Scope:
1. TCP/UDP Sockets & HTTP:
   - Connection refused handling & socket state cleanup
   - Zero-byte read / empty frames / empty stream disconnects
   - Client abrupt disconnect (partial frames, RST/hard close)
   - Malformed HTTP request parsing & error response verification
2. FastAPI REST APIs:
   - Invalid JSON payloads (type mismatches, corrupt body, missing fields)
   - Negative & out-of-bound sensor values (schema validation)
   - Boundary query limits (ge/le, offset boundaries, batch limits)
   - Highly concurrent requests (race condition & thread safety check)
3. TensorFlow / tf_compat:
   - Multi-variable GradientTape (gradient accuracy, unused sources)
   - Higher-order derivatives (nested tapes, 2nd & 3rd order derivatives)
   - Custom Keras training steps (zero grads, non-trainable vars, weight saving)
4. Reversi Capstone:
   - Full game to completion (validity, terminal state, score integrity)
   - Passes on no legal moves (consecutive passes == 1, turn toggle)
   - Double pass game termination (consecutive passes == 2, terminal resolution)
   - Board evaluation symmetry (PST symmetry, reflection invariance, heuristic negation)
5. Motor Control & Simulink ODE45:
   - Anti-windup clamping under sustained extreme overload
   - Severe bi-directional step disturbances
   - Zero damping (b = 0.0) stability & conservation
   - High stiffness / numerical stability of adaptive RK45
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import socket
import struct
import sys
import threading
import time
from typing import Dict, List, Tuple

import numpy as np
import pytest
from scipy.integrate import solve_ivp
from starlette.testclient import TestClient

# -----------------------------------------------------------------------------
# Path Configurations
# -----------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NETWORKING_DIR = REPO_ROOT / "networking"
ML_DIR = REPO_ROOT / "machine-learning"
GAME_AI_DIR = REPO_ROOT / "game-ai"
ENG_MATH_DIR = REPO_ROOT / "engineering-mathematics"

for p in [str(REPO_ROOT), str(NETWORKING_DIR), str(ML_DIR), str(GAME_AI_DIR), str(ENG_MATH_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_module(rel_path: str, module_name: str):
    full_path = REPO_ROOT / rel_path
    assert full_path.exists(), f"File does not exist: {full_path}"
    spec = importlib.util.spec_from_file_location(module_name, str(full_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# =============================================================================
# 1. TCP/UDP SOCKETS & HTTP ADVERSARIAL TESTS
# =============================================================================
class TestAdversarialNetworking:
    """Stress testing TCP/UDP sockets, clients, servers, and HTTP parsing."""

    @pytest.fixture(scope="class")
    def tcp_server_mod(self):
        return _load_module("networking/01_tcp_ip/01_tcp_server.py", "mod_adv_tcp_server")

    @pytest.fixture(scope="class")
    def tcp_client_mod(self):
        return _load_module("networking/01_tcp_ip/02_tcp_client.py", "mod_adv_tcp_client")

    @pytest.fixture(scope="class")
    def udp_mod(self):
        return _load_module("networking/01_tcp_ip/03_udp_sockets.py", "mod_adv_udp")

    @pytest.fixture(scope="class")
    def concurrent_server_mod(self):
        return _load_module("networking/01_tcp_ip/04_concurrent_server.py", "mod_adv_conc_server")

    @pytest.fixture(scope="class")
    def raw_http_mod(self):
        return _load_module("networking/02_http_protocols/01_raw_http_client.py", "mod_adv_raw_http")

    @pytest.fixture(scope="class")
    def http_server_mod(self):
        return _load_module("networking/02_http_protocols/02_python_http_server.py", "mod_adv_http_server")

    # 1.1 Socket Connection Refused & Half-Open Socket Bug
    def test_tcp_client_connection_refused_handling(self, tcp_client_mod):
        """Verify client raises ConnectionRefusedError on closed port and cleanly closes socket without leaking state."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 0))
        unused_port = s.getsockname()[1]
        s.close()

        client = tcp_client_mod.TCPClient(host="127.0.0.1", port=unused_port, timeout=0.5)

        with pytest.raises((ConnectionRefusedError, OSError)):
            client.connect()

        # Verified Remediation:
        # When connect() fails, self._sock is closed and set to None.
        # client.is_connected() must return False, preventing socket descriptor leaks.
        assert client.is_connected() is False
        assert client._sock is None
        client.close()
        assert not client.is_connected()

    # 1.2 Zero-Byte Read / 0-Length Payload
    def test_tcp_zero_byte_frame_and_recovery(self, tcp_server_mod, tcp_client_mod):
        """Send empty length-prefixed frame (payload_len=0) followed by a valid frame."""
        server = tcp_server_mod.TCPEchoServer(port=0, timeout=0.5)
        port = server.start()
        srv_thread = threading.Thread(target=server.serve_forever, daemon=True)
        srv_thread.start()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect(("127.0.0.1", port))

            # Send empty frame (4-byte header length = 0)
            sock.sendall(struct.pack("!I", 0))

            # Send valid frame immediately on the same connection
            msg = b"VALID_AFTER_ZERO"
            sock.sendall(struct.pack("!I", len(msg)) + msg)

            # Receive response: server skipped empty frame and echoed valid message
            hdr = sock.recv(4)
            assert len(hdr) == 4
            (rlen,) = struct.unpack("!I", hdr)
            assert rlen == len(msg)
            echoed = sock.recv(rlen)
            assert echoed == msg

            sock.close()
        finally:
            server.stop()

    def test_tcp_zero_byte_stream_immediate_eof(self, tcp_server_mod):
        """Client connects and immediately closes without sending any data."""
        server = tcp_server_mod.TCPEchoServer(port=0, timeout=0.5)
        port = server.start()
        srv_thread = threading.Thread(target=server.serve_forever, daemon=True)
        srv_thread.start()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", port))
            sock.close()  # Immediate EOF

            time.sleep(0.1)
            assert server.connections_handled >= 1
        finally:
            server.stop()

    # 1.3 Client Abrupt Disconnect (Partial Frames & RST)
    def test_tcp_abrupt_disconnect_partial_frame(self, concurrent_server_mod):
        """Client sends partial header / truncated frame and hard-disconnects via SO_LINGER=0."""
        server = concurrent_server_mod.ConcurrentTCPServer(port=0, timeout=0.5)
        port = server.start()
        srv_thread = threading.Thread(target=server.serve_forever, daemon=True)
        srv_thread.start()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", port))
            time.sleep(0.05)
            assert server.active_client_count == 1

            # Send 2 bytes of the 4-byte header, then send RST
            sock.sendall(b"\x00\x00")
            # Force RST packet (abrupt reset)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
            sock.close()

            # Server worker thread must recover cleanly and remove client from active registry
            time.sleep(0.3)
            assert server.active_client_count == 0
        finally:
            server.stop()

    # 1.4 Malformed HTTP Request Parsing
    def test_malformed_http_response_parsing(self, raw_http_mod):
        """RawHTTPClient._parse_response rejects corrupted HTTP responses."""
        parse = raw_http_mod.RawHTTPClient._parse_response

        # Empty response
        with pytest.raises(ConnectionError, match="Empty response received"):
            parse(b"")

        # Missing status line
        with pytest.raises(ValueError, match="Malformed HTTP response: no status line"):
            parse(b"\r\n\r\n")

        # Malformed status line with missing status code
        with pytest.raises(ValueError, match="Malformed status line"):
            parse(b"HTTP/1.1\r\nContent-Length: 0\r\n\r\n")

        # Delimiter with \n\n instead of \r\n\r\n
        res_lf = parse(b"HTTP/1.1 200 OK\nContent-Type: text/plain\n\nHello LF")
        assert res_lf.status_code == 200
        assert res_lf.body == b"Hello LF"

        # Invalid non-integer Content-Length header should degrade gracefully without crashing
        res_bad_cl = parse(b"HTTP/1.1 200 OK\r\nContent-Length: invalid\r\n\r\nFallback Body")
        assert res_bad_cl.status_code == 200
        assert res_bad_cl.body == b"Fallback Body"

    def test_http_server_malformed_requests(self, http_server_mod):
        """PythonHTTPServer returns 400 or 422 for invalid requests."""
        server = http_server_mod.PythonHTTPServer(port=0)
        port = server.start()

        try:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect(("127.0.0.1", port))

            # Missing Content-Length on POST
            req_missing_cl = (
                b"POST /api/items HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Content-Type: application/json\r\n\r\n"
                b'{"name": "test"}'
            )
            client_sock.sendall(req_missing_cl)
            resp = client_sock.recv(1024).decode()
            assert "400" in resp or "Missing Content-Length" in resp
            client_sock.close()

            # Corrupt JSON body
            client_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock2.connect(("127.0.0.1", port))
            bad_json = b"{name: invalid_json_syntax"
            req_bad_json = (
                b"POST /api/items HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Content-Type: application/json\r\n"
                b"Content-Length: " + str(len(bad_json)).encode() + b"\r\n\r\n" + bad_json
            )
            client_sock2.sendall(req_bad_json)
            resp2 = client_sock2.recv(1024).decode()
            assert "400" in resp2 or "Invalid JSON" in resp2
            client_sock2.close()
        finally:
            server.stop()


# =============================================================================
# 2. FASTAPI REST APIS ADVERSARIAL TESTS
# =============================================================================
class TestAdversarialFastAPI:
    """Stress testing FastAPI schemas, boundary query validation, and concurrency."""

    @pytest.fixture(scope="class")
    def sensor_client(self):
        mod = _load_module("networking/03_rest_apis/02_fastapi_endpoints.py", "mod_adv_fastapi_sensors")
        return TestClient(mod.app)

    @pytest.fixture(scope="class")
    def ml_client(self):
        mod = _load_module("networking/03_rest_apis/03_ml_model_serving.py", "mod_adv_fastapi_ml")
        return TestClient(mod.app)

    # 2.1 Invalid JSON Input
    def test_invalid_json_inputs(self, sensor_client, ml_client):
        """Verify API rejects non-JSON, corrupted bodies, and type violations with 422."""
        # Non-JSON bytes
        resp_corrupt = sensor_client.post(
            "/sensors",
            content=b"CORRUPTED_RAW_NON_JSON",
            headers={"Content-Type": "application/json"}
        )
        assert resp_corrupt.status_code == 422

        # Missing required field in sensor creation
        resp_missing = sensor_client.post("/sensors", json={"sensor_type": "vibration"})
        assert resp_missing.status_code == 422

        # String passed to float field in ML model
        resp_type_mismatch = ml_client.post("/predict", json={
            "machine_id": "PUMP_X",
            "temperature_c": "EXTREMELY_HOT",  # should be float
            "vibration_rms": 2.5,
            "acoustic_peak_db": 40.0,
            "rotational_speed_rpm": 1800.0,
        })
        assert resp_type_mismatch.status_code == 422

    # 2.2 Negative & Out-of-Bounds Sensor Values
    def test_sensor_value_range_boundaries(self, ml_client, sensor_client):
        """Test physical limits and negative values against Pydantic validation."""
        # temperature_c: ge=-20.0, le=200.0
        # Below lower bound (-20.1)
        r_temp_low = ml_client.post("/predict", json={
            "machine_id": "PUMP_COLD",
            "temperature_c": -20.1,
            "vibration_rms": 2.0,
            "acoustic_peak_db": 30.0,
            "rotational_speed_rpm": 1500.0,
        })
        assert r_temp_low.status_code == 422

        # Exactly at lower bound (-20.0) -> MUST PASS
        r_temp_bound = ml_client.post("/predict", json={
            "machine_id": "PUMP_COLD",
            "temperature_c": -20.0,
            "vibration_rms": 2.0,
            "acoustic_peak_db": 30.0,
            "rotational_speed_rpm": 1500.0,
        })
        assert r_temp_bound.status_code == 200

        # Negative vibration RMS: ge=0.0 -> must be rejected
        r_vib_neg = ml_client.post("/predict", json={
            "machine_id": "PUMP_VIB",
            "temperature_c": 25.0,
            "vibration_rms": -0.1,
            "acoustic_peak_db": 30.0,
            "rotational_speed_rpm": 1500.0,
        })
        assert r_vib_neg.status_code == 422

        # Negative sampling rate in sensor catalog: ge=1 -> must be rejected
        r_sampling_neg = sensor_client.post("/sensors", json={
            "name": "Invalid Rate Sensor",
            "sensor_type": "vibration",
            "sampling_rate_hz": -100,
        })
        assert r_sampling_neg.status_code == 422

    # 2.3 Boundary Query Limits
    def test_query_parameter_limits(self, sensor_client, ml_client):
        """Query bounds: limit ge=1, le=100; skip ge=0; batch min_length=1."""
        # limit=0 (below ge=1)
        assert sensor_client.get("/sensors?limit=0").status_code == 422

        # limit=101 (above le=100)
        assert sensor_client.get("/sensors?limit=101").status_code == 422

        # skip=-1 (below ge=0)
        assert sensor_client.get("/sensors?skip=-1").status_code == 422

        # Excessive skip beyond count -> 200 OK with empty array
        r_empty = sensor_client.get("/sensors?skip=99999&limit=10")
        assert r_empty.status_code == 200
        assert r_empty.json() == []

        # Empty batch prediction (min_length=1)
        r_empty_batch = ml_client.post("/predict/batch", json={"samples": []})
        assert r_empty_batch.status_code == 422

    # 2.4 Concurrent Requests
    def test_concurrent_prediction_requests(self, ml_client):
        """Fire 50 concurrent requests across multiple threads to verify thread-safety and latency."""
        sample = {
            "machine_id": "TURBINE_STRESS",
            "temperature_c": 55.0,
            "vibration_rms": 3.2,
            "acoustic_peak_db": 42.0,
            "rotational_speed_rpm": 1750.0,
        }

        def send_request():
            res = ml_client.post("/predict", json=sample)
            return res.status_code, res.json()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_request) for _ in range(50)]
            results = [f.result() for f in futures]

        for status_code, data in results:
            assert status_code == 200
            assert "anomaly_detected" in data
            assert data["machine_id"] == "TURBINE_STRESS"
            assert data["inference_latency_ms"] >= 0.0


# =============================================================================
# 3. TENSORFLOW / TF_COMPAT ADVERSARIAL TESTS
# =============================================================================
class TestAdversarialTensorFlow:
    """Stress testing tf_compat GradientTape, higher-order derivatives, and Keras edges under Python 3.14."""

    @pytest.fixture(scope="class")
    def tf(self):
        mod = _load_module("machine-learning/08_tensorflow_fundamentals/tf_compat.py", "tf_compat_adv")
        return mod

    # 3.1 Multi-Variable GradientTape
    def test_multivariable_gradient_accuracy(self, tf):
        """Analytical gradient verification for target L = 2*w1^2 + 3*w2^2 + 4*w3^2 + b^2 + w1*w2."""
        w1 = tf.Variable(2.0, name="w1")
        w2 = tf.Variable(3.0, name="w2")
        w3 = tf.Variable(4.0, name="w3")
        b  = tf.Variable(1.5, name="b")
        unrelated = tf.Variable(10.0, name="unrelated")

        with tf.GradientTape() as tape:
            L = 2.0 * (w1 * w1) + 3.0 * (w2 * w2) + 4.0 * (w3 * w3) + (b * b) + (w1 * w2)

        grads = tape.gradient(L, [w1, w2, w3, b, unrelated])

        # Analytical partial derivatives:
        # dL/dw1 = 4*w1 + w2 = 4*2 + 3 = 11.0
        # dL/dw2 = 6*w2 + w1 = 6*3 + 2 = 20.0
        # dL/dw3 = 8*w3 = 8*4 = 32.0
        # dL/db  = 2*b  = 2*1.5 = 3.0
        # dL/dunrelated = 0.0
        assert np.isclose(grads[0].numpy(), 11.0, atol=1e-5)
        assert np.isclose(grads[1].numpy(), 20.0, atol=1e-5)
        assert np.isclose(grads[2].numpy(), 32.0, atol=1e-5)
        assert np.isclose(grads[3].numpy(), 3.0, atol=1e-5)
        assert np.isclose(grads[4].numpy(), 0.0, atol=1e-5)

    # 3.2 Higher-Order Derivatives (Nested GradientTapes)
    def test_higher_order_derivatives(self, tf):
        """Compute 1st, 2nd, and 3rd order derivatives: f(x) = x^3 - 5*x^2 + 2*x + 7."""
        x_val = 4.0
        x = tf.Variable(x_val)

        # 2nd order derivative via nested tapes
        with tf.GradientTape() as outer_tape:
            with tf.GradientTape() as inner_tape:
                y = (x * x * x) - 5.0 * (x * x) + 2.0 * x + 7.0
            dy_dx = inner_tape.gradient(y, x)
        d2y_dx2 = outer_tape.gradient(dy_dx, x)

        # At x = 4.0:
        # y = 64 - 80 + 8 + 7 = -1
        # y' = 3*x^2 - 10*x + 2 = 3*16 - 40 + 2 = 10.0
        # y'' = 6*x - 10 = 24 - 10 = 14.0
        assert np.isclose(dy_dx.numpy(), 10.0, atol=1e-4)
        assert np.isclose(d2y_dx2.numpy(), 14.0, atol=1e-4)

    # 3.3 Custom Keras Training Steps & Bug 2 Demonstration
    def test_gradient_with_trainable_variables_only(self, tf):
        """Verify gradient computation and SGD update work when only trainable variables are passed."""
        v_train = tf.Variable(1.0, trainable=True)
        opt = tf.keras.optimizers.SGD(learning_rate=0.1)

        with tf.GradientTape() as tape:
            loss = v_train * v_train

        grads = tape.gradient(loss, [v_train])
        opt.apply_gradients(zip(grads, [v_train]))

        # v_train updated: 1.0 - 0.1 * 2.0 = 0.8
        assert np.isclose(v_train.numpy(), 0.8, atol=1e-4)

    def test_non_trainable_variable_gradient_bug_exposure(self, tf):
        """Verify passing non-trainable variable to tape.gradient() preserves genuine gradients for trainable variables."""
        v_train = tf.Variable(1.0, trainable=True)
        v_frozen = tf.Variable(5.0, trainable=False)

        with tf.GradientTape() as tape:
            loss = v_train * v_train + v_frozen * 2.0

        grads = tape.gradient(loss, [v_train, v_frozen])
        grad_train = grads[0].numpy()
        grad_frozen = grads[1].numpy()

        # Verified Remediation:
        # Trainable variable receives genuine non-zero gradient, frozen variable receives 0.0
        assert np.isclose(grad_train, 2.0), f"Expected trainable gradient 2.0, got {grad_train}"
        assert np.isclose(grad_frozen, 0.0), f"Expected frozen gradient 0.0, got {grad_frozen}"

    def test_batch_size_1_and_serialization(self, tf, tmp_path):
        """Test Keras Sequential and Functional models with batch size 1 and weight persistence."""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy")

        # Single sample input (shape 1, 4)
        x_single = np.array([[1.0, 2.0, 3.0, 4.0]], dtype=np.float32)

        # Forward pass in training mode and eval mode
        out_tr = model(x_single, training=True)
        out_ev = model(x_single, training=False)
        assert out_tr.shape == (1, 1)
        assert out_ev.shape == (1, 1)
        assert 0.0 <= out_ev.numpy()[0, 0] <= 1.0

        # Save and restore weights to verify persistence fidelity
        weights_file = str(tmp_path / "test_weights.npz")
        model.save_weights(weights_file)
        assert os.path.exists(weights_file)

        # Create new identical model and load
        model2 = tf.keras.Sequential([
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ])
        model2.compile(optimizer="adam", loss="binary_crossentropy")
        _ = model2(x_single, training=False)  # build
        model2.load_weights(weights_file)

        out_restored = model2(x_single, training=False)
        assert np.allclose(out_ev.numpy(), out_restored.numpy(), atol=1e-5)


# =============================================================================
# 4. REVERSI CAPSTONE ADVERSARIAL TESTS
# =============================================================================
class TestAdversarialReversi:
    """Stress testing Othello game engine, pass semantics, double pass, and evaluation symmetry."""

    @pytest.fixture(scope="class")
    def rev(self):
        return _load_module("game-ai/solutions/reversi_solution.py", "reversi_adv_mod")

    # 4.1 Full Game to Completion
    def test_full_game_to_completion(self, rev):
        """Execute autonomous self-play and check valid scores, winner, and board limits."""
        winner, scores = rev.play_game(ai_depth=2, verbose=False)
        assert winner in [rev.BLACK, rev.WHITE, 0]
        assert scores[rev.BLACK] + scores[rev.WHITE] <= 64
        assert scores[rev.BLACK] + scores[rev.WHITE] >= 20

        # Verify winner consistency with scores
        if scores[rev.BLACK] > scores[rev.WHITE]:
            assert winner == rev.BLACK
        elif scores[rev.WHITE] > scores[rev.BLACK]:
            assert winner == rev.WHITE
        else:
            assert winner == 0

    # 4.2 Passes on No Legal Moves
    def test_single_pass_when_no_legal_moves(self, rev):
        """Player has zero legal moves but opponent has legal moves -> single pass toggles turn."""
        # Setup: White has 1 disc at (0, 1), Black has discs at (0, 0) and (1, 0)
        # White has NO legal moves; Black has legal move at (0, 2)
        board = [[rev.EMPTY for _ in range(8)] for _ in range(8)]
        board[0][0] = rev.BLACK
        board[1][0] = rev.BLACK
        board[0][1] = rev.WHITE
        state = rev.OthelloState(board=board, current_player=rev.WHITE)

        assert len(state.get_legal_moves(rev.WHITE)) == 0
        assert (0, 2) in state.get_legal_moves(rev.BLACK)

        # White passes
        next_state = state.make_move(None)
        assert next_state.current_player == rev.BLACK
        assert next_state.consecutive_passes == 1
        assert not next_state.is_terminal

        # Black plays (0, 2)
        after_black = next_state.make_move((0, 2))
        assert after_black.board[0][1] == rev.BLACK  # flipped to Black!

    # 4.3 Double Pass Game Termination
    def test_double_pass_game_termination(self, rev):
        """When neither player has legal moves, consecutive passes trigger game termination."""
        # Two isolated discs on opposite sides of board
        board = [[rev.EMPTY for _ in range(8)] for _ in range(8)]
        board[0][0] = rev.BLACK
        board[7][7] = rev.WHITE
        state = rev.OthelloState(board=board, current_player=rev.BLACK, consecutive_passes=0)

        assert len(state.get_legal_moves(rev.BLACK)) == 0
        assert len(state.get_legal_moves(rev.WHITE)) == 0

        # When Black makes pass, engine recognizes White also has 0 moves and sets terminal
        term_state = state.make_move(None)
        assert term_state.is_terminal is True
        assert term_state.winner == 0  # 1 Black vs 1 White = Draw

    # 4.4 Board Evaluation Symmetry
    def test_board_evaluation_symmetry(self, rev):
        """Verify Piece-Square Table (PST) and heuristic symmetry."""
        pst = np.array(rev.PST)

        # 1. PST Quadrant Symmetry: PST must be horizontally and vertically symmetric
        assert np.array_equal(pst, np.flipud(pst)), "PST must be vertically symmetric"
        assert np.array_equal(pst, np.fliplr(pst)), "PST must be horizontally symmetric"
        assert np.array_equal(pst, pst.T), "PST must be symmetric across main diagonal"

        # 2. Corner and Danger Zone calibration
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for r, c in corners:
            assert rev.PST[r][c] == 100, f"Corner ({r},{c}) must have maximum weight +100"

        # 3. Initial state heuristic evaluation should be neutral (0.0)
        init_state = rev.OthelloState()
        h_black = rev.heuristic(init_state, rev.BLACK)
        h_white = rev.heuristic(init_state, rev.WHITE)
        # Initial board is perfectly symmetric
        assert h_black == h_white == 0.0

        # 4. Inversion property for arbitrary symmetric positions
        test_board = [[rev.EMPTY for _ in range(8)] for _ in range(8)]
        test_board[0][0] = rev.BLACK
        test_board[7][7] = rev.WHITE
        sym_state = rev.OthelloState(board=test_board, current_player=rev.BLACK)
        # Black has (0,0)=+100 + corner=25 -> +125; White has (7,7)=+100 + corner=25 -> +125
        # Total heuristic relative to Black should be exactly 0
        assert rev.heuristic(sym_state, rev.BLACK) == 0.0
        assert rev.heuristic(sym_state, rev.WHITE) == 0.0


# =============================================================================
# 5. MOTOR CONTROL & SIMULINK ODE45 ADVERSARIAL TESTS
# =============================================================================
class TestAdversarialMotorControlODE45:
    """Stress testing anti-windup clamping, severe step disturbances, zero damping, and solver stability."""

    # 5.1 Anti-Windup Clamping Under Sustained Extreme Load
    def test_anti_windup_under_extreme_overload(self):
        """Under a massive load torque (tau_L = 2.5 N*m), actuator saturates at 36V and integrator state freezes."""
        Ra = 2.0
        La = 0.5
        Kt = 0.1
        Ke = 0.1
        J = 0.02
        b = 0.01
        V_max = 36.0
        omega_ref = 100.0
        Kp = 2.0
        Ki = 12.0

        # Massive load torque exceeding motor maximum stall torque (Kt * (V_max / Ra) = 0.1 * 18 = 1.8 N*m)
        tau_overload = 2.5

        def ode_aw(t, x):
            ia, omega, x_int = x
            err = omega_ref - omega
            u_unsat = Kp * err + Ki * x_int
            u_sat = min(V_max, max(-V_max, u_unsat))

            is_saturated = (u_sat != u_unsat)
            same_sign = (err * u_unsat > 0)
            dx_int = 0.0 if (is_saturated and same_sign) else err

            dia = (u_sat - Ra * ia - Ke * omega) / La
            domega = (Kt * ia - b * omega - tau_overload) / J
            return [dia, domega, dx_int]

        sol = solve_ivp(ode_aw, [0.0, 5.0], [0.0, 0.0, 0.0], method="RK45", max_step=0.005)
        x_int_traj = sol.y[2]

        # The integrator state must remain tightly bounded due to anti-windup clamping (< 5.0 rad)
        # In contrast, without anti-windup, x_int would integrate ~100 rad/s over 5s -> ~705 rad!
        max_int = np.max(np.abs(x_int_traj))
        assert max_int < 5.0, f"Integrator wound up to {max_int}, expected anti-windup clamping < 5.0"

    # 5.2 Severe Bi-Directional Step Disturbances
    def test_severe_step_disturbances(self):
        """Verify disturbance rejection under achievable load step +0.25 N*m and anti-windup stability under saturation."""
        Ra = 2.0
        La = 0.5
        Kt = 0.1
        Ke = 0.1
        J = 0.02
        b = 0.01
        V_max = 36.0
        omega_ref = 100.0
        Kp = 2.0
        Ki = 12.0

        # Step 1: Achievable load step 0.25 Nm (within 36V actuator capability)
        # Step 2: Regenerative step -0.20 Nm
        def tau_l_profile(t):
            if t < 2.0:
                return 0.0
            elif t < 4.0:
                return 0.25  # Achievable disturbance load
            else:
                return -0.20 # Overhauling / regenerative torque

        def motor_ode(t, x):
            ia, omega, x_int = x
            tau_l = tau_l_profile(t)
            err = omega_ref - omega
            u_unsat = Kp * err + Ki * x_int
            u_sat = min(V_max, max(-V_max, u_unsat))

            is_sat = (u_sat != u_unsat)
            same_sign = (err * u_unsat > 0)
            dx_int = 0.0 if (is_sat and same_sign) else err

            dia = (u_sat - Ra * ia - Ke * omega) / La
            domega = (Kt * ia - b * omega - tau_l) / J
            return [dia, domega, dx_int]

        sol = solve_ivp(motor_ode, [0.0, 6.0], [0.0, 0.0, 0.0], method="RK45", max_step=0.005)
        t = sol.t
        omega = sol.y[1]

        # Check solver did not produce NaN or Inf
        assert not np.any(np.isnan(omega))
        assert not np.any(np.isinf(omega))

        # Check steady-state zero tracking error recovery after each step:
        # Near t = 3.9 s (recovering from +0.25 N*m load)
        idx_rec1 = np.argmin(np.abs(t - 3.9))
        assert np.isclose(omega[idx_rec1], omega_ref, atol=1.0), f"Speed {omega[idx_rec1]} != {omega_ref}"

        # Near t = 5.9 s (recovering from -0.20 N*m regenerative load)
        idx_rec2 = np.argmin(np.abs(t - 5.9))
        assert np.isclose(omega[idx_rec2], omega_ref, atol=1.0), f"Speed {omega[idx_rec2]} != {omega_ref}"

    # 5.3 Zero Damping (b = 0.0) Dynamics & Stability
    def test_zero_damping_numerical_stability(self):
        """Simulate motor with b = 0 (pure frictionless inertia) to verify no division by zero, divergence, or instability."""
        Ra = 2.0
        La = 0.5
        Kt = 0.1
        Ke = 0.1
        J = 0.02
        b = 0.0  # Zero damping
        V_rated = 24.0

        def open_loop_ode(t, x):
            ia, omega = x
            dia = (V_rated - Ra * ia - Ke * omega) / La
            domega = (Kt * ia - b * omega) / J
            return [dia, domega]

        # Overdamped pole at s = -0.268 s^-1 -> tau = 3.73 s. Simulate 25 s (6.7 time constants)
        sol = solve_ivp(open_loop_ode, [0.0, 25.0], [0.0, 0.0], method="RK45", max_step=0.01)
        t = sol.t
        ia = sol.y[0]
        omega = sol.y[1]

        assert sol.status == 0
        assert not np.any(np.isnan(omega))
        # With b = 0, theoretical steady-state speed when ia -> 0 is V_rated / Ke = 24 / 0.1 = 240 rad/s
        omega_theoretical = V_rated / Ke
        assert np.isclose(omega[-1], omega_theoretical, atol=1.0)
        assert np.isclose(ia[-1], 0.0, atol=0.05)

    # 5.4 High Stiffness / Fast Dynamics Solver Stability
    def test_stiff_fast_electrical_pole_stability(self):
        """Very small inductance La = 0.005 H (fast electrical dynamics, pole at -400 s^-1)."""
        Ra = 2.0
        La = 0.005  # 100x smaller inductance -> high stiffness
        Kt = 0.1
        Ke = 0.1
        J = 0.02
        b = 0.01
        V_rated = 24.0

        def stiff_ode(t, x):
            ia, omega = x
            dia = (V_rated - Ra * ia - Ke * omega) / La
            domega = (Kt * ia - b * omega) / J
            return [dia, domega]

        # Simulate 8.0 s (4 mechanical time constants tau_mech = J/b = 2.0s)
        sol = solve_ivp(stiff_ode, [0.0, 8.0], [0.0, 0.0], method="RK45", rtol=1e-6, atol=1e-8)
        assert sol.status == 0, f"ODE solver failed with status {sol.status}: {sol.message}"
        # Theoretical steady state speed = (Kt * V) / (Ra * b + Kt * Ke) = (0.1 * 24) / (0.02 + 0.01) = 80 rad/s
        omega_ss = (Kt * V_rated) / (Ra * b + Kt * Ke)
        assert np.isclose(sol.y[1][-1], omega_ss, atol=0.5)
