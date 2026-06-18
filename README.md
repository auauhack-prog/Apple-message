# Apple-message v1.32

Bulk SMS automation tool powered by LangGraph. Import Apple serial numbers → auto-assign virtual devices → batch send SMS → real-time ban detection.

**¥299 one-time purchase, lifetime updates included.**

---

## Screenshot

![Apple-message Console](app_screenshot.png)

---

## 30+ Features

### 1. Serial Number Management
| Feature | Description |
|---------|-------------|
| Batch Import | TXT/CSV, one serial per line |
| Auto Dedup | Removes duplicates on import, retries 3x max |
| Format Validation | Validates and filters illegal serials |
| Chunked Import | Large file import without freezing |
| Anomaly Tagging | Auto-tags banned/abnormal serials |

### 2. Device Pool
| Feature | Description |
|---------|-------------|
| Virtual Device Pool | Simulates real iPhone environment |
| Load Balancing | Smart task distribution across devices |
| Status Monitor | Real-time device status (idle/sending/banned) |
| Device Grouping | Group by device model |
| Dynamic Scaling | Add/remove devices at runtime |

### 3. SMS Sending
| Feature | Description |
|---------|-------------|
| Message Template | Custom SMS content templates |
| Variable Substitution | {sn} {phone} {time} dynamic variables |
| Batch Sending | One-click mass send |
| Interval Control | 1-60s adjustable, simulates real rhythm |
| Priority Queue | High-priority serials first |
| Rate Limiting | Auto throttle, smooth output |
| Retry on Failure | Auto retry up to 3 times |
| Pause/Resume | Mid-task pause and resume |

### 4. Ban Detection
| Feature | Description |
|---------|-------------|
| Real-time Detection | Check after each send |
| Auto Intercept | Block banned serials automatically |
| Alert Notification | Terminal alert on ban |
| Ban Statistics | By time and device |

### 5. Authentication & Security
| Feature | Description |
|---------|-------------|
| SMS Login | Tencent Cloud SMS verification |
| Password Reset | Forgot password flow |
| Key Management | .env based, no sensitive exposure |

### 6. Data & Records
| Feature | Description |
|---------|-------------|
| Send Records | Auto-log time, content, serial, result |
| Persistent Storage | records.json, permanent access |
| Success Rate | Real-time success rate tracking |
| Export Reports | Export send reports |
| Full Logging | Complete operation logs |

### 7. Engineering
| Feature | Description |
|---------|-------------|
| One-click Launch | Double-click .command |
| Bilingual Docs | Chinese + English README |
| Continuous Updates | Free lifetime upgrades |

---

## Setup

Copy `.env.example` to `.env`:
```
TENCENT_SECRET_ID=your_id
TENCENT_SECRET_KEY=your_key
USER_PHONE=your_phone
SMS_CONTENT=your_message
```
Get keys: https://console.cloud.tencent.com/cam/capi

## Launch
```bash
python graph.py
```

## Workflow
```
Login → Import Serials → Dedup → Device Pool
  → Batch Send → Log Time → Ban Check → Continue/Alert
```

## Dependencies
```bash
pip install -r requirements.txt
```
