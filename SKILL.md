# 苹果apple短信群发工具 V1.32

利用 Mac 序列号机群模拟手机发送短信。导入序列号后自动分配虚拟设备、批量发送、记录时间，实时检测苹果封禁。

---

## 价格

**¥299** 一次性买断，终身使用，持续更新。V1.32 及后续版本免费升级。

---

## 安装后配置

复制 `.env.example` 为 `.env`，填入腾讯云密钥：

```
TENCENT_SECRET_ID=你的SecretId
TENCENT_SECRET_KEY=你的SecretKey
USER_PHONE=你的手机号
SMS_CONTENT=要发送的短信内容
```

密钥获取：https://console.cloud.tencent.com/cam/capi

---

## 使用步骤

### 1. 准备序列号
编辑 `serials.txt`，一行一个序列号：
```
ABC123456789
DEF987654321
```

### 2. 启动
双击 `启动.command`

### 3. 自动执行流程
```
登录 → 序列号导入 → 去重 → 设备池分配
  → 批量发送 → 记录时间 → 封禁检测 → 继续/告警
```

### 4. 查看结果
- 发送记录：`records.json`
- 封禁提示：终端实时输出

---

## 常见问题

**Q: 序列号从哪里来？**  
A: 苹果设备「设置 → 关于本机」查看。

**Q: 重复导入怎么办？**  
A: 自动去重，最多重试 3 次跳过。

**Q: 序列号被封禁？**  
A: 每次发送后自动检测，封禁即时告警。

---

## 依赖
```bash
pip install -r requirements.txt
```
