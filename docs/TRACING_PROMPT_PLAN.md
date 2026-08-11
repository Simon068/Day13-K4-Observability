# Kế hoạch Chi tiết: Tracing & Prompt Versioning

**Vai trò**: Tracing & Prompt Versioning  
**Dự án**: Day 13 — Observability cho Hệ thống AI (`Day13-K4-Observability`)  
**Người thực hiện**: Student / Role Leader  

---

## 🎯 1. Mục tiêu & Đầu ra cần bàn giao (Deliverables)

Theo [RUBRIC.md](../RUBRIC.md) và [SUBMISSION.md](../SUBMISSION.md), vai trò này chịu trách nhiệm bàn giao các minh chứng (evidence) sau vào thư mục `submission/evidence/` và cập nhật thông tin tương ứng vào [submission/REPORT.md](../submission/REPORT.md):

1. **Tối thiểu 10 traces** hiển thị thành công trên giao diện Langfuse UI (có metadata đầy đủ).
2. **1 Ảnh Waterfall Trace** thể hiện chi tiết luồng span (`retrieval` + `generation`).
3. **2 Prompt Versions trên Langfuse** (Prompt Name: `day13-chat`):
   - **Version 1**: Gắn label `baseline` và `production`.
   - **Version 2**: Gắn label `candidate` (với thay đổi định dạng câu trả lời).
4. **2 Trace ID minh chứng**: 1 trace chạy với label `baseline` và 1 trace chạy với label `candidate`.
5. **Bằng chứng chuyển label / Rollback**: Ảnh chụp giao diện Langfuse thể hiện thao tác chuyển/rollback label `production` giữa Version 1 và Version 2.
6. **Nội dung Báo cáo**: Hoàn thiện **Mục 3 (Tracing)** và **Mục 4 (Prompt Versioning)** trong `submission/REPORT.md`.

---

## 📁 2. Danh sách File làm việc & Trạng thái Mã nguồn

| File / Tài nguyên | Thao tác cần làm | Trạng thái mã nguồn / Ghi chú |
|---|---|---|
| [`.env`](../.env.example) | **Chỉnh sửa** | Điền thông số `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`, `LANGFUSE_PROMPT_NAME`, `LANGFUSE_PROMPT_LABEL`. |
| [`app/tracing.py`](../app/tracing.py) | **Đọc / Kiểm tra** | **ĐÃ HOÀN THIỆN CHO SẴN**. Khởi tạo Langfuse SDK client và decorator `@observe`. |
| [`app/agent.py`](../app/agent.py) | **Đọc / Kiểm tra** | **ĐÃ HOÀN THIỆN CHO SẴN**. Đã tự động gọi `update_current_trace()` & `update_current_generation()` gắn metadata (`prompt_name`, `prompt_label`, `prompt_version`, `prompt_source`). |
| [`app/prompt_management.py`](../app/prompt_management.py) | **Đọc / Kiểm tra** | **ĐÃ HOÀN THIỆN CHO SẴN**. Đã tự động fetch prompt từ Langfuse theo name/label hoặc fallback local. |
| [`submission/REPORT.md`](../submission/REPORT.md) | **Chỉnh sửa** | Điền nội dung Mục 3 & 4 (Trace ID, Waterfall span explanation, Prompt versions, Rollback evidence). |
| `submission/evidence/` | **Thêm tệp ảnh** | Lưu các ảnh chụp màn hình minh chứng (`trace_list.png`, `waterfall_trace.png`, `prompt_versions.png`, `prompt_rollback.png`). |

> ⚠️ **Lưu ý quan trọng**: Mã nguồn trong `app/agent.py`, `app/tracing.py` và `app/prompt_management.py` **đã được viết chuẩn xác và sẵn sàng sử dụng**. Không cần chỉnh sửa logic ngoại trừ khi phát hiện lỗi bất thường.

---

## 🔄 3. Ma trận Phụ thuộc (Dependency Matrix)

* **Phụ thuộc đầu vào**: 
  - **KHÔNG CAN CHỜ**. Vai trò này có thể tạo Prompt trên Langfuse UI, thiết lập `.env` và chạy thử nghiệm ngay lập tức.
  - Sau khi Role Logging hoàn thiện Correlation ID và PII Redaction, các trace của bạn sẽ tự động hiển thị dữ liệu đã làm sạch (`user_id_hash`, `correlation_id`).
