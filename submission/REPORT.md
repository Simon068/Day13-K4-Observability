# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: Debugging
- Repository URL: https://github.com/Simon068/Day13-K4-Observability
- Commit SHA cuối: `abf3735`
- Thành viên và vai trò:
  - Nguyễn Phú Quang — 2A202602017 — Role 1: Logging & PII (CP1).
  - Nguyễn Đại Quân — 2A202601933 — Role 2: Tracing & Prompt Versioning.
  - Trần Tuấn Linh — 2A202601612 — Role 3: Dashboard, SLO & Alert (CP2).
  - Trần Kiên — 2A202601598 — Role 4: Incident, Report & Demo.
  - Nguyễn Hữu Huy — 2A202601220 — Vai trò hỗ trợ: QA, Integration & Evidence.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: 45 root traces / khoảng 90 observations trên Langfuse US Cloud (Lưu tại `submission/evidence/trace_list.png`)
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: https://us.cloud.langfuse.com


## 3. Logging và tracing

- Evidence correlation ID: log request/response dùng trùng correlation ID `req-8a6f57b3`; kết quả kiểm chứng lưu tại `submission/evidence/cp1-validate-logs.txt`.
- Evidence PII redaction: `submission/evidence/cp1-validate-logs.txt` ghi nhận 0 PII leak; log đã che email, phone và credit card bằng `[REDACTED_...]`.
- Evidence trace waterfall: Trace ID `c11ea75cc1111abc27f169b2cdded022` (`submission/evidence/waterfall_trace.png`).
- Giải thích một span đáng chú ý: Span `run` (Generation) xử lý prompt và sinh câu trả lời trong **0.86s**, tiêu tốn **147 tokens** với chi phí **$0.001929**; tags gồm `claude-sonnet-4-5`, `lab`, `qa`, session `s1` và user ID đã mã hóa PII (`f85ac825d102`).

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: Version 1 (`baseline`, `production`)
- Version/label candidate: Version 2 (`candidate`)
- Trace ID của mỗi version:
  - Version 1 (`baseline`): Cần điền trace ID thật từ trace metadata `prompt_name=day13-chat`, `prompt_label=baseline`, `prompt_version=1`.
  - Version 2 (`candidate`): Cần điền trace ID thật khác Version 1 từ trace metadata `prompt_name=day13-chat`, `prompt_label=candidate`, `prompt_version=2`.
