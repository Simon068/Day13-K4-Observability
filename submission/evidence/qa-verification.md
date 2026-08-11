# QA verification pass — Nguyễn Hữu Huy (2A202601220)

Ngày kiểm tra: 2026-08-11. Mục tiêu: xác minh độc lập rằng repo ở trạng thái
`main` hiện tại chạy đúng, log/dashboard/tests pass, và không có PII/secret
lọt vào Git trước khi nộp bài.

## Môi trường kiểm tra

Máy dev cài Python 3.14, không tương thích với các wheel đã pin trong
`requirements.txt` (pydantic-core build fail). Đã tạo venv riêng bằng
Python 3.11.9 (`C:\Users\Huy Nguyen\AppData\Local\Programs\Python\Python311`)
để chạy lại toàn bộ pipeline một cách sạch, độc lập với máy đã dùng khi phát
triển.

## Kết quả chạy lại

1. `uvicorn app.main:app` → `/health` trả `{"ok": true, ...}` (không có
   `LANGFUSE_*` key nên `tracing_enabled: false`, đúng hành vi fallback mô tả
   trong `SETUP.md`).
2. `python scripts/load_test.py` → 10 request, toàn bộ `[200]`, latency
   ~150-160ms.
3. `python scripts/validate_logs.py`:
   ```
   Total log records analyzed: 21
   Records with missing required fields: 0
   Records with missing enrichment (context): 0
   Unique correlation IDs found: 11
   Potential PII leaks detected: 0
   Estimated Score: 100/100
   ```
4. `python scripts/validate_dashboard.py` → `VALID: 6/6 panels are present in
   the dashboard contract.`
5. `python -m pytest -q` → `22 passed, 2 warnings` (warning chỉ là
   `on_event` deprecated trong FastAPI, không ảnh hưởng chức năng).

## Kiểm tra PII độc lập

Đọc trực tiếp `data/logs.jsonl` sinh ra từ load test: trường
`message_preview` chứa "What is your refund policy? My email is
`[REDACTED_EMAIL]`" — xác nhận scrubber hoạt động trên dữ liệu thật, không
chỉ qua validator. Grep toàn bộ `data/logs.jsonl` bằng regex email/số điện
thoại VN/số thẻ 16 số: 0 kết quả khớp dạng thô.

## Kiểm tra không lộ secret

- `git ls-files` không có `.env`, `.venv/`, hay file chứa `LANGFUSE_SECRET`.
- `git status --short` sạch trước khi bắt đầu kiểm tra (không có thay đổi
  chưa commit).
- Grep `submission/` với pattern khoá API (`sk-`, `pk-lf-`,
  `LANGFUSE_SECRET`, `api_key`) → không có kết quả.

## Kết luận

Repo ở commit `2cab2ad` chạy được từ môi trường sạch, ba script kiểm tra kỹ
thuật đều pass, log không lộ PII, Git không lộ secret. Không phát hiện vấn đề
cần fix trước khi nộp bài.
