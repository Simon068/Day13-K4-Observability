# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL: https://github.com/Simon068/Day13-K4-Observability
- Commit SHA cuối: `0407d5a`
- Thành viên và vai trò:
  - Nguyễn Phú Quang — 2A202602017 — Role 1: Logging & PII (CP1).
  - Nguyễn Đại Quân — 2A202601933 — Role 2: Tracing & Prompt Versioning.
  - Trần Tuấn Linh — 2A202601612 — Role 3: Dashboard, SLO & Alert (CP2).
  - Trần Kiên — 2A202601598 — Role 4: Incident, Report & Demo.
  - Nguyễn Hữu Huy — 2A202601220 — Vai trò hỗ trợ: QA, Integration & Evidence.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: 20+ traces trên Langfuse US Cloud
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: https://us.cloud.langfuse.com


## 3. Logging và tracing

- Evidence correlation ID: log request/response dùng cùng `req-evidence01`; kết quả kiểm chứng lưu tại `submission/evidence/cp1-validate-logs.txt`.
- Evidence PII redaction: `submission/evidence/cp1-validate-logs.txt` ghi nhận 0 PII leak; log đã che email, phone và credit card bằng `[REDACTED_...]`.
- Evidence trace waterfall: Trace ID `c11ea75cc1111abc27f169b2cdded022` (`submission/evidence/waterfall_trace.png`).
- Giải thích một span đáng chú ý: Span `run` (Generation) xử lý prompt và sinh câu trả lời trong **0.86s**, tiêu tốn **147 tokens** với chi phí **$0.001929**; tags gồm `claude-sonnet-4-5`, `lab`, `qa`, session `s1` và user ID đã hash.

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: Version 1 (`baseline`, `production`)
- Version/label candidate: Version 2 (`candidate`)
- Trace ID của mỗi version:
  - Version 1 (`production`): `c11ea75cc1111abc27f169b2cdded022` (Trace metadata: `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=1`)
  - Version 2 (`candidate`): `c11ea75cc1111abc27f169b2cdded022` (Trace metadata: `prompt_name=day13-chat`, `prompt_label=candidate`, `prompt_version=2`)
- Bằng chứng đổi label hoặc rollback: File minh chứng `submission/evidence/prompt_rollback.png` và `submission/evidence/prompt_versions.png`

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: HỢP LỆ: 6/6 panel
- Evidence dashboard:
- SLO đã chọn và lý do:
- Alert rules và runbook:

## 6. Điều tra challenge

- Challenge ID:
- Triệu chứng từ metrics:
- Trace ID liên quan:
- Log line/correlation ID liên quan:
- Root cause:
- Fix action:
- Preventive measure:

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Nguyễn Phú Quang — 2A202602017 | Role 1 — CP1 Logging/PII: structured JSON logging, correlation ID middleware, log enrichment (`user_id_hash`, `session_id`, `feature`, `model`, `env`) và PII redaction cho email, phone VN, CCCD, credit card, passport, IP. | Commit `7c6b5b4` | Hiểu cách dùng structlog/contextvars để propagate correlation ID và PII scrubber trong logging pipeline. |
| Nguyễn Đại Quân — 2A202601933 | Role 2 — CP2 Tracing & Prompt Versioning: Đã tích hợp Langfuse SDK và metadata `prompt_name`, `prompt_label`, `prompt_version`, `prompt_source`; khởi tạo prompt `day13-chat` v1/v2, thực hiện test rollback label và tạo 20+ traces. | Commit `63cbdb4` / `0407d5a` | Nắm vững quy trình LLM Tracing và Prompt Lifecycle Management; cách gắn metadata phiên bản prompt vào từng trace để phục vụ audit/rollback; cách sử dụng Langfuse Waterfall Tracing để phân tích latency từng span (`retrieval` vs `generation`). |
| Trần Tuấn Linh — 2A202601612 | Role 3 — Hoàn thiện SLO, 3 alert rules, runbook và dashboard 6 panel; xác nhận bằng dashboard validator. | Chưa cập nhật | Chưa cập nhật |
| Trần Kiên — 2A202601598 | Role 4 — Điều tra incident theo Metrics → Traces → Logs, tổng hợp evidence, hoàn thiện báo cáo và chuẩn bị demo. | Chưa cập nhật | Chưa cập nhật |
| Nguyễn Hữu Huy — 2A202601220 | Vai trò hỗ trợ — QA, Integration & Evidence: chạy full test và validators, kiểm tra log/evidence không chứa PII hoặc secret, rà soát liên kết REPORT và hỗ trợ tích hợp trước demo. | Chưa cập nhật | Chưa cập nhật |
