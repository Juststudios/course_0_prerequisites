# Challenger 2 Adversarial Stress Testing & Verification Report

**Date**: 2026-09-18T15:51:30Z  
**Agent Identity**: `teamwork_preview_challenger_2`  
**Archetype**: Empirical Challenger (`critic`, `specialist`)  
**Verdict**: **`REQUEST_CHANGES`**  

---

## 1. Observation

Direct empirical observations from executing adversarial tests in `/home/settings/Documents/pearl/tests/adversarial/test_challenger_2_adversarial.py`:

```
============================= test session starts ==============================
platform linux -- Python 3.14.6, pytest-8.4.2, pluggy-1.6.0 -- /home/settings/anaconda3/bin/python3.14
rootdir: /home/settings/Documents/pearl
collected 23 items

tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialNetworking::test_tcp_client_connection_refused_handling PASSED [  4%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialNetworking::test_tcp_zero_byte_frame_and_recovery PASSED [  8%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialNetworking::test_tcp_zero_byte_stream_immediate_eof PASSED [ 13%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialNetworking::test_tcp_abrupt_disconnect_partial_frame PASSED [ 17%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialNetworking::test_malformed_http_response_parsing PASSED [ 21%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialNetworking::test_http_server_malformed_requests PASSED [ 26%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialFastAPI::test_invalid_json_inputs PASSED [ 30%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialFastAPI::test_sensor_value_range_boundaries PASSED [ 34%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialFastAPI::test_query_parameter_limits PASSED [ 39%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialFastAPI::test_concurrent_prediction_requests PASSED [ 43%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialTensorFlow::test_multivariable_gradient_accuracy PASSED [ 47%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialTensorFlow::test_higher_order_derivatives PASSED [ 52%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialTensorFlow::test_gradient_with_trainable_variables_only PASSED [ 56%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialTensorFlow::test_non_trainable_variable_gradient_bug_exposure PASSED [ 60%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialTensorFlow::test_batch_size_1_and_serialization PASSED [ 65%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialReversi::test_full_game_to_completion PASSED [ 69%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialReversi::test_single_pass_when_no_legal_moves PASSED [ 73%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialReversi::test_double_pass_game_termination PASSED [ 78%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialReversi::test_board_evaluation_symmetry PASSED [ 82%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialMotorControlODE45::test_anti_windup_under_extreme_overload PASSED [ 86%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialMotorControlODE45::test_severe_step_disturbances PASSED [ 91%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialMotorControlODE45::test_zero_damping_numerical_stability PASSED [ 95%]
tests/adversarial/test_challenger_2_adversarial.py::TestAdversarialMotorControlODE45::test_stiff_fast_electrical_pole_stability PASSED [100%]

======================== 23 passed, 1 warning in 5.04s =========================
```

### Observation 1.1 — Defect in `networking/01_tcp_ip/02_tcp_client.py` (Dangling Socket upon `ConnectionRefusedError`)
- **File**: `/home/settings/Documents/pearl/networking/01_tcp_ip/02_tcp_client.py`
- **Lines 34–43**:
  ```python
  def connect(self) -> None:
      """Establishes connection to the target server."""
      self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self._sock.settimeout(self.timeout)
      self._sock.connect((self.host, self.port))

  def is_connected(self) -> bool:
      """Returns True if the socket exists and is not closed."""
      return self._sock is not None and self._sock.fileno() != -1
  ```
- **Empirical Failure Output**:
  ```
  connect() raised: <class 'ConnectionRefusedError'> [Errno 111] Connection refused
  client.is_connected(): True
  send_framed() raised: <class 'BrokenPipeError'> [Errno 32] Broken pipe
  ```
- When `connect()` fails, `self._sock` is assigned but neither closed nor reset to `None`.
- `client.is_connected()` evaluates `self._sock is not None and self._sock.fileno() != -1` which evaluates to `True`.
- Subsequent calls to `client.send_framed(b"data")` bypass the `if not self.is_connected():` guard and trigger unhandled `BrokenPipeError` or `OSError: [Errno 107] Transport endpoint is not connected`, leaking an OS socket file descriptor.

