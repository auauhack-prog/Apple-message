# 苹果 Apple 短信群发工具 V1.32

> 基于 LangGraph 构建的智能批量短信引擎。利用 Mac 序列号机群模拟手机环境，实现序列号导入、虚拟设备分配、批量短信发送、封禁实时检测的全链路自动化。

在线演示 & 定制联系：**https://skill.600.im**

---

## 界面预览

![Apple-message 控制台](app_screenshot.png)

---

## 项目概述

Apple-message 是一款运行在 macOS 环境下的群发短信自动化工具。将苹果设备的序列号映射到虚拟手机设备上，模拟真实手机的短信发送行为，完成大批量短信的定时、定量、可控发送。基于 LangGraph 有向状态图引擎构建，状态可回溯、节点可中断、流程可恢复。

传统的短信群发工具依赖真实手机硬件或第三方网关，硬件成本高、扩展性差。Apple-message 另辟蹊径，在 Mac 上创建虚拟设备池，每台虚拟设备拥有独立身份标识，可模拟 iPhone 的真实发送行为。用户只需准备序列号列表，导入后系统自动完成去重、校验、分配、发送、记录、检测的全流程。

---

## 40+ 核心功能详介

### 一、序列号获取与管理（8项）

| # | 功能 | 说明 |
|---|------|------|
| 1 | 批量导入 | TXT/CSV 格式，一行一个序列号，GB 级大文件自动分片 |
| 2 | 自动去重 | 哈希集合 O(1) 查重，失败重试 3 次后标记跳过 |
| 3 | 格式校验 | 内置苹果序列号格式规则，自动过滤非法字符 |
| 4 | 分批导入 | 超 1000 条自动分 500 条/批，中间状态持久化 |
| 5 | 异常标记隔离 | 封禁/异常/连续失败序列号自动移入隔离区 |
| 6 | 序列号搜索 | 按前缀、后缀、模糊关键词搜索已导入序列号 |
| 7 | 苹果设备扫描 | 局域网内自动发现苹果设备并提取序列号信息 |
| 8 | 序列号导出 | 支持将筛选结果导出为 TXT/CSV，含状态标记 |

---

### 二、设备池管理（5项）

| # | 功能 | 说明 |
|---|------|------|
| 9 | 虚拟设备池 | Mac 上创建虚拟 iPhone 设备，每台独立标识 |
| 10 | 智能负载均衡 | 按负载从低到高排序，优先分配空闲时间最长设备 |
| 11 | 设备状态监控 | 卡片式展示，颜色标记：绿（空闲）蓝（发送中）黄（等待）红（封禁） |
| 12 | 设备型号分组 | 按 iPhone 15 Pro / 14 / SE 分组，差异化策略 |
| 13 | 运行态动态增减 | 运行时动态添加/移除设备，无需停止任务 |

---

### 三、短信发送引擎（9项）

| # | 功能 | 说明 |
|---|------|------|
| 14 | 短信模板编辑 | 可视化编辑，多套模板创建、切换、预览 |
| 15 | 变量替换引擎 | {sn} {phone} {time} {device} {index} {content} 动态替换 |
| 16 | 一键批量群发 | 选定序列号遍历发送，完成后弹出统计摘要 |
| 17 | 发送间隔控制 | 1-60 秒可调，模拟真实用户节奏防风控 |
| 18 | 优先级队列 | 高优先级序列号优先进入发送队列，VIP 通道 |
| 19 | 速率自适应 | 根据成功率和封禁率自动微调发送节奏 |
| 20 | 失败自动重试 | 最多 3 次，间隔递增（1s/3s/5s），超限跳过 |
| 21 | 任务暂停与恢复 | 全局暂停/单设备暂停，队列保持，续传不重复 |
| 22 | 分组发送 | 按设备型号分组批量发送，每组独立策略 |

---

### 四、封禁检测与防护（6项）

| # | 功能 | 说明 |
|---|------|------|
| 23 | 实时封禁检测 | 每次发送后自动检测，延迟 < 0.5s |
| 24 | 自动拦截机制 | 封禁序列号立即从队列移除，设备释放 |
| 25 | 多级告警通知 | 控制台红色高亮 + 终端日志 + 系统通知 |
| 26 | 多维度封禁统计 | 按时段和型号维度统计封禁率 |
| 27 | 封禁恢复检测 | 每 12 小时复检，解除后自动恢复可用池 |
| 28 | 封禁预警 | 封禁率超阈值时提前预警，建议调整策略 |

---

### 五、登录与安全（3项）

| # | 功能 | 说明 |
|---|------|------|
| 29 | 短信验证码登录 | 腾讯云 API 发送 6 位验证码，5 分钟有效 |
| 30 | 忘记密码重置 | 手机验证码验证后重置，完整日志追踪 |
| 31 | 密钥安全管理 | .env 管理，.gitignore 排除，启动时完整性检测 |

---

### 六、数据记录与导出（6项）

| # | 功能 | 说明 |
|---|------|------|
| 32 | 自动发送记录 | 记录序列号、号码、内容、时间戳、耗时、结果 |
| 33 | 持久化存储 | records.json 增量写入，断电不丢失 |
| 34 | 成功率实时看板 | 总数/成功/失败/封禁/速率，实时刷新 |
| 35 | 一键导出报告 | JSON 格式完整报告，含统计摘要 |
| 36 | 完整操作日志 | LangGraph 审计追踪，每节点状态可回溯 |
| 37 | 发送记录搜索 | 按时间、序列号、状态搜索历史发送记录 |

---

