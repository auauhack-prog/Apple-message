# Apple-message v1.32

Bulk SMS automation tool. Uses Mac serial number clusters to simulate phone SMS sending. Import serials → auto-assign virtual devices → batch send → log timestamps → real-time Apple ban detection.

---

## Pricing

**¥299** one-time purchase, lifetime use, free updates.

> Current v1.32, future versions included.

---

## Setup

Copy `.env.example` to `.env` and fill in your Tencent Cloud credentials:

```
TENCENT_SECRET_ID=your_secret_id
TENCENT_SECRET_KEY=your_secret_key
USER_PHONE=your_phone_number
SMS_CONTENT=your_sms_content
```

Get keys: https://console.cloud.tencent.com/cam/capi

---

## Quick Start

### 1. Prepare serials
Edit `serials.txt`, one serial per line:
```
ABC123456789
DEF987654321
```

### 2. Launch
Double-click `启动.command`

### 3. Automated workflow
```
Login → Import Serials → Dedup → Device Pool
  → Batch Send → Log Time → Ban Check → Continue/Alert
```

### 4. Check results
- Send records: `records.json`
- Ban alerts: terminal output

---

## FAQ

**Q: Where to get serial numbers?**  
A: Apple device → Settings → About This Mac.

**Q: Duplicate serials?**  
A: Auto-dedup, retries up to 3 times then skips.

**Q: Serial banned?**  
A: Detected after each send, instant alert.

---

## Dependencies
```bash
pip install -r requirements.txt
```
