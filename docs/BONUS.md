# Bonus: Cost Optimization and Audit Log

## Cost optimization

The fake LLM now supports a response-token cap:

- `COST_OPTIMIZATION_ENABLED=true` enables the cap.
- `MAX_OUTPUT_TOKENS=120` is the default cap.

To collect before/after evidence, use two clean API runs so `/metrics` starts
from zero each time:

1. Set `COST_OPTIMIZATION_ENABLED=false` in your local `.env`, start the API,
   enable `cost_spike`, run the load test, and capture `/metrics` or the Cost
   dashboard panel as **before**.
2. Stop the API, set `COST_OPTIMIZATION_ENABLED=true`, start it again, repeat
   the same incident and load test, and capture **after**.
3. Disable the incident after each run. Save the two screenshots under
   `submission/evidence/` without committing `.env` or runtime logs.

The cap is applied after the simulated cost spike, so the before run makes the
cost increase visible and the after run demonstrates the mitigation.

## Audit log

`app.audit.write_audit_event()` writes sanitized JSONL records to
`AUDIT_LOG_PATH` (default `data/audit.jsonl`). The API records:

- `runtime_config_loaded` at startup;
- `incident_enabled`;
- `incident_disabled`.

`data/audit.jsonl` is intentionally ignored by Git because it is a runtime
log. Capture a sanitized screenshot or a short redacted excerpt as evidence if
you submit the Audit Log bonus.
