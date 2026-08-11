# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: high_latency_p95
- Severity: warning
- SLI/SLO liên quan: latency_p95_ms, objective 3000ms theo `config/slo.yaml`
- Điều kiện và thời gian duy trì: latency_p95_ms > 3000 trong ít nhất 5 phút liên tục
- Ảnh hưởng tới người dùng: request phản hồi chậm rõ rệt, trải nghiệm chat bị delay, có thể dẫn đến timeout ở phía client
- Ba bước kiểm tra đầu tiên: xem panel Latency trên dashboard để xác nhận P95 thực sự vượt ngưỡng chứ không phải nhiễu tạm thời; mở Langfuse tìm các trace có latency cao nhất trong cửa sổ thời gian đó và xác định span nào chiếm phần lớn thời gian (retrieval, LLM call hay xử lý nội bộ); đối chiếu log theo correlation ID của các trace đó để xem có lỗi hoặc retry bất thường không
- Mitigation tạm thời: giảm concurrency của load test hoặc traffic nếu đang overload, tắt tính năng gây chậm nếu vừa mới triển khai, hoặc kiểm tra scenario incident đang bật (ví dụ rag_slow) và tắt nếu là practice
- Owner: Tran Tuan Linh

## Alert 2

- Tên: elevated_error_rate
- Severity: critical
- SLI/SLO liên quan: error_rate_pct, objective tối đa 2% theo `config/slo.yaml`
- Điều kiện và thời gian duy trì: error_rate_pct > 2 trong ít nhất 5 phút liên tục
- Ảnh hưởng tới người dùng: một phần request bị lỗi, người dùng nhận thông báo thất bại thay vì câu trả lời, ảnh hưởng trực tiếp đến khả năng sử dụng dịch vụ
- Ba bước kiểm tra đầu tiên: xem panel Errors trên dashboard để xác nhận tỉ lệ lỗi và breakdown theo error_type; mở trace của các request thất bại gần nhất trên Langfuse để xác định span nào ném lỗi; tra log theo correlation ID tương ứng để đọc message lỗi và context cụ thể
- Mitigation tạm thời: nếu lỗi tập trung ở một loại cụ thể (ví dụ timeout tới dependency ngoài), có thể tạm thời retry hoặc rollback về prompt version ổn định trước đó; nếu do incident practice đang bật thì tắt incident đó
- Owner: Tran Tuan Linh

## Alert 3

- Tên: quality_score_degradation
- Severity: warning
- SLI/SLO liên quan: quality_score_avg, objective tối thiểu 0.75 theo `config/slo.yaml`
- Điều kiện và thời gian duy trì: quality_score_avg < 0.75 trong ít nhất 10 phút liên tục (cửa sổ dài hơn vì đây là chỉ số trung bình, cần đủ mẫu để tránh cảnh báo giả)
- Ảnh hưởng tới người dùng: câu trả lời của agent kém chính xác hoặc kém liên quan hơn bình thường, dù request vẫn thành công về mặt kỹ thuật
- Ba bước kiểm tra đầu tiên: xem panel Quality trên dashboard để xác nhận xu hướng giảm chứ không phải một vài outlier; kiểm tra trên Langfuse xem prompt_label và prompt_version của các trace gần đây có bị đổi ngoài ý muốn không; đối chiếu log các response có quality_score thấp để xem input có bất thường hay không
- Mitigation tạm thời: rollback prompt về version hoặc label đã được xác nhận ổn định trước đó, nếu nguyên nhân không phải do prompt thì ghi nhận lại để điều tra sâu hơn trong báo cáo incident
- Owner: Tran Tuan Linh