### Observation 1.2 — Critical Defect in `machine-learning/08_tensorflow_fundamentals/tf_compat.py` (Autograd Gradient Collapse on Non-Trainable Variables)
- **File**: `/home/settings/Documents/pearl/machine-learning/08_tensorflow_fundamentals/tf_compat.py`
- **Lines 514–534**:
  ```python
  try:
      create_graph = len(_ACTIVE_TAPES) > 0
      torch_grads = torch.autograd.grad(
          outputs=target_torch,
          inputs=sources_torch,
          retain_graph=self.persistent or create_graph,
          create_graph=create_graph,
          allow_unused=True,
      )
      out_grads = []
      for g, src in zip(torch_grads, source_list):
          if g is not None:
              out_grads.append(Tensor(g, dtype=src.dtype))
          else:
              out_grads.append(zeros(src.shape, dtype=src.dtype))
      return out_grads if is_list else out_grads[0]
  except Exception:
      zeros_list = [zeros(s.shape, dtype=s.dtype) for s in source_list]
      return zeros_list if is_list else zeros_list[0]
  ```
- **Empirical Execution**:
  ```python
  v_train = tf.Variable(1.0, trainable=True)
  v_frozen = tf.Variable(5.0, trainable=False)
  with tf.GradientTape() as tape:
      loss = v_train * v_train + v_frozen * 2.0
  grads = tape.gradient(loss, [v_train, v_frozen])
  ```
- **Verbatim Error Inside PyTorch**:
  ```
  RuntimeError: One of the differentiated Tensors does not require grad
  ```
- **Resulting Gradients Returned**:
  ```
  grads = [<tf.Tensor: numpy=0.0>, <tf.Tensor: numpy=0.0>]
  ```
- Passing any non-trainable variable (or `model.variables` containing batch norm moving statistics or frozen weights) in `sources` causes PyTorch autograd to throw `RuntimeError`. The blanket `except Exception:` catches it and zeroes out gradients for **all** variables, including valid trainable parameters. Model optimization silently stalls with 0 gradients!

### Observation 1.3 — Robustness in Networking (TCP/UDP, HTTP)
- `TCPEchoServer` (`01_tcp_server.py`) gracefully handles zero-byte payload frames (`payload_len = 0`) by skipping echo without disconnecting, and immediately processes subsequent valid frames on the same connection.
- `ConcurrentTCPServer` (`04_concurrent_server.py`) handles abrupt client disconnects (truncated 2-byte header + hard `SO_LINGER=0` reset packet), cleanly decrementing `active_client_count` to 0.
- `RawHTTPClient` (`01_raw_http_client.py`) and `PythonHTTPServer` (`02_python_http_server.py`) properly raise `ConnectionError` on empty server responses, reject missing status lines, and return HTTP 400 for missing `Content-Length` or corrupted JSON payloads.

### Observation 1.4 — Robustness in FastAPI Microservices
- `SensorGateway` (`02_fastapi_endpoints.py`) and `MLModelServing` (`03_ml_model_serving.py`) strictly enforce Pydantic contracts:
  - Non-JSON / corrupted payload bytes $\rightarrow$ HTTP 422 Unprocessable Entity.
  - Negative values on unsigned metrics (`vibration_rms = -0.1`, `sampling_rate_hz = -100`) $\rightarrow$ HTTP 422.
  - Temperature below lower bound (`temperature_c = -20.1` vs lower limit `-20.0`) $\rightarrow$ HTTP 422.
  - Pagination violations (`limit = 0`, `limit = 101`, `skip = -1`) $\rightarrow$ HTTP 422.
  - High concurrency: 50 concurrent requests across 10 threads completed with 100% HTTP 200 responses, zero race conditions, and median latency < 1.0 ms.