* **Phụ thuộc đầu ra**:
  - **Role Incident & Demo**: Cần bạn mở **Waterfall Trace** để khoanh vùng span nguyên nhân (ví dụ span `retrieval` bị chậm trong kịch bản `rag_slow`) và cung cấp **Trace ID** làm bằng chứng cho bài báo cáo.
  - **Role Report**: Cần bạn bàn giao hình ảnh minh chứng và các thông số Trace ID.

---

## 🛠️ 4. Các bước Thực hiện Chi tiết (Step-by-Step)

### 📌 Bước 1: Cấu hình Môi trường Langfuse (10 phút)
1. Lấy thông tin `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` và `LANGFUSE_HOST` từ dự án Langfuse (Cloud hoặc Server dùng chung).
2. Tạo/Cập nhật file `.env`:
   ```dotenv
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   LANGFUSE_PROMPT_NAME=day13-chat
   LANGFUSE_PROMPT_LABEL=production
   ```

### 📌 Bước 2: Quản lý Prompt Versions trên Langfuse UI (15 phút)
1. Đăng nhập Langfuse UI, truy cập mục **Prompts** $\rightarrow$ Tạo mới Text Prompt tên **`day13-chat`**.
2. Thiết lập nội dung template với đúng 3 biến bắt buộc:
   ```text
   Feature={{feature}}
   Docs={{docs}}
   Question={{message}}
   ```
3. **Tạo Version 1**:
   - Gán 2 labels: `baseline` và `production`.
4. **Tạo Version 2**:
   - Thêm quy tắc định dạng ngắn gọn hơn.
   - Gán label: `candidate`.
5. **Lưu minh chứng 1**: Chụp ảnh màn hình danh sách Prompts hiển thị cả Version 1, Version 2 và các labels $\rightarrow$ Lưu thành `submission/evidence/prompt_versions.png`.

### 📌 Bước 3: Thu thập Traces & Kiểm tra Metadata (20 phút)
1. Khởi động API local:
   ```bash
   uv run uvicorn app.main:app --reload --env-file .env
   ```
2. Gửi traffic thử nghiệm bằng `load_test.py`:
   ```bash
   uv run python scripts/load_test.py --concurrency 2
   ```
3. Mở Langfuse UI kiểm tra:
   - Đảm bảo danh sách Traces có **tối thiểu 10 traces**.
   - Mở chi tiết 1 Trace, kiểm tra metadata gồm: `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=1`, `prompt_source=langfuse`.
4. **Lưu minh chứng 2**: Chụp ảnh danh sách $\ge 10$ traces $\rightarrow$ Lưu thành `submission/evidence/trace_list.png`.
5. **Lưu minh chứng 3**: Chụp ảnh chi tiết **Waterfall Trace** (gồm span `retrieval` và `generation`) $\rightarrow$ Lưu thành `submission/evidence/waterfall_trace.png`. Ghi lại `Trace ID`.

### 📌 Bước 4: Thao tác Rollback Prompt & Minh chứng (15 phút)
1. Thay đổi `.env`: Đặt `LANGFUSE_PROMPT_LABEL=candidate`. Chạy 1 request và ghi lại `Trace ID` (gắn Version 2).
2. Thay đổi `.env`: Đặt `LANGFUSE_PROMPT_LABEL=baseline`. Chạy 1 request và ghi lại `Trace ID` (gắn Version 1).
3. Trên Langfuse UI: Chuyển label `production` từ Version 1 sang Version 2.
4. Đổi lại `.env`: `LANGFUSE_PROMPT_LABEL=production`, chạy 1 request và xác nhận trace cập nhật sang `prompt_version=2`.
5. Thực hiện **Rollback**: Chuyển label `production` trên UI về lại Version 1.
6. **Lưu minh chứng 4**: Chụp ảnh màn hình lịch sử đổi label / rollback trên Langfuse UI $\rightarrow$ Lưu thành `submission/evidence/prompt_rollback.png`.

### 📌 Bước 5: Phối hợp Challenge & Điền Báo cáo (30 phút)
1. Khi có sự cố Challenge (`config/challenge.json`), khởi động load test challenge:
   ```bash
   uv run python scripts/load_test.py --challenge --concurrency 5
   ```
2. Mở Langfuse UI, lọc các trace trong khung thời gian bị chậm.
3. Xác định span chậm nhất (ví dụ span `retrieval` chiếm > 80% tổng thời gian do `rag_slow`).
4. Cung cấp **Trace ID** và **Waterfall Trace Screenshot** cho người giữ vai trò Điều tra Incident.
5. Hoàn thiện thông tin tại **Mục 3** và **Mục 4** trong `submission/REPORT.md`.
