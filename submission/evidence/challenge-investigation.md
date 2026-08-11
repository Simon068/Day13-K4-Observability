# Official challenge investigation

- Challenge ID: `day13-k4-observability-v1`
- Released incident: `rag_slow`
- Affected feature: `monitoring`
- Run: 2026-08-11 (five released challenge queries, concurrent)

## Metrics symptom

| Metric | Observed value | Challenge threshold |
|---|---:|---:|
| Traffic | 5 | n/a |
| Latency P50 | 3457 ms | 2000 ms |
| Latency P95 | 3511 ms | 2000 ms |
| Latency P99 | 3511 ms | 2000 ms |
| Errors | 0 | n/a |

The P95 latency exceeded both the released challenge threshold (2000 ms) and
the configured `high_latency_p95` alert threshold (3000 ms), while there were
no failed requests.

## Correlated log evidence

Use correlation ID `req-2b31b06b` and session `k4-challenge-s02`:

| Event | Timestamp (UTC) | Latency |
|---|---|---:|
| `request_received` | 2026-08-11T09:49:46.326230Z | n/a |
| `response_sent` | 2026-08-11T09:49:49.732682Z | 3403 ms |

Both records are in the generated `data/logs.jsonl`; that runtime log remains
ignored by Git because it can contain local execution data.

## Trace evidence

- Langfuse trace ID: `c709ac1e15ee347068438f5464d7bb13`
- Session: `k4-challenge-s02`
- Observed trace latency: 3.32 s
- Waterfall screenshot: `submission/evidence/challenge_waterfall.png`

## Root cause, fix and prevention

The released `rag_slow` incident causes `app.mock_rag.retrieve()` to sleep for
2.5 seconds before returning documents. The incident was disabled after the
run, and `/health` confirmed `rag_slow=false`. A safe Langfuse tool span named
`retrieval` now wraps the retriever without capturing input or output, allowing
the next waterfall to localize this delay without exposing prompt content.

Prevention: alert on P95 latency, add a retriever timeout/circuit breaker, and
cache stable corpus results. The saved waterfall can be reopened in Langfuse
using the trace ID above for further inspection.
