# Track 02 — Load Test Results

## Locust Summary (10 Users)
- RPS: 0.3
- Average Latency: 20.8s
- P95 Latency: 31s

## Locust Summary (50 Users)
- RPS: 0.3
- Average Latency: 23.8s
- P95 Latency: 39s

## Observations
Server throughput remained stable at ~0.3 RPS but latency increased significantly under high concurrency (50 users), indicating a processing bottleneck on the CPU.
