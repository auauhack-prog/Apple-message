"""LangGraph 状态图定义 - 苹果短信自动化"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from nodes import (
    node_classify_login,
    node_sms_login,
    node_send_sms,
    node_verify_oss,
    node_verify_code,
    node_reset_password,
    node_login_success,
    node_import_serials,
    node_check_duplicates,
    node_duplicates_found,
    node_allocate_pool,
    node_simulate_send,
    node_record_time,
    node_generate_records,
    node_check_ban,
    node_ban_alert,
    node_continue,
)

# ====== 条件路由函数 ======

def route_after_classify(state: AgentState) -> str:
    step = state.get("login_step", "")
    if step == "sms_login":
        return "sms_login"
    return "forgot_password"

def route_after_dup_check(state: AgentState) -> str:
    if state.get("next_step") == "has_duplicates":
        return "duplicates"
    return "allocate"

def route_after_dup_found(state: AgentState) -> str:
    if state.get("next_step") == "skip_duplicates":
        return "skip"
    return "retry"

def route_after_verify(state: AgentState) -> str:
    if state.get("next_step") == "retry_verify":
        return "retry"
    return "success"

def route_after_ban_check(state: AgentState) -> str:
    if state.get("next_step") == "banned":
        return "banned"
    return "normal"

# ====== 构建图 ======

builder = StateGraph(AgentState)

builder.add_node("classify_login", node_classify_login)
builder.add_node("sms_login", node_sms_login)
builder.add_node("forgot_password", node_verify_oss)
builder.add_node("send_sms", node_send_sms)
builder.add_node("verify_code", node_verify_code)
builder.add_node("reset_password", node_reset_password)
builder.add_node("login_success", node_login_success)
builder.add_node("import_serials", node_import_serials)
builder.add_node("check_duplicates", node_check_duplicates)
builder.add_node("duplicates_found", node_duplicates_found)
builder.add_node("allocate_pool", node_allocate_pool)
builder.add_node("simulate_send", node_simulate_send)
builder.add_node("record_time", node_record_time)
builder.add_node("generate_records", node_generate_records)
builder.add_node("check_ban", node_check_ban)
builder.add_node("ban_alert", node_ban_alert)
builder.add_node("continue_send", node_continue)

builder.add_edge(START, "classify_login")
builder.add_conditional_edges("classify_login", route_after_classify, {
    "sms_login": "sms_login",
    "forgot_password": "forgot_password",
})
builder.add_edge("sms_login", "send_sms")
builder.add_edge("forgot_password", "reset_password")
builder.add_edge("send_sms", "verify_code")
builder.add_edge("reset_password", "login_success")
builder.add_conditional_edges("verify_code", route_after_verify, {
    "success": "login_success",
    "retry": "send_sms",
})
builder.add_edge("login_success", "import_serials")
builder.add_edge("import_serials", "check_duplicates")
builder.add_conditional_edges("check_duplicates", route_after_dup_check, {
    "duplicates": "duplicates_found",
    "allocate": "allocate_pool",
})
builder.add_conditional_edges("duplicates_found", route_after_dup_found, {
    "retry": "import_serials",
    "skip": "allocate_pool",
})
builder.add_edge("allocate_pool", "simulate_send")
builder.add_edge("simulate_send", "record_time")
builder.add_edge("record_time", "generate_records")
builder.add_edge("generate_records", "check_ban")
builder.add_conditional_edges("check_ban", route_after_ban_check, {
    "banned": "ban_alert",
    "normal": "continue_send",
})
builder.add_edge("ban_alert", END)
builder.add_edge("continue_send", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "apple-sms-demo"}}
    initial_state: AgentState = {
        "messages": [],
        "has_account": "yes",
        "login_step": "",
        "serial_numbers": [],
        "device_pool": {},
        "send_records": [],
        "is_banned": False,
        "next_step": "",
        "dup_retry_count": 0,
        "verify_retry_count": 0,
    }
    print("== 苹果短信自动化 Agent 启动 ==")
    for event in graph.stream(initial_state, config):
        node_name = list(event.keys())[0]
        step = event[node_name].get("next_step", "")
        if node_name and node_name != "__end__":
            print(f"[{node_name}] -> {step}")
    print("== 流程结束 ==")