### Observation 1.5 — Robustness in Reversi Capstone Solution
- `OthelloState` (`game-ai/solutions/reversi_solution.py`) correctly executes a 60-turn autonomous match to completion with total disc counts $\le 64$ and valid winner determination.
- Single pass handling: when passing player has 0 moves and opponent has valid moves, `make_move(None)` increments `consecutive_passes = 1`, toggles turn, and leaves `is_terminal = False`.
- Double pass handling: when neither player has moves, `make_move(None)` triggers double pass terminal detection (`consecutive_passes = 2`, `is_terminal = True`) and resolves the winner.
- Board evaluation symmetry: Piece-Square Table (PST) is symmetric under horizontal, vertical, and diagonal reflections, and the initial board state evaluates to neutral 0.0 for both players.

### Observation 1.6 — Robustness in Motor Control & Simulink ODE45
- Anti-windup clamping: under a sustained 2.5 N*m extreme overload, actuator voltage is clamped at $+36.0\text{ V}$, and the anti-windup clamping logic stops accumulating error, freezing integrator state $x_{int} < 5.0\text{ rad}$. In contrast, an unregulated integrator winds up to $> 705\text{ rad}$ (a 140x+ runaway).
- Disturbance rejection: under an achievable load torque ($\tau_L = 0.25\text{ N}\cdot\text{m} \le 0.30\text{ N}\cdot\text{m}$ saturation ceiling), the closed-loop PI controller achieves zero steady-state error ($e_{ss} \approx 0$) and restores speed to $100.0\text{ rad/s}$.
- Zero damping ($b = 0.0$): simulation over 25.0 s stably integrates the overdamped pole ($s = -0.268\text{ s}^{-1}$), converging to theoretical no-load speed $V_{rated}/K_e = 240.0\text{ rad/s}$ with armature current decaying to $0\text{ A}$.
- High stiffness: with electrical inductance reduced 100x ($L_a = 0.005\text{ H}$, pole at $-400\text{ s}^{-1}$), RK45 adaptive step integration completes with exit status 0 and converges to steady-state $80.0\text{ rad/s}$.

---

## 2. Logic Chain

1. **Step 1 (Inspection & Hypothesis Formulation)**:
   - Evaluated the 5 target areas across `networking/`, `machine-learning/`, `game-ai/`, and `engineering-mathematics/`.
   - Identified two critical risk areas in non-standard edge cases: socket connection error state handling in `TCPClient`, and non-trainable variable interaction with PyTorch autograd in `tf_compat.py`.

2. **Step 2 (Empirical Stress Testing)**:
   - Constructed `tests/adversarial/test_challenger_2_adversarial.py` containing 23 automated tests covering:
     - Socket connection refusal, zero-byte frames, abrupt RST disconnects, malformed HTTP responses.
     - Invalid JSON schemas, negative sensor values, boundary query limits, concurrent requests.
     - Multi-variable GradientTape, higher-order derivatives, custom Keras training step edge cases.
     - Full Reversi self-play, single pass, double pass termination, board evaluation symmetry.
     - Motor control anti-windup under severe overload, step disturbances, zero damping, and stiff ODE45 dynamics.

3. **Step 3 (Defect Confirmation & Impact Assessment)**:
   - **Bug 1 (`02_tcp_client.py`)**: `TCPClient.connect()` assigns `self._sock = socket.socket(...)` prior to calling `self._sock.connect(...)`. When `connect()` throws `ConnectionRefusedError`, the socket is left open and unmanaged. Calling `client.is_connected()` returns `True`, producing misleading connection state and leaking socket descriptors.
   - **Bug 2 (`tf_compat.py`)**: `GradientTape.gradient()` collects `[s._torch for s in source_list]` and passes them directly to `torch.autograd.grad(target_torch, sources_torch)`. In PyTorch autograd, passing any tensor where `requires_grad is False` throws `RuntimeError: One of the differentiated Tensors does not require grad`. Because `tf_compat.py` catches all exceptions with `except Exception: return zeros_list`, passing a non-trainable variable (e.g. from `model.variables`) collapses all gradients to zero, silently freezing model training.

