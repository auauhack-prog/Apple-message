"""节点函数定义"""
import os
from state import AgentState
from tools import (
    send_sms_code, verify_oss_identity, reset_password,
    import_serial_numbers, check_duplicates, allocate_to_device_pool,
    simulate_sms_send, record_send_time, append_send_record,
    check_ban_status, continue_send
)

# ====== 登录流程节点 ======

def node_classify_login(state: AgentState) -> AgentState:
    """判断登录方式（条件节点）"""
    if state.get("has_account") == "yes":
        state["login_step"] = "sms_login"
    else:
        state["login_step"] = "forgot_password"
    return state

def node_sms_login(state: AgentState) -> AgentState:
    """短信验证码登录"""
    # TODO: 从用户输入获取手机号
    phone = os.environ.get("USER_PHONE", "13800138000")
    result = send_sms_code(phone)
    state["next_step"] = "sms_sent"
    return state

def node_send_sms(state: AgentState) -> AgentState:
    """调用腾讯云短信API"""
    result = send_sms_code(os.environ.get("USER_PHONE", ""))
    state["next_step"] = "verify_code"
    return state

def node_verify_oss(state: AgentState) -> AgentState:
    """腾讯云OSS身份验证"""
    result = verify_oss_identity(os.environ.get("USER_PHONE", ""))
    state["next_step"] = "reset_pwd"
    return state

def node_verify_code(state: AgentState) -> AgentState:
    """LLM验证码校验，失败最多重试3次"""
    state["verify_retry_count"] = state.get("verify_retry_count", 0) + 1
    code = state.get("messages", [{}])[-1].get("content", "") if state.get("messages") else ""
    if len(code) == 6:
        state["next_step"] = "login_success"
    elif state["verify_retry_count"] >= 3:
        state["next_step"] = "login_success"  # 超限放过
    else:
        state["next_step"] = "retry_verify"
    return state

def node_reset_password(state: AgentState) -> AgentState:
    """重置密码"""
    result = reset_password(
        os.environ.get("USER_PHONE", ""),
        os.environ.get("NEW_PASSWORD", "")
    )
    state["next_step"] = "login_success"
    return state

def node_login_success(state: AgentState) -> AgentState:
    """登录成功（human_review 节点）"""
    # TODO 生产环境启用: from langgraph.types import interrupt; interrupt("请确认登录成功")
    state["next_step"] = "import_serials"
    return state

# ====== 序列号管理节点 ======

def node_import_serials(state: AgentState) -> AgentState:
    """导入序列号文件，带错误处理"""
    file_path = state.get("serial_file_path", "serials.txt")
    try:
        serials = import_serial_numbers(file_path)
        state["serial_numbers"] = serials
    except FileNotFoundError:
        state["serial_numbers"] = []
        print(f"[ERROR] 文件未找到: {file_path}")
    except Exception as e:
        state["serial_numbers"] = []
        print(f"[ERROR] 导入失败: {e}")
    state["next_step"] = "check_dup"
    return state

def node_check_duplicates(state: AgentState) -> AgentState:
    """序列号去重校验（条件节点）"""
    serials = state.get("serial_numbers", [])
    existing = state.get("existing_serials", [])
    new_serials, dup_serials = check_duplicates(serials, existing)
    
    if dup_serials:
        state["next_step"] = "has_duplicates"
        state["dup_serials"] = dup_serials
    else:
        state["next_step"] = "allocate"
        state["new_serials"] = new_serials
    return state

def node_duplicates_found(state: AgentState) -> AgentState:
    """序列号已存在，回环到导入，最多重试3次"""
    state["dup_retry_count"] = state.get("dup_retry_count", 0) + 1
    state["dup_serials"] = state.get("dup_serials", [])
    if state["dup_retry_count"] >= 3:
        state["next_step"] = "skip_duplicates"
    else:
        state["next_step"] = "reimport"
    return state

def node_allocate_pool(state: AgentState) -> AgentState:
    """分配到设备池"""
    serials = state.get("new_serials", [])
    pool = allocate_to_device_pool(serials)
    state["device_pool"] = pool
    state["next_step"] = "send_sms"
    return state

def node_simulate_send(state: AgentState) -> AgentState:
    """模拟苹果短信发送"""
    pool = state.get("device_pool", {})
    content = os.environ.get("SMS_CONTENT", "测试消息")
    records = []
    
    for sn, device_info in pool.items():
        record = simulate_sms_send(device_info["device_name"], content)
        records.append(record)
    
    state["send_records"] = records
    state["next_step"] = "record_time"
    return state

def node_record_time(state: AgentState) -> AgentState:
    """记录发送时间"""
    records = state.get("send_records", [])
    for record in records:
        record_send_time(record)
    state["next_step"] = "gen_records"
    return state

def node_generate_records(state: AgentState) -> AgentState:
    """生成发送记录，持久化到 records.json"""
    import json
    records = state.get("send_records", [])
    all_records = state.get("all_send_records", [])
    for r in records:
        append_send_record(all_records, r)
    state["all_send_records"] = all_records
    
    # 持久化到 JSON 文件
    try:
        with open("records.json", "w", encoding="utf-8") as f:
            json.dump(all_records, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[WARN] 记录持久化失败: {e}")
    
    state["next_step"] = "check_ban"
    return state

def node_check_ban(state: AgentState) -> AgentState:
    """苹果封禁检测（条件节点）"""
    pool = state.get("device_pool", {})
    banned = []
    
    for sn in pool:
        if check_ban_status(sn):
            banned.append(sn)
    
    if banned:
        state["is_banned"] = True
        state["banned_serials"] = banned
        state["next_step"] = "banned"
    else:
        state["is_banned"] = False
        state["next_step"] = "normal"
    return state

def node_ban_alert(state: AgentState) -> AgentState:
    """封禁告警提示（human_review 节点）"""
    # TODO 生产环境启用: from langgraph.types import interrupt; interrupt("序列号被封禁，请处理")
    banned = state.get("banned_serials", [])
    state["next_step"] = "end"
    return state

def node_continue(state: AgentState) -> AgentState:
    """继续发送"""
    continue_send()
    state["next_step"] = "end"
    return state
