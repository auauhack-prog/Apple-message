"""状态定义"""
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    has_account: str          # "yes" | "no" | ""
    login_step: str           # "sms_login" | "forgot_password" | ""
    serial_numbers: list      # 导入的序列号列表
    device_pool: dict         # 设备池分配结果
    send_records: list        # 发送记录
    is_banned: bool           # 是否被封禁
    next_step: str            # 路由字段
    dup_retry_count: int      # 序列号去重回环计数
    verify_retry_count: int   # 验证码重试计数