### 七、工程化与辅助（7项）

| # | 功能 | 说明 |
|---|------|------|
| 38 | macOS 一键启动 | 双击 .command 自动激活环境并运行 |
| 39 | 中英文双语文档 | 中文 SKILL.md + 英文 README.md 全覆盖 |
| 40 | 环境健康自检 | 启动时检查 Python、依赖、.env 完整性 |
| 41 | 版本持续迭代 | V1.0 → V1.32，GitHub 免费获取更新 |
| 42 | LangGraph 架构 | StateGraph 支持分支、重试、中断人工确认 |
| 43 | 自定义脚本扩展 | 支持挂载自定义 Python 脚本扩展业务逻辑 |
| 44 | 定时发送任务 | 支持设定定时批量发送，无需人工值守 |

---

## 使用流程

### 第一步：环境配置
复制 `.env.example` 为 `.env`，填入腾讯云密钥：
```
TENCENT_SECRET_ID=你的SecretId
TENCENT_SECRET_KEY=你的SecretKey
USER_PHONE=你的手机号
SMS_CONTENT=要发送的短信内容
```

密钥获取：https://console.cloud.tencent.com/cam/capi

### 第二步：获取序列号
方式一：手动编辑 `serials.txt`，每行一个序列号。
方式二：使用苹果设备扫描功能，自动发现局域网内设备并提取序列号。

### 第三步：启动
双击 `启动.command` 或执行 `python graph.py`

### 第四步：自动化流程
```
登录（验证码） → 导入序列号 → 去重校验 → 设备池分配
  → 批量发送 → 记录时间 → 封禁检测 → 正常继续 / 告警拦截
```

### 第五步：查看结果
- 发送记录：`records.json`
- 封禁告警：终端实时显示
- 支持导出发送报告

---

## 常见问题

**Q: 序列号从哪里来？** A: 苹果设备「设置 → 关于本机」查看，或使用内置扫描功能自动获取。

**Q: 重复导入怎么办？** A: 自动去重，3 次重试后跳过，不影响其他序列号。

**Q: 序列号被封禁？** A: 实时检测，封禁后自动拦截并红色告警，设备释放回空闲池。

**Q: 支持搜索序列号吗？** A: 支持按前缀、后缀、模糊关键词搜索已导入的序列号。

**Q: 支持局域网扫描苹果设备吗？** A: 支持自动发现局域网内苹果设备并提取序列号信息。

---

## 技术架构

```
┌─────────────────────────────────────────┐
│              控制台界面                    │
│  序列号管理 │ 设备池 │ 队列 │ 监控 │ 日志   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          LangGraph StateGraph           │
│  START → 登录 → 导入 → 去重 → 分配 → 发送  │
│    → 记录 → 检测 → 判断 → 继续/告警 → END  │
│                                          │
│   节点函数: nodes.py (18个)               │
│   工具函数: tools.py (12个)               │
│   状态定义: state.py (AgentState)         │
│   图定义:   graph.py (StateGraph)         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              Python 运行时               │
│  langgraph · langchain-core · tencentcloud│
└─────────────────────────────────────────┘
```

---

## 定制 Skill

**需要定制专属 Skill？欢迎沟通。**

- 专属功能定制：根据你的业务场景定制流程节点、工具函数
- 产品升级交流：需求讨论、功能排期、Beta 内测
- 技术咨询：LangGraph 架构优化、API 对接指导

联系方式：**https://skill.600.im**

---

## 依赖

```bash
pip install -r requirements.txt
```

---

## Apple-message V1.32 — English

> LangGraph-powered bulk SMS engine. Map Apple serials to virtual iPhones, batch send, real-time ban detection.

**Live Demo & Contact:** https://skill.600.im

### 44 Features at a Glance

**Serial Acquisition & Management (8)**
Batch import (TXT/CSV with auto-chunking) · Auto dedup (O(1) hashing, 3x retry) · Format validation · Chunked import (500/batch) · Anomaly isolation · Serial search (prefix/suffix/fuzzy) · Apple device LAN scanner · Serial export (TXT/CSV with status)

**Device Pool (5)**
Virtual device pool · Intelligent load balancing · Real-time status monitor (color-coded) · Model grouping (15 Pro/14/SE) · Runtime dynamic scaling

**SMS Engine (9)**
Template editor · Variable engine ({sn} {phone} {time} {device}) · One-click mass send · Interval control (1-60s) · Priority queue · Adaptive rate throttling · Auto retry (3x with backoff) · Pause/resume (global & per-device) · Grouped sending by model

**Ban Detection (6)**
Real-time detection (<0.5s) · Auto intercept · Multi-level alerts · Multi-dimension statistics · Recovery recheck (12h) · Early warning on threshold breach

**Security (3)**
SMS OTP login · Password reset · .env key management

**Data & Export (6)**
Auto records · Persistent storage (records.json) · Live dashboard · One-click export · Full audit logging · Record search

**Engineering (7)**
One-click macOS launch · Bilingual docs · Health check on startup · Continuous updates (V1.0→V1.32) · LangGraph StateGraph architecture · Custom script extensions · Scheduled batch sending

### Quick Start

```bash
# 1. Configure .env
cp .env.example .env

# 2. Add serials to serials.txt or use LAN scanner

# 3. Launch
python graph.py
```

### Architecture

LangGraph StateGraph: Login → Import → Dedup → Device Pool → Batch Send → Log → Ban Check → Continue/Alert

### Custom Skills

Custom feature development, product upgrades, LangGraph consulting: https://skill.600.im