4. **Step 4 (Verdict Determination)**:
   - While Networking HTTP/FastAPI, Reversi, and Motor Control ODE45 demonstrate excellent numerical and architectural robustness, Bug 2 in `tf_compat.py` is a severe silent failure mode in the TensorFlow autograd shim that directly impairs student exercises involving custom training loops or model variables.
   - Therefore, a verdict of `REQUEST_CHANGES` is mandated.

---

## 3. Caveats

- **Scope boundary**: Did not test GPU CUDA execution; all tests were verified headlessly on CPU under Python 3.14.6 on Linux x86_64.
- **Actuator Limits in DC Motor**: Under severe load disturbance $\tau_L > 0.30\text{ N}\cdot\text{m}$, the motor speed physically cannot reach $100.0\text{ rad/s}$ due to the $+36\text{ V}$ rail limit ($V_{sat} = 36\text{ V} \implies \omega_{max} \approx 71\text{ rad/s}$ under $\tau_L = 0.8\text{ N}\cdot\text{m}$). This is an inherent physical property of the specified motor parameters, not a software bug.

---

## 4. Conclusion & Actionable Fixes

**Final Verdict**: **`REQUEST_CHANGES`**

### Required Action 1: Fix `networking/01_tcp_ip/02_tcp_client.py`
In `TCPClient.connect()`:
```python
# BEFORE:
def connect(self) -> None:
    self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._sock.settimeout(self.timeout)
    self._sock.connect((self.host, self.port))

# AFTER (Proposed Fix):
def connect(self) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(self.timeout)
    try:
        sock.connect((self.host, self.port))
        self._sock = sock
    except Exception:
        sock.close()
        self._sock = None
        raise
```

### Required Action 2: Fix `machine-learning/08_tensorflow_fundamentals/tf_compat.py`
In `GradientTape.gradient()`: Filter source tensors so only tensors with `requires_grad=True` are passed to `torch.autograd.grad`:
```python
# BEFORE (Lines 514-525):
target_torch = target._torch
sources_torch = [s._torch for s in source_list]
torch_grads = torch.autograd.grad(outputs=target_torch, inputs=sources_torch, ...)

# AFTER (Proposed Fix):
target_torch = target._torch
grad_sources = []
grad_indices = []
for idx, s in enumerate(source_list):
    if hasattr(s, "_torch") and s._torch.requires_grad:
        grad_sources.append(s._torch)
        grad_indices.append(idx)

if grad_sources:
    create_graph = len(_ACTIVE_TAPES) > 0
    torch_grads = torch.autograd.grad(
        outputs=target_torch,
        inputs=grad_sources,
        retain_graph=self.persistent or create_graph,
        create_graph=create_graph,
        allow_unused=True,
    )
    out_grads = [zeros(s.shape, dtype=s.dtype) for s in source_list]
    for g, idx in zip(torch_grads, grad_indices):
        if g is not None:
            out_grads[idx] = Tensor(g, dtype=source_list[idx].dtype)
else:
    out_grads = [zeros(s.shape, dtype=s.dtype) for s in source_list]
return out_grads if is_list else out_grads[0]
```

---

## 5. Verification Method

1. **Run Full Adversarial Suite**:
   ```bash
   pytest /home/settings/Documents/pearl/tests/adversarial/test_challenger_2_adversarial.py -v
   ```
2. **Inspect Concrete Defect Reproduction**:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'machine-learning/08_tensorflow_fundamentals')
   import tf_compat as tf
   v1 = tf.Variable(1.0, trainable=True)
   v2 = tf.Variable(2.0, trainable=False)
   with tf.GradientTape() as tape:
       loss = v1 * v1 + v2 * 3.0
   print('Grads:', tape.gradient(loss, [v1, v2]))
   "
   ```
3. **Invalidation Condition**:
   If applying the proposed fixes resolves Bug 1 and Bug 2 such that:
   - `client.is_connected()` returns `False` after failed `connect()`, and
   - `tape.gradient(loss, [v_train, v_frozen])[0]` returns `2.0` (rather than collapsing to `0.0`),
   then this challenge is fully resolved and the milestone can be certified for `APPROVE`.
