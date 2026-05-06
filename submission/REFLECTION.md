# Reflection — Lab 20 (Personal Report)

> **Đây là báo cáo cá nhân.** Mỗi học viên chạy lab trên laptop của mình, với spec của mình. Số liệu của bạn không so sánh được với bạn cùng lớp — chỉ so sánh **before vs after trên chính máy bạn**. Grade rubric tính theo độ rõ ràng của setup + tuning của bạn, không phải tốc độ tuyệt đối.

---

**Họ Tên:** Hà Hữu An
**Cohort:** 
**Ngày submit:** _2026-05-06_

---

## 1. Hardware spec (từ `00-setup/detect-hardware.py`)

- **OS:** Windows 11 Home (AMD64)
- **CPU:** 12 physical · 12 logical cores
- **Cores:** 12
- **CPU extensions:** AVX2, FMA, SSE3, SSSE3
- **RAM:** 16 GB (Ước tính)
- **Accelerator:** NVIDIA GeForce GTX 1650, 4096 MiB
- **llama.cpp backend đã chọn:** CPU (Bản prebuilt wheel)
- **Recommended model tier:** TinyLlama-1.1B (Q4_K_M)

**Setup story** (≤ 80 chữ): 
Cài đặt môi trường ảo .venv thành công. Phải cài thêm `prometheus-client` và `llama-cpp-python[server]` để chạy được endpoint metrics và uvicorn. Máy có CUDA 13.2 nhưng hiện tại đang chạy bản CPU wheel để hoàn thành lab nhanh chóng.

---

## 2. Track 01 — Quickstart numbers (từ `benchmarks/01-quickstart-results.md`)

> Paste bảng từ `benchmarks/01-quickstart-results.md` xuống đây (auto-generated bởi `python 01-llama-cpp-quickstart/benchmark.py`).

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|--:|--:|--:|--:|--:|
| tinyllama-1.1b-chat... (Q4_K_M) | 1077 | 96 / 112 | 34.7 / 61.3 | 2247 / 2293 / 2296 | 28.8 |
| tinyllama-1.1b-chat... (Q2_K)   | 370 | 158 / 220 | 28.6 / 31.3 | 1913 / 2113 / 2148 | 35.0 |

**Một quan sát** (≤ 50 chữ): 
Mô hình Q2_K tải nhanh hơn và cho tốc độ sinh từ cao hơn (~35 tok/s so với 28.8 tok/s) nhưng câu trả lời đôi khi bị cụt hoặc lặp từ. Q4_K_M chậm hơn một chút nhưng ổn định hơn nhiều về chất lượng.

---

## 3. Track 02 — llama-server load test

> Chạy 2 lần locust ở concurrency 10 và 50, paste tóm tắt bên dưới.

| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|--:|--:|--:|--:|--:|--:|
| 10 | 0.3 | 18000 | 31000 | 31000 | 0 |
| 50 | 0.3 | 24000 | 39000 | 39000 | 0 |

**KV-cache observation**: peak `llamacpp:kv_cache_usage_ratio` ở concurrency 50 ổn định, do mô hình TinyLlama rất nhỏ nên bộ nhớ KV-cache chưa phải là rào cản lớn nhất.

---

## 4. Track 03 — Milestone integration

- **N16 (Cloud/IaC):** stub: localhost only
- **N17 (Data pipeline):** stub: in-memory dict
- **N18 (Lakehouse):** stub: SQLite
- **N19 (Vector + Feature Store):** stub: TOY_DOCS

**Nơi tốn nhiều ms nhất** trong pipeline: llama-server.

**Reflection** (≤ 60 chữ): 
Bottleneck nằm hoàn toàn ở bước Inference của LLM (llama-server). Các bước nhúng (embed) và truy vấn (retrieve) diễn ra gần như tức thì so với thời gian chờ server sinh văn bản dưới tải cao.

---

## 5. Bonus — The single change that mattered most

**Change:** Thay đổi số lượng CPU threads (`LAB_N_THREADS`) từ 1 lên 12.

**Before vs after** (paste 2-3 dòng từ sweep output):

```
n_threads=1:  Decode rate ~ 17.7 tok/s
n_threads=12: Decode rate ~ 28.8 tok/s
speedup: ~1.63×
```

**Tại sao nó work**:
Mặc dù số lượng luồng tăng 12 lần nhưng tốc độ chỉ tăng ~1.6 lần. Điều này là do việc tính toán LLM cực kỳ tốn băng thông bộ nhớ (Memory Bandwidth bound). Khi dùng quá nhiều core, các core phải tranh giành băng thông RAM dẫn đến hiệu năng tăng chậm dần (diminishing returns). Tuy nhiên 12 threads vẫn cho kết quả tốt nhất trên máy này.

---

## 6. (Optional) Điều ngạc nhiên nhất

Bất ngờ khi thấy card đồ họa GTX 1650 dù đời cũ nhưng vẫn được script detect chuẩn CUDA. Nếu có thời gian build từ source, chắc chắn tốc độ sẽ còn ấn tượng hơn nữa.

---

## 7. Self-graded checklist

- [x] `hardware.json` đã commit
- [x] `models/active.json` đã commit
- [x] `benchmarks/01-quickstart-results.md` đã commit
- [x] `benchmarks/02-server-results.md` (hoặc CSV) đã commit
- [x] `benchmarks/bonus-*.md` đã commit
- [x] Ít nhất 6 screenshots trong `submission/screenshots/`
- [x] `python scripts/verify.py` pass toàn bộ.
- [x] Repo trên GitHub ở chế độ **public**
- [x] Đã paste public repo URL vào VinUni LMS

---

**Quan trọng:** repo phải **public** đến khi điểm được công bố. Nếu private, grader không xem được → 0 điểm.
