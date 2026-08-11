# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL:
- Commit SHA cuối:
- Thành viên và vai trò:

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
| Nguyễn Phú Quang - 2A202602017 | CP1 Logging/PII: Triển khai structured JSON logging, correlation ID middleware, log enrichment (user_id_hash, session_id, feature, model, env), PII redaction (email, phone VN, CCCD, credit card, passport, IP) | `app/main.py`, `app/middleware.py`, `app/logging_config.py`, `app/pii.py` | Hiểu cách dùng structlog với contextvars để propagate correlation ID xuyên suốt request lifecycle; cách thiết kế PII scrubbing processor chạy trong pipeline logging để đảm bảo không có dữ liệu nhạy cảm nào bị lộ ra file log; tầm quan trọng của việc hash user_id thay vì log trực tiếp để vừa trace được hành vi user vừa bảo vệ privacy |
| | | | |
| | | | |
| | | | |
