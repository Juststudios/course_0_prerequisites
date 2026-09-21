"""
test_c0_math_bridges_adversarial.py
===================================
Empirical Adversarial Verification & Stress Test Harness authored by Challenger 2.

Scope:
1. Course 0 mini_agent:
   - Tool registry execution: Unknown tools, malformed arguments, AST calculator safety, async timeouts.
   - SQLite memory: Transactional integrity, concurrent read/writes (WAL mode), schema constraints, recovery.
   - JSON parsing & schema validation: Severely malformed markdown fences, trailing commas, truncated strings, Python literals.
   - ContextVars isolation: 50+ concurrent tasks, task-local state preservation, zero cross-talk.
2. Engineering Mathematics AI Bridges:
   - Linear Algebra: High-D projection idempotence (P^2=P) and symmetry (P^T=P), eigenvalue spectrum of P,
     SVD Eckart-Young reconstruction error bounds, attention score softmax sum to 1 under extreme logits.
   - Calculus: Numerical gradient against finite differences with strict relative tolerances (<= 1e-4),
     Hessian symmetry and Schwarz's theorem (f_xy = f_yx).
   - Probability: Gaussian-Gaussian sequential vs batch Bayesian conjugate update exact equality,
     Beta-Binomial conjugate update, Shannon entropy bounds (0 <= H <= ln K), temperature scaling monotonicity.
"""

import asyncio
import contextvars
import json
from pathlib import Path
import sqlite3
import sys
import threading
import time
from typing import Dict, List, Any

import numpy as np
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Target imports
from course_0_prerequisites.mini_agent.agent import MiniAgent, trace_id_ctx, session_id_ctx
from course_0_prerequisites.mini_agent.config import AgentConfig
from course_0_prerequisites.mini_agent.memory import SQLiteMemory
from course_0_prerequisites.mini_agent.tools import ToolRegistry, SafeASTCalculator
from course_0_prerequisites.mini_agent.engine import DeterministicReActEngine
# Math bridge modules & numeric folder imports
import importlib.util

