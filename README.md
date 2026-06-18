# Apple-message v1.32

> LangGraph-powered bulk SMS engine. Import Apple serials → auto-assign virtual devices → batch send → real-time ban detection.

**¥299 one-time purchase · lifetime updates**

Live Demo: https://skill.600.im

---

## Screenshot

![Apple-message Console](app_screenshot.png)

---

## 36 Core Features

### Serial Management
| # | Feature | Detail |
|---|---------|--------|
| 1 | Batch Import | TXT/CSV, drag & drop, GB-scale auto-chunk |
| 2 | Auto Dedup | Detects & removes duplicates, retries 3x |
| 3 | Format Validation | Apple serial format rules, auto-filter |
| 4 | Chunked Import | 500/batch for 1000+ serials |
| 5 | Anomaly Isolation | Banned/abnormal serials auto-quarantined |

### Device Pool
| # | Feature | Detail |
|---|---------|--------|
| 6 | Virtual Device Pool | Independent virtual iPhones |
| 7 | Load Balancing | Smart task distribution |
| 8 | Status Monitor | Real-time idle/sending/banned |
| 9 | Model Grouping | Group by iPhone model |
| 10 | Dynamic Scaling | Add/remove devices at runtime |

### SMS Sending
| # | Feature | Detail |
|---|---------|--------|
| 11 | Template Editor | Multi-template visual editing |
| 12 | Variable Engine | {sn} {phone} {time} {device} |
| 13 | One-click Mass Send | Full automation |
| 14 | Interval Control | 1-60s adjustable |
| 15 | Priority Queue | VIP serials first |
| 16 | Adaptive Rate | Auto throttle based on ban rate |
| 17 | Retry on Fail | 3x auto retry, then skip |
| 18 | Pause/Resume | Global & per-device |

### Ban Detection
| # | Feature | Detail |
|---|---------|--------|
| 19 | Real-time Detection | <0.5s after each send |
| 20 | Auto Intercept | Remove from queue instantly |
| 21 | Alert Notification | Red highlight in terminal |
| 22 | Ban Statistics | By hour/day/week/model |
| 23 | Recovery Check | Periodic recheck of banned serials |

### Security
| # | Feature | Detail |
|---|---------|--------|
| 24 | SMS Login | Tencent Cloud 6-digit OTP |
| 25 | Password Reset | Phone verification flow |
| 26 | Key Management | .env based, never in repo |

### Data & Export
| # | Feature | Detail |
|---|---------|--------|
| 27 | Auto Records | serial, phone, content, time, result |
| 28 | Persistent Storage | records.json, incremental |
| 29 | Success Rate | Real-time dashboard stats |
| 30 | Export Reports | One-click JSON export |
| 31 | Full Logging | LangGraph audit trail |

### Engineering
| # | Feature | Detail |
|---|---------|--------|
| 32 | One-click Launch | Double-click .command on macOS |
| 33 | Bilingual Docs | Chinese + English README |
| 34 | Auto Health Check | Python version, deps, .env |
| 35 | Continuous Updates | Free lifetime upgrades via GitHub |
| 36 | LangGraph Architecture | StateGraph, interruptible, recoverable |

---

## Setup

Copy `.env.example` to `.env`:

```
TENCENT_SECRET_ID=your_id
TENCENT_SECRET_KEY=your_key
USER_PHONE=your_phone
SMS_CONTENT=your_message
```

Keys: https://console.cloud.tencent.com/cam/capi

## Launch

```bash
python graph.py
```

## Workflow

```
Login (OTP) → Import Serials → Dedup → Device Pool
  → Batch Send → Log Time → Ban Check → Continue/Alert
```

---

## Custom Skills

Need a custom Skill? Let's talk!

- Custom feature development tailored to your workflow
- Product upgrade discussions & priority queuing
- LangGraph architecture consulting

Demo & Contact: https://skill.600.im

---

## Dependencies

```bash
pip install -r requirements.txt
```
