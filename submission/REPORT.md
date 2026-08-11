# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL: https://github.com/Simon068/Day13-K4-Observability
- Commit SHA cuối:
- Thành viên và vai trò:
  - Nguyễn Phú Quang — 2A202602017 — Role 1: Logging & PII (CP1).
  - Nguyễn Đại Quân — 2A202601933 — Role 2: Tracing & Prompt Versioning.
  - Trần Tuấn Linh — 2A202601612 — Role 3: Dashboard, SLO & Alert (CP2).
  - Trần Kiên — 2A202601598 — Role 4: Incident, Report & Demo.
  - Nguyễn Hữu Huy — 2A202601220 — Vai trò hỗ trợ: QA, Integration & Evidence.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`:
- Tổng số traces:
- Số PII leak còn lại:
- Link/đường dẫn dashboard:

## 3. Logging và tracing

- Evidence correlation ID:
- Evidence PII redaction:
- Evidence trace waterfall:
- Giải thích một span đáng chú ý:

## 4. Prompt versioning

- Prompt name:
- Version/label baseline:
- Version/label candidate:
- Trace ID của mỗi version:
- Bằng chứng đổi label hoặc rollback:

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`:
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
| Nguyễn Phú Quang — 2A202602017 | Role 1 — Hoàn thiện correlation ID, enrich log context, JSON logging và PII redaction trong `app/main.py`, `app/middleware.py`, `app/logging_config.py`, `app/pii.py`; xác nhận bằng `validate_logs.py`. | Chưa cập nhật | Chưa cập nhật |
| Nguyễn Đại Quân — 2A202601933 | Role 2 — Thiết lập tracing, tạo evidence tối thiểu 10 traces, prompt v1/v2, label và rollback trên Langfuse. | Chưa cập nhật | Chưa cập nhật |
| Trần Tuấn Linh — 2A202601612 | Role 3 — Hoàn thiện SLO, 3 alert rules, runbook và dashboard 6 panel; xác nhận bằng dashboard validator. | Chưa cập nhật | Chưa cập nhật |
| Trần Kiên — 2A202601598 | Role 4 — Điều tra incident theo Metrics → Traces → Logs, tổng hợp evidence, hoàn thiện báo cáo và chuẩn bị demo. | Chưa cập nhật | Chưa cập nhật |
| Nguyễn Hữu Huy — 2A202601220 | Vai trò hỗ trợ — QA, Integration & Evidence: chạy full test và validators, kiểm tra log/evidence không chứa PII hoặc secret, rà soát liên kết REPORT và hỗ trợ tích hợp trước demo. | Chưa cập nhật | Chưa cập nhật |
