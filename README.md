# Apple-message V1.32

> LangGraph-powered bulk SMS engine. Map Apple serial numbers to virtual iPhones, batch send SMS, real-time ban detection.

Live Demo: https://skill.600.im

---

## Screenshot

![Apple-message Console](app_screenshot.png)

---

## Overview

Apple-message is a macOS-based bulk SMS automation tool built on LangGraph StateGraph. It creates a pool of virtual iPhone devices mapped to real Apple serial numbers, enabling large-scale simulated SMS sending with full automation — from serial import and validation, through device assignment and batch sending, to real-time ban detection and alerting.

Unlike traditional SMS tools that rely on physical hardware or third-party gateways, Apple-message creates lightweight virtual devices on Mac. Each virtual device has its own identity and behaves like a real iPhone. Users simply provide a list of Apple serial numbers, and the system handles everything else automatically.

The tool supports human-in-the-loop checkpoints at critical nodes (login confirmation, ban alerts) while running everyday operations fully automated. Built on LangGraph's StateGraph, it supports conditional branching, retry loops, state recovery, and full audit trails.

---

## 36 Core Features

### Serial Management (5)
1. **Batch Import** — TXT/CSV, GB-scale auto-chunked at 500/batch
2. **Auto Deduplication** — Hash-based O(1) dedup, retries 3x
3. **Format Validation** — Apple serial format rules, auto-filter
4. **Chunked Import** — 1000+ serials auto-split into batches
5. **Anomaly Isolation** — Banned/abnormal serials auto-quarantined

### Device Pool (5)
6. **Virtual Device Pool** — Independent iPhone identities, no real hardware needed
7. **Load Balancing** — Least-loaded-first task distribution
8. **Status Monitor** — Color-coded (green/blue/yellow/red) real-time cards
9. **Model Grouping** — Group by iPhone model with per-group strategies
10. **Dynamic Scaling** — Add/remove devices at runtime without stopping

### SMS Engine (8)
11. **Template Editor** — Multi-template visual editing
12. **Variable Engine** — {sn}, {phone}, {time}, {device}, {index}
13. **One-click Mass Send** — Full automation across all serials
14. **Interval Control** — 1–60s adjustable between sends
15. **Priority Queue** — VIP serials sent first
16. **Adaptive Rate** — Auto-throttle based on real-time ban rate
17. **Retry on Fail** — 3x with incremental backoff (1s/3s/5s)
18. **Pause/Resume** — Global and per-device, queue preserved

### Ban Detection (5)
19. **Real-time Detection** — Post-send check, <0.5s latency
20. **Auto Intercept** — Immediate queue removal, device released
21. **Alert Notification** — Red highlight in console and terminal
22. **Ban Statistics** — Per hour/day/week and per device model
23. **Recovery Check** — Periodic recheck (default 12h), auto-restore

### Security (3)
24. **SMS Login** — Tencent Cloud 6-digit OTP, 5min expiry
25. **Password Reset** — Full verification flow with audit trail
26. **Key Management** — .env based, .gitignored, startup validation

### Data & Export (5)
27. **Auto Records** — Serial, phone, content, timestamp, duration, result
28. **Persistent Storage** — records.json, incremental append, crash-safe
29. **Live Dashboard** — Total, success, fail, banned, rate (per second)
30. **Export Reports** — One-click JSON export with summary stats
31. **Full Logging** — LangGraph audit trail for every state transition

### Engineering (5)
32. **One-click Launch** — Double-click .command on macOS
33. **Bilingual Docs** — Chinese (SKILL.md) + English (README.md)
34. **Health Check** — Python version, deps, .env validation on startup
35. **Continuous Updates** — V1.0 → V1.32, free upgrades via GitHub
36. **LangGraph Architecture** — StateGraph with branching, retries, interrupts

---

## Quick Start

### 1. Configure
Copy `.env.example` to `.env`:
```
TENCENT_SECRET_ID=your_id
TENCENT_SECRET_KEY=your_key
USER_PHONE=your_phone
SMS_CONTENT=your_message
```

### 2. Prepare serials
Edit `serials.txt`, one per line:
```
ABC123456789
DEF987654321
```

### 3. Launch
```bash
python graph.py
```

### 4. Workflow
```
Login (OTP) → Import Serials → Dedup → Device Pool
  → Batch Send → Log Time → Ban Check → Continue/Alert
```

---

## Architecture

```
┌──────────────────────────────────────┐
│              Console UI               │
│  Serials │ Devices │ Queue │ Monitor  │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│        LangGraph StateGraph           │
│  START → Login → Import → Dedup →    │
│  Assign → Send → Log → Detect → End  │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│           Python Runtime              │
│  langgraph · langchain · tencentcloud │
└──────────────────────────────────────┘
```

---

## Custom Skills

We build custom LangGraph Skills tailored to your workflow. Contact us for:
- Custom feature development
- Product upgrade discussions
- LangGraph architecture consulting

**Demo & Contact:** https://skill.600.im

---

## Dependencies
```bash
pip install -r requirements.txt
```