- Bằng chứng đổi label hoặc rollback: Minh chứng tại `submission/evidence/prompt_versions.png` và `submission/evidence/prompt_rollback.png` (Ghi nhận quá trình tạo Version 2 với label `candidate`, thử nghiệm promote `production` sang v2 và rollback về v1 thành công).

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: `VALID: 6/6 required panels are present in the dashboard contract.` Output được lưu tại `submission/evidence/dashboard-validator.txt`.
- Evidence dashboard: `submission/evidence/dashboard_full_6panels.png`, chụp toàn bộ 6 panel trong một ảnh duy nhất từ dashboard Streamlit dựng trên `data/logs.jsonl` (Latency percentiles, Request traffic, Error rate and breakdown, Cost over time, Input and output tokens, Quality proxy). Ảnh thể hiện đầy đủ time range 60 phút, refresh 30 giây, đơn vị và threshold của từng panel theo đúng `config/dashboard.yaml`. Baseline đo được tại thời điểm chụp: P95 latency 1220ms, error rate 0.00%, tổng cost $0.0418, quality score trung bình 0.880 — tất cả đều nằm trong ngưỡng SLO. P95 latency ở mức này cao hơn baseline ban đầu (208ms) do log tích luỹ từ nhiều lần chạy `load_test.py` trong cùng cửa sổ 60 phút, một vài request có latency cao hơn kéo percentile lên, nhưng vẫn nằm dưới threshold 3000ms nên không vi phạm SLO.
- SLO đã chọn và lý do: SLO được định nghĩa trong `config/slo.yaml` với cửa sổ đo 28 ngày, gồm bốn SLI bám theo đúng bốn nhóm rủi ro chính của một API AI: độ trễ, tỉ lệ lỗi, chi phí và chất lượng đầu ra. Latency P95 lấy ngưỡng 3000ms vì đây là mốc phổ biến cho trải nghiệm chat còn chấp nhận được trước khi người dùng cảm thấy hệ thống bị treo, với target 99.5% thời gian phải đạt ngưỡng này do latency là yếu tố người dùng cảm nhận trực tiếp nên cần độ khắt khe cao. Error rate đặt ngưỡng tối đa 2%, target 99%, vì lỗi ảnh hưởng trực tiếp đến khả năng hoàn thành tác vụ của người dùng nhưng một tỉ lệ lỗi rất nhỏ vẫn có thể chấp nhận được do phụ thuộc dependency ngoài. Daily cost đặt ngưỡng $2.5 mỗi ngày để giới hạn chi phí vận hành ở mức phù hợp với quy mô lab, tránh việc traffic hoặc lỗi bất thường làm chi phí tăng không kiểm soát. Quality score trung bình đặt ngưỡng tối thiểu 0.75, target 95% thời gian phải đạt ngưỡng này, vì đây là proxy đo mức độ hữu ích của câu trả lời và cần được giữ ổn định qua thời gian dù không thể đo chính xác bằng con người ở quy mô lớn.
- Alert rules và runbook: ba alert được định nghĩa trong `config/alert_rules.yaml`, đều là symptom-based bám theo đúng bốn SLO trên. `high_latency_p95` (severity warning) kích hoạt khi P95 latency vượt 3000ms liên tục 5 phút. `elevated_error_rate` (severity critical) kích hoạt khi error rate vượt 2% liên tục 5 phút. `quality_score_degradation` (severity warning) kích hoạt khi quality score trung bình dưới 0.75 liên tục 10 phút. Mỗi alert có runbook chi tiết tại `docs/alerts.md`, gồm SLI/SLO liên quan, ảnh hưởng tới người dùng, ba bước kiểm tra đầu tiên và mitigation tạm thời, giúp người trực có thể xử lý ngay khi alert nổ ra mà không cần đoán.

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
| Nguyễn Đại Quân — 2A202601933 | Role 2 — CP2 Tracing & Prompt Versioning: Cấu hình Langfuse SDK US Cloud, đính kèm trace metadata (`prompt_name`, `prompt_label`, `prompt_version`, `prompt_source`), tạo prompt `day13-chat` Version 1 (`production`/`baseline`) và Version 2 (`candidate`), thực hiện thử nghiệm rollback label và thu thập 45 root traces. | Commit `63cbdb4` / `abf3735` | Nắm vững quy trình LLM Tracing và Prompt Lifecycle Management; cách gắn metadata phiên bản prompt vào từng trace để phục vụ audit/rollback; cách sử dụng Langfuse Waterfall Tracing để phân tích latency từng span (`retrieval` vs `generation`). |
| Trần Tuấn Linh — 2A202601612 | Role 3 — Hoàn thiện SLO, 3 alert rules, runbook và dashboard 6 panel; xác nhận bằng dashboard validator. | Commit `CP3 eval complete` | Biết chuyển SLO thành dashboard contract có ngưỡng đo được, thiết kế alert theo symptom và viết runbook có thể thao tác. |
| Trần Kiên — 2A202601598 | Role 4 — Điều tra incident theo Metrics → Traces → Logs, tổng hợp evidence, hoàn thiện báo cáo và chuẩn bị demo. | Chưa cập nhật | Chưa cập nhật |
| Nguyễn Hữu Huy — 2A202601220 | Vai trò hỗ trợ — QA, Integration & Evidence: chạy full test và validators, kiểm tra log/evidence không chứa PII hoặc secret, rà soát liên kết REPORT và hỗ trợ tích hợp trước demo. | Chưa cập nhật | Chưa cập nhật |