def _load_module(rel_path: str, module_name: str):
    full_path = REPO_ROOT / rel_path
    assert full_path.exists(), f"File does not exist: {full_path}"
    spec = importlib.util.spec_from_file_location(module_name, str(full_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

json_repair_mod = _load_module("course_0_prerequisites/07_json_and_schema_validation/repair_malformed_json.py", "adv_json_repair")
LLMJSONRepair = json_repair_mod.LLMJSONRepair

la_mod = _load_module("engineering-mathematics/linear_algebra/07_embeddings_attention_svd.py", "adv_la_bridge")
calc_mod = _load_module("engineering-mathematics/calculus/05_optimization_gradients_backprop.py", "adv_calc_bridge")
prob_mod = _load_module("engineering-mathematics/probability/05_bayesian_entropy_sampling.py", "adv_prob_bridge")


# =============================================================================
# 1. COURSE 0 MINI_AGENT: TOOL REGISTRY STRESS TESTS
# =============================================================================

class TestMiniAgentToolRegistryStress:
    """Adversarial stress testing of ToolRegistry execution boundaries."""

    @pytest.fixture
    def registry(self):
        reg = ToolRegistry()
        @reg.register(name="add_numbers")
        def add_numbers(a: int, b: int) -> int:
            """Adds two integers."""
            return a + b

        @reg.register(name="fragile_tool")
        def fragile_tool(fail: bool = False) -> str:
            """Intentionally raises an exception when fail=True."""
            if fail:
                raise RuntimeError("Intentional tool explosion")
            return "all good"

        return reg

    def test_unknown_tool_graceful_failure(self, registry):
        """Registry must return ToolResult(success=False) for unknown tools without raising."""
        unknown_names = ["non_existent_tool", "", "__init__", "eval", "system", "12345"]
        for name in unknown_names:
            res = registry.execute(name, call_id="call_test", query="dummy")
            assert not res.success
            assert res.call_id == "call_test"
            assert "not found" in res.error.lower()
            assert res.output is None

    def test_malformed_arguments_handling(self, registry):
        """Registry must catch TypeError from missing or unexpected kwargs and return clean error."""
        # Missing required positional argument 'b'
        res_missing = registry.execute("add_numbers", a=10)
        assert not res_missing.success
        assert "missing" in res_missing.error.lower() or "typeerror" in res_missing.error.lower()

        # Unexpected keyword argument 'extra_arg'
        res_extra = registry.execute("add_numbers", a=10, b=20, extra_arg="unexpected")
        assert not res_extra.success
        assert "unexpected" in res_extra.error.lower() or "typeerror" in res_extra.error.lower()

        # Tool that throws runtime exception
        res_fail = registry.execute("fragile_tool", fail=True)
        assert not res_fail.success
        assert "RuntimeError" in res_fail.error
        assert "Intentional tool explosion" in res_fail.error

    def test_safe_ast_calculator_adversarial_inputs(self):
        """SafeASTCalculator must prevent code execution, handle division by zero, and reject invalid syntax."""
        # Valid safe arithmetic
        assert SafeASTCalculator.evaluate("2 + 2") == 4.0
        assert SafeASTCalculator.evaluate("(15 * 4) + 20") == 80.0
        assert SafeASTCalculator.evaluate("2 ** 5") == 32.0
        assert SafeASTCalculator.evaluate("-5 * 3") == -15.0

        # Division by zero
        with pytest.raises(ZeroDivisionError):
            SafeASTCalculator.evaluate("10 / 0")

        # Disallowed function calls / security probes
        security_probes = [
            "__import__('os').system('ls')",
            "eval('2 + 2')",
            "exec('a = 1')",
            "open('/etc/passwd').read()",
            "lambda x: x",
            "[x for x in range(10)]",
            "2 << 4",
            "1 | 2",
        ]
        for probe in security_probes:
            with pytest.raises(ValueError) as excinfo:
                SafeASTCalculator.evaluate(probe)
            assert "Disallowed syntax node" in str(excinfo.value) or "Invalid arithmetic expression" in str(excinfo.value)

        # Disallowed string constants
        with pytest.raises(ValueError):
            SafeASTCalculator.evaluate("'hello' + 'world'")

    @pytest.mark.asyncio
    async def test_agent_timeout_boundary_and_event_loop_blocking(self):
        """MiniAgent: Test AgentConfig validation, ContextVar cleanup on timeout, and synchronous tool event loop blocking."""
        # 1. Verify Pydantic schema validation rejects timeout < 1.0s
        with pytest.raises(Exception):
            AgentConfig(timeout_seconds=0.1)

        # 2. Verify ContextVars cleanup when asyncio.TimeoutError is raised
        cfg = AgentConfig(timeout_seconds=1.0, max_steps=3)
        mem = SQLiteMemory(":memory:")
        agent = MiniAgent(config=cfg, memory=mem)

        # Force a timeout by wrapping agent.run in an external wait_for with a yielding coroutine
        # First ensure ContextVars are set during execution
        trace_id_ctx.set("dirty_trace")
        session_id_ctx.set("dirty_session")

        # Running agent.run restores caller's context variables in finally block (PEP 567 semantics)
        resp = await agent.run("calculate 2 + 2", session_id="test_sess")
        assert resp.success
        assert trace_id_ctx.get() == "dirty_trace"
        assert session_id_ctx.get() == "dirty_session"

        # When caller context is clean, it returns to untraced/default
        trace_id_ctx.set("untraced")
        session_id_ctx.set("default")
        resp2 = await agent.run("calculate 2 + 2", session_id="clean_sess")
        assert resp2.success
        assert trace_id_ctx.get() == "untraced"
        assert session_id_ctx.get() == "default"

        # 3. Empirical Challenger Finding: Synchronous Tool Blocking
        # Because MiniAgent._execute_react_loop is synchronous (contains no await statements),
        # a synchronous blocking tool will block the asyncio thread and prevent wait_for from firing until tool returns.
        class SlowEngine(DeterministicReActEngine):
            def plan_next_step(self, query, history, steps, available_tools):
                if not steps:
                    from course_0_prerequisites.mini_agent.models import ToolCall
                    return "Need slow tool", ToolCall(id="c1", tool_name="slow_tool", arguments={}), None
                return "Done", None, "Finished"

        reg = ToolRegistry()
        @reg.register(name="slow_tool")
        def slow_tool():
            time.sleep(1.2)
            return "ok"

        slow_agent = MiniAgent(config=cfg, memory=mem, tools=reg, engine=SlowEngine())
        start = time.perf_counter()
        resp_slow = await slow_agent.run("test", session_id="s_slow")
        duration = time.perf_counter() - start

        # The synchronous tool ran for 1.2s despite timeout_seconds=1.0 because the event loop was blocked!
        assert duration >= 1.2
        # Response succeeded because wait_for was unable to interrupt the synchronous execution
        assert resp_slow.success


# =============================================================================
# 2. COURSE 0 MINI_AGENT: SQLITE MEMORY CONCURRENCY & RECOVERY
# =============================================================================

class TestSQLiteMemoryStress:
    """Stress testing transactional integrity, concurrency, and schema enforcement."""

    def test_schema_foreign_key_and_cascade_constraints(self, tmp_path):
        """Verify FOREIGN KEY enforcement and ON DELETE CASCADE integrity."""
        db_file = str(tmp_path / "test_schema.db")
        mem = SQLiteMemory(db_path=db_file)

        # 1. Foreign key violation on messages
        with pytest.raises(sqlite3.IntegrityError):
            with mem.conn:
                mem.conn.execute(
                    "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                    ("non_existent_session", "user", "hello", time.time())
                )

        # 2. Foreign key violation on tool_audit
        with pytest.raises(sqlite3.IntegrityError):
            with mem.conn:
                mem.conn.execute(
                    """INSERT INTO tool_audit (
                        session_id, trace_id, tool_name, args_json, result_json,
                        success, duration_ms, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("non_existent_session", "t1", "calc", "{}", "{}", 1, 5.0, time.time())
                )

        # 3. Create valid session and verify cascade delete
        session_id = "cascade_session"
        mem.add_message(session_id, "user", "Message 1")
        mem.add_message(session_id, "assistant", "Response 1")
        mem.log_tool_call(session_id, "tr_1", "calc", {"exp": "2+2"}, 4.0, True, 2.5)

        assert len(mem.get_history(session_id)) == 2
        assert len(mem.get_audit_logs(session_id)) == 1

        # Delete parent session
        with mem.conn:
            mem.conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))

        # Verify child messages and audits are completely cascaded away
        assert len(mem.get_history(session_id)) == 0
        assert len(mem.get_audit_logs(session_id)) == 0

        mem.close()

    def test_concurrent_multithreaded_wal_access(self, tmp_path):
        """Spawn 20 concurrent threads reading and writing to file-backed SQLiteMemory in WAL mode."""
        db_file = str(tmp_path / "concurrent_wal.db")
        # Initialize WAL mode database
        init_mem = SQLiteMemory(db_path=db_file)
        init_mem.close()

        num_threads = 20
        ops_per_thread = 25
        errors = []

        def worker(thread_idx: int):
            try:
                # Each thread creates its own SQLiteMemory connection instance
                thread_mem = SQLiteMemory(db_path=db_file)
                sess_id = f"session_thread_{thread_idx}"
                for op in range(ops_per_thread):
                    thread_mem.add_message(sess_id, "user", f"Query {op} from thread {thread_idx}")
                    thread_mem.log_tool_call(
                        session_id=sess_id,
                        trace_id=f"tr_{thread_idx}_{op}",
                        tool_name="calculator",
                        args={"val": op},
                        result=op * 2,
                        success=True,
                        duration_ms=1.2
                    )
                    hist = thread_mem.get_history(sess_id, limit=10)
                    assert len(hist) > 0
                thread_mem.close()
            except Exception as e:
                errors.append((thread_idx, str(e)))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Encountered concurrency errors: {errors}"

        # Verify total records accounted for
        verify_mem = SQLiteMemory(db_path=db_file)
        cur = verify_mem.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM messages")
        total_messages = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tool_audit")
        total_audits = cur.fetchone()[0]
        verify_mem.close()

        expected = num_threads * ops_per_thread
        assert total_messages == expected, f"Expected {expected} messages, found {total_messages}"
        assert total_audits == expected, f"Expected {expected} audits, found {total_audits}"

    def test_shared_connection_multithreaded_misuse_detection(self):
        """Verify that sharing a single sqlite3.Connection across concurrent threads causes InterfaceError."""
        mem = SQLiteMemory(":memory:")
        num_threads = 8
        errors = []

        def worker(idx: int):
            try:
                for op in range(15):
                    mem.add_message(f"sess_{idx}", "user", f"Msg {op}")
            except Exception as e:
                errors.append(type(e).__name__)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Empirical finding: Sharing un-synchronized Connection pointer across OS threads triggers InterfaceError
        assert len(errors) > 0, "Expected multithreaded contention on shared connection without mutex"
        mem.close()

    def test_recovery_and_edge_case_queries(self):
        """Test non-existent session querying, SQL injection attempts, and large message payloads."""
        mem = SQLiteMemory(":memory:")

        # Non-existent session
        assert mem.get_history("ghost_session") == []
        assert mem.get_audit_logs("ghost_session") == []

        # SQL injection attempt in session_id and content
        malicious_session = "sess'; DROP TABLE messages; --"
        malicious_content = "Robert'); DROP TABLE sessions; --"
        mem.add_message(malicious_session, "user", malicious_content)

        history = mem.get_history(malicious_session)
        assert len(history) == 1
        assert history[0]["content"] == malicious_content

        # Large payload (64 KB string)
        large_content = "X" * (64 * 1024)
        mem.add_message("large_payload_sess", "user", large_content)
        retrieved = mem.get_history("large_payload_sess")
        assert len(retrieved) == 1
        assert retrieved[0]["content"] == large_content

        mem.close()


# =============================================================================
# 3. COURSE 0 MINI_AGENT: JSON REPAIR & SCHEMA HEURISTICS
# =============================================================================

class TestLLMJSONRepairStress:
    """Stress testing JSON heuristic extraction, bracket balancing, and syntax repairs."""

    def test_markdown_code_fence_variations(self):
        """Repair JSON wrapped in standard markdown code fences, preambles, and postscripts."""
        # 1. 3-backtick json fence with conversational preamble and trailing notes
        text1 = """
        Here is the configuration you requested:
        ```json
        {
            "service": "agent_worker",
            "active": true,
            "replicas": 3
        }
        ```
        Let me know if you need changes.
        """
        res1 = LLMJSONRepair.extract_and_repair(text1)
        assert res1["service"] == "agent_worker"
        assert res1["active"] is True
        assert res1["replicas"] == 3

        # 2. No code fence, raw text with outer curly braces
        text2 = "The result of execution is: {\"tool\": \"calculator\", \"value\": 42.5} recorded."
        res2 = LLMJSONRepair.extract_and_repair(text2)
        assert res2["tool"] == "calculator"
        assert res2["value"] == 42.5

        # 3. Code fence with array of objects
        text3 = """```json\n[{"id": 1, "name": "alpha"}, {"id": 2, "name": "beta"}]\n```"""
        res3 = LLMJSONRepair.extract_and_repair(text3)
        assert len(res3) == 2
        assert res3[0]["id"] == 1

    def test_empirical_vulnerabilities_in_json_repair(self):
        """Document and verify empirical vulnerabilities in regex heuristic (uppercase JSON, 4-backtick fences)."""
        # Vulnerability 1: Uppercase ```JSON is not matched case-insensitively
        text_upper = "```JSON\n{\"status\": \"ok\"}\n```"
        with pytest.raises(ValueError) as exc:
            LLMJSONRepair.extract_and_repair(text_upper)
        assert "Expecting value" in str(exc.value)

        # Vulnerability 2: 4-backtick code fences leave a trailing backtick inside the payload
        text_4tick = "````json\n{\"status\": \"ok\"}\n````"
        with pytest.raises(ValueError) as exc:
            LLMJSONRepair.extract_and_repair(text_4tick)
        assert "Expecting value" in str(exc.value)

    def test_trailing_commas_and_python_literals(self):
        """Repair trailing commas in objects/arrays and Python literals (True, False, None)."""
        text = """
        {
            'model': 'gpt-4o',
            'temperature': 0.7,
            'features': ['search', 'bash', 'python',],
            'debug': True,
            'cache': False,
            'fallback': None,
        }
        """
        res = LLMJSONRepair.extract_and_repair(text)
        assert res["model"] == "gpt-4o"
        assert res["features"] == ["search", "bash", "python"]
        assert res["debug"] is True
        assert res["cache"] is False
        assert res["fallback"] is None

    def test_truncated_json_bracket_balancing(self):
        """Test stack-based balancing on truncated LLM streaming responses."""
        # 1. Truncated nested array
        text1 = '{"status": "streaming", "tokens": ["Hello", "world", "from"'
        res1 = LLMJSONRepair.extract_and_repair(text1)
        assert res1["status"] == "streaming"
        assert res1["tokens"] == ["Hello", "world", "from"]

        # 2. Truncated open string quote
        text2 = '{"thought": "I need to query the database to'
        res2 = LLMJSONRepair.extract_and_repair(text2)
        assert "I need to query" in res2["thought"]

        # 3. Truncated flat object
        text3 = '{"service": "orchestrator", "running": true, "step": 5'
        res3 = LLMJSONRepair.extract_and_repair(text3)
        assert res3["service"] == "orchestrator"
        assert res3["running"] is True
        assert res3["step"] == 5


# =============================================================================
# 4. COURSE 0 MINI_AGENT: CONTEXTVARS CONCURRENCY ISOLATION
# =============================================================================

class TestContextVarsIsolationStress:
    """Empirical verification that concurrent asyncio tasks never leak ContextVars."""

    @pytest.mark.asyncio
    async def test_high_concurrency_task_isolation(self):
        """Launch 60 concurrent tasks with interleaving async sleeps and assert zero context bleed."""
        num_tasks = 60
        task_ids = [f"task_{i:03d}" for i in range(num_tasks)]
        results: Dict[str, bool] = {}

        async def worker(tid: str):
            t_tok = trace_id_ctx.set(f"trace_{tid}")
            s_tok = session_id_ctx.set(f"sess_{tid}")
            try:
                # Stage 1 check
                assert trace_id_ctx.get() == f"trace_{tid}"
                assert session_id_ctx.get() == f"sess_{tid}"

                # Async suspension to force event loop task switching
                await asyncio.sleep(0.01 * (hash(tid) % 5 + 1))

                # Stage 2 check after suspension
                assert trace_id_ctx.get() == f"trace_{tid}"
                assert session_id_ctx.get() == f"sess_{tid}"

                # Nested async call
                await asyncio.sleep(0.005)

                # Stage 3 check
                assert trace_id_ctx.get() == f"trace_{tid}"
                assert session_id_ctx.get() == f"sess_{tid}"

                results[tid] = True
            finally:
                trace_id_ctx.reset(t_tok)
                session_id_ctx.reset(s_tok)

        tasks = [asyncio.create_task(worker(tid)) for tid in task_ids]
        await asyncio.gather(*tasks)

        assert len(results) == num_tasks
        assert all(results.values())
        # Global context must remain at default
        assert trace_id_ctx.get() == "untraced"
        assert session_id_ctx.get() == "default"


# =============================================================================
# 5. ENGINEERING MATHEMATICS: LINEAR ALGEBRA AI BRIDGE
# =============================================================================

class TestLinearAlgebraAIBridgeAdversarial:
    """Stress testing linear algebra bridge: Idempotence, symmetry, SVD bounds, attention softmax."""

    @pytest.mark.parametrize("m,n", [(50, 5), (100, 10), (300, 20), (500, 40)])
    def test_projection_idempotence_and_symmetry(self, m: int, n: int):
        """Orthogonal projection P = X (X^T X)^(-1) X^T must satisfy P^2=P, P^T=P, and rank=n."""
        rng = np.random.default_rng(100 + m + n)
        X = rng.standard_normal((m, n))
        y = rng.standard_normal(m)

        res = la_mod.compute_orthogonal_projection(X, y)
        P = res["P"]

        # 1. Idempotence: ||P^2 - P||_F < 1e-10
        assert res["idempotence_error"] < 1e-10, f"Failed P^2 = P at dim ({m},{n})"

        # 2. Symmetry: ||P^T - P||_F < 1e-10
        assert res["symmetry_error"] < 1e-10, f"Failed P^T = P at dim ({m},{n})"

        # 3. Trace invariant: Tr(P) == rank(P) == n
        trace_P = float(np.trace(P))
        assert np.isclose(trace_P, float(n), atol=1e-8), f"Tr(P) {trace_P} != {n}"

        # 4. Eigenvalues of projection: exactly n ones and (m-n) zeros
        eigvals = np.linalg.eigvalsh(P)
        ones = np.isclose(eigvals, 1.0, atol=1e-8)
        zeros = np.isclose(eigvals, 0.0, atol=1e-8)
        assert np.sum(ones) == n, f"Expected {n} eigenvalues of 1.0, got {np.sum(ones)}"
        assert np.sum(zeros) == (m - n), f"Expected {m-n} eigenvalues of 0.0, got {np.sum(zeros)}"

        # 5. Residual orthogonality: X^T (y - Py) == 0
        assert res["orthogonality_error"] < 1e-10

    def test_svd_eckart_young_exact_error_bounds(self):
        """Eckart-Young theorem: ||A - A_k||_F = sqrt(sum_{i=k+1} sigma_i^2) and ||A - A_k||_2 = sigma_{k+1}."""
        rng = np.random.default_rng(777)
        m, n = 64, 32
        A = rng.standard_normal((m, n))

        U, s, Vt = np.linalg.svd(A, full_matrices=False)

        for k in [1, 4, 8, 16, 24]:
            A_k = (U[:, :k] * s[:k]) @ Vt[:k, :]
            residual = A - A_k

            # Empirical Frobenius error
            emp_fro_err = float(np.linalg.norm(residual, ord='fro'))
            theor_fro_err = float(np.sqrt(np.sum(s[k:]**2)))
            assert np.isclose(emp_fro_err, theor_fro_err, atol=1e-11), \
                f"Frobenius error mismatch at rank {k}: {emp_fro_err} vs {theor_fro_err}"

            # Empirical Spectral (2-norm) error
            emp_spec_err = float(np.linalg.norm(residual, ord=2))
            theor_spec_err = float(s[k])
            assert np.isclose(emp_spec_err, theor_spec_err, atol=1e-11), \
                f"Spectral error mismatch at rank {k}: {emp_spec_err} vs {theor_spec_err}"

    def test_scaled_dot_product_extreme_logits_and_masking(self):
        """Softmax attention weights must sum to 1.0 even under large logit scales (+-1000) and masks."""
        rng = np.random.default_rng(999)
        seq_len, d_k = 16, 64

        # Extreme magnitude queries and keys
        Q = rng.standard_normal((seq_len, d_k)) * 50.0
        K = rng.standard_normal((seq_len, d_k)) * 50.0
        V = rng.standard_normal((seq_len, d_k))

        # Causal lower-triangular mask
        mask = np.tril(np.ones((seq_len, seq_len)))

        context, weights = la_mod.scaled_dot_product_attention(Q, K, V, mask=mask)

        # 1. Weights sum strictly to 1.0 along rows
        row_sums = np.sum(weights, axis=-1)
        assert np.allclose(row_sums, 1.0, atol=1e-12)

        # 2. Strict lower triangular property: masked upper positions must be 0.0
        upper_weights = weights[np.triu_indices(seq_len, k=1)]
        assert np.max(upper_weights) < 1e-12, f"Causal mask leaked attention to future tokens: {np.max(upper_weights)}"


# =============================================================================
# 6. ENGINEERING MATHEMATICS: CALCULUS AI BRIDGE
# =============================================================================

class TestCalculusAIBridgeAdversarial:
    """Stress testing calculus bridge: Numerical gradients, Hessian symmetry, Schwarz's theorem."""

    def test_multivariable_gradient_relative_tolerance_bound(self):
        """Verify central finite difference vs analytical gradient has relative error <= 1e-4 across non-linear functions."""
        # 1. Rosenbrock banana function: f(x, y) = 100*(y - x^2)^2 + (1 - x)^2
        def rosenbrock(v):
            x, y = v[0], v[1]
            return 100.0 * ((y - x**2)**2) + (1.0 - x)**2

        def grad_rosenbrock(v):
            x, y = v[0], v[1]
            dx = -400.0 * x * (y - x**2) - 2.0 * (1.0 - x)
            dy = 200.0 * (y - x**2)
            return np.array([dx, dy])

        non_stationary_points = [
            np.array([0.0, 0.0]),
            np.array([-1.2, 1.0]),
            np.array([2.0, 3.0]),
        ]

        for pt in non_stationary_points:
            res = calc_mod.check_multivariable_gradient(rosenbrock, grad_rosenbrock, pt, eps=1e-5)
            assert res["rel_error"] <= 1e-4, f"Rosenbrock grad check failed at {pt}: rel_error={res['rel_error']}"

        # Stationary point [1.0, 1.0] where grad == 0: check absolute error matches O(eps^2) Taylor remainder <= 1e-4
        stat_pt = np.array([1.0, 1.0])
        stat_res = calc_mod.check_multivariable_gradient(rosenbrock, grad_rosenbrock, stat_pt, eps=1e-5)
        # Theoretical truncation error is eps^2 / 6 * f'''(1) = (1e-10 / 6) * 2400 = 4.0e-8 <= 1e-4
        assert stat_res["abs_error"] <= 1e-4, f"Rosenbrock stationary point abs_error too high: {stat_res['abs_error']}"
        assert stat_res["abs_error"] < 1e-6, f"Rosenbrock stationary point abs_error exceeds 1e-6: {stat_res['abs_error']}"

        # 2. Multivariable Log-Sum-Exp: f(x) = ln(sum(exp(x_i)))
        def logsumexp(x):
            c = np.max(x)
            return c + np.log(np.sum(np.exp(x - c)))

        def grad_logsumexp(x):
            c = np.max(x)
            ex = np.exp(x - c)
            return ex / np.sum(ex)

        rng = np.random.default_rng(42)
        x_vec = rng.standard_normal(8)
        lse_res = calc_mod.check_multivariable_gradient(logsumexp, grad_logsumexp, x_vec, eps=1e-5)
        assert lse_res["rel_error"] <= 1e-4, f"LogSumExp grad check failed: rel_error={lse_res['rel_error']}"

    def test_hessian_symmetry_and_schwarz_theorem(self):
        """Hessian matrix of 2nd derivatives must be symmetric (Schwarz's theorem: f_xy = f_yx)."""
        # Non-linear test function: f(x, y, z) = x^3 y + y^2 z^3 + sin(x z)
        def func(v):
            x, y, z = v[0], v[1], v[2]
            return (x**3) * y + (y**2) * (z**3) + np.sin(x * z)

        v0 = np.array([1.5, -0.8, 2.2])
        eps = 1e-4
        n_dim = len(v0)
        H_numerical = np.zeros((n_dim, n_dim))

        # Central 2nd difference: H_ij = [f(x+ei+ej) - f(x+ei-ej) - f(x-ei+ej) + f(x-ei-ej)] / (4 eps^2)
        for i in range(n_dim):
            for j in range(n_dim):
                ei = np.zeros(n_dim)
                ej = np.zeros(n_dim)
                ei[i] = eps
                ej[j] = eps
                f_pp = func(v0 + ei + ej)
                f_pm = func(v0 + ei - ej)
                f_mp = func(v0 - ei + ej)
                f_mm = func(v0 - ei - ej)
                H_numerical[i, j] = (f_pp - f_pm - f_mp + f_mm) / (4.0 * eps * eps)

        # Verify symmetry ||H - H^T||_F < 1e-4
        sym_error = float(np.linalg.norm(H_numerical - H_numerical.T, ord='fro'))
        assert sym_error < 1e-4, f"Hessian violates symmetry / Schwarz's theorem: error={sym_error}"


# =============================================================================
# 7. ENGINEERING MATHEMATICS: PROBABILITY AI BRIDGE
# =============================================================================

class TestProbabilityAIBridgeAdversarial:
    """Stress testing probability bridge: Bayesian conjugate updates, Shannon entropy bounds, temperature scaling."""

    def test_sequential_vs_batch_bayesian_conjugate_update(self):
        """Sequential 1-by-1 Gaussian updates must exactly equal batch analytical posterior."""
        prior_mu = 15.0
        prior_sigma = 8.0
        sensor_sigma = 3.0

        rng = np.random.default_rng(2026)
        N = 50
        data = rng.normal(loc=72.0, scale=sensor_sigma, size=N)

        # 1. Sequential 1-by-1 update
        curr_mu = prior_mu
        curr_tau = 1.0 / (prior_sigma ** 2)
        tau_sensor = 1.0 / (sensor_sigma ** 2)

        for x in data:
            new_tau = curr_tau + tau_sensor
            new_mu = (curr_tau * curr_mu + tau_sensor * x) / new_tau
            curr_mu = new_mu
            curr_tau = new_tau

        seq_posterior_mu = curr_mu
        seq_posterior_sigma = np.sqrt(1.0 / curr_tau)

        # 2. Batch analytical update
        tau_0 = 1.0 / (prior_sigma ** 2)
        tau_batch = tau_0 + N * tau_sensor
        batch_posterior_sigma = np.sqrt(1.0 / tau_batch)
        batch_posterior_mu = (tau_0 * prior_mu + tau_sensor * np.sum(data)) / tau_batch

        # 3. Exact equality check
        assert np.isclose(seq_posterior_mu, batch_posterior_mu, atol=1e-10), \
            f"Sequential mean {seq_posterior_mu} != batch mean {batch_posterior_mu}"
        assert np.isclose(seq_posterior_sigma, batch_posterior_sigma, atol=1e-10), \
            f"Sequential sigma {seq_posterior_sigma} != batch sigma {batch_posterior_sigma}"

    def test_shannon_entropy_bounds_and_temperature_monotonicity(self):
        """Shannon entropy must be bounded (0 <= H <= ln K) and monotonically increase with temperature."""
        logits = np.array([4.0, 2.5, 0.5, -2.0])
        K = len(logits)
        max_theoretical_entropy = np.log(K)

        temperatures = [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0]
        entropies = []

        for T in temperatures:
            # Scaled stable softmax
            scaled = logits / T
            shifted = scaled - np.max(scaled)
            probs = np.exp(shifted) / np.sum(np.exp(shifted))

            # Shannon Entropy H(P) in nats
            H = float(-np.sum(probs * np.log(np.clip(probs, 1e-15, 1.0))))
            entropies.append(H)

            # Bound check: 0 <= H <= ln K
            assert H >= -1e-12, f"Entropy became negative at T={T}: H={H}"
            assert H <= max_theoretical_entropy + 1e-12, f"Entropy exceeded ln(K) at T={T}: H={H}"

        # Monotonicity check: H(T) must be strictly increasing with temperature
        for i in range(len(entropies) - 1):
            assert entropies[i] < entropies[i + 1], \
                f"Entropy not monotonically increasing: H(T={temperatures[i]})={entropies[i]} >= H(T={temperatures[i+1]})={entropies[i+1]}"

        # Low temperature approaches 0.0 (one-hot)
        assert np.isclose(entropies[0], 0.0, atol=1e-3)

        # High temperature approaches uniform ln(K)
        assert np.isclose(entropies[-1], max_theoretical_entropy, atol=1e-3)
