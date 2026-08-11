from __future__ import annotations

import json

from app import audit
from app.incidents import STATE
from app.mock_llm import FakeLLM


def test_audit_event_is_jsonl_and_scrubs_pii(monkeypatch, tmp_path) -> None:
    audit_path = tmp_path / "audit.jsonl"
    monkeypatch.setattr(audit, "AUDIT_LOG_PATH", audit_path)

    assert audit.write_audit_event("incident_enabled", {"operator": "student@vinuni.edu.vn"})

    record = json.loads(audit_path.read_text(encoding="utf-8"))
    assert record["event"] == "incident_enabled"
    assert record["payload"]["operator"] == "[REDACTED_EMAIL]"


def test_cost_optimization_caps_a_cost_spike(monkeypatch) -> None:
    monkeypatch.setitem(STATE, "cost_spike", True)
    monkeypatch.setattr("app.mock_llm.random.randint", lambda _low, _high: 150)
    monkeypatch.setenv("COST_OPTIMIZATION_ENABLED", "true")
    monkeypatch.setenv("MAX_OUTPUT_TOKENS", "120")

    response = FakeLLM().generate("prompt")

    assert response.usage.output_tokens == 120


def test_cost_spike_is_visible_when_optimization_is_disabled(monkeypatch) -> None:
    monkeypatch.setitem(STATE, "cost_spike", True)
    monkeypatch.setattr("app.mock_llm.random.randint", lambda _low, _high: 150)
    monkeypatch.setenv("COST_OPTIMIZATION_ENABLED", "false")

    response = FakeLLM().generate("prompt")

    assert response.usage.output_tokens == 600
