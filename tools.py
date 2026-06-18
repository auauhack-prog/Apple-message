"""工具函数定义"""
import os
import time
import json
import random
from typing import Optional

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models as sms_models
from tencentcloud.faceid.v20180301 import faceid_client, models as faceid_models

# ========== 登录模块 ==========

def send_sms_code(phone: str) -> dict:
    """通过腾讯云短信API发送验证码"""
    try:
        secret_id = os.environ.get("TENCENT_SECRET_ID", "")
        secret_key = os.environ.get("TENCENT_SECRET_KEY", "")

        if not secret_id or not secret_key:
            return {"status": "error", "message": "缺少腾讯云API密钥，请设置 TENCENT_SECRET_ID / TENCENT_SECRET_KEY", "phone": phone}

        cred = credential.Credential(secret_id, secret_key)
        client = sms_client.SmsClient(cred, "ap-guangzhou")

        # 生成6位随机验证码
        code = str(random.randint(100000, 999999))

        req = sms_models.SendSmsRequest()
        req.SmsSdkAppId = os.environ.get("SMS_SDK_APP_ID", "")
        req.SignName = os.environ.get("SMS_SIGN_NAME", "苹果自动化")
        req.TemplateId = os.environ.get("SMS_TEMPLATE_ID", "")
        req.TemplateParamSet = [code]
        req.PhoneNumberSet = [f"+86{phone}"]

        resp = client.SendSms(req)
        send_status = resp.SendStatusSet[0]

        return {
            "status": "success" if send_status.Code == "Ok" else "failed",
            "code": send_status.Code,
            "message": send_status.Message,
            "phone": phone,
            "verify_code": code  # 生产环境不应返回，仅用于演示
        }

    except TencentCloudSDKException as e:
        return {"status": "error", "message": str(e), "phone": phone}

def verify_oss_identity(phone: str) -> dict:
    """腾讯云OSS身份验证（人脸识别核身）"""
    try:
        secret_id = os.environ.get("TENCENT_SECRET_ID", "")
        secret_key = os.environ.get("TENCENT_SECRET_KEY", "")

        if not secret_id or not secret_key:
            return {"status": "error", "message": "缺少腾讯云API密钥", "phone": phone}

        cred = credential.Credential(secret_id, secret_key)
        client = faceid_client.FaceidClient(cred, "ap-guangzhou")

        req = faceid_models.DetectAuthRequest()
        req.RuleId = os.environ.get("FACEID_RULE_ID", "")
        req.IdCard = os.environ.get("USER_ID_CARD", "")

        resp = client.DetectAuth(req)

        return {
            "status": "verified",
            "phone": phone,
            "biz_token": resp.Result.BizToken if resp.Result else "",
            "url": resp.Result.Url if resp.Result else ""
        }

    except TencentCloudSDKException as e:
        return {"status": "error", "message": str(e), "phone": phone}

def reset_password(phone: str, new_password: str) -> dict:
    """重置密码"""
    return {"status": "reset", "phone": phone}

# ========== 序列号管理模块 ==========

def import_serial_numbers(file_path: str) -> list:
    """导入序列号文件"""
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def check_duplicates(serials: list, existing: list) -> tuple:
    """序列号去重校验，返回 (新序列号列表, 重复序列号列表)"""
    existing_set = set(existing)
    new = [s for s in serials if s not in existing_set]
    dup = [s for s in serials if s in existing_set]
    return new, dup

def allocate_to_device_pool(serials: list) -> dict:
    """将序列号分配到设备池"""
    pool = {}
    for i, sn in enumerate(serials):
        pool[sn] = {"device_name": f"iPhone-Sim-{i+1:03d}", "status": "active"}
    return pool

def simulate_sms_send(device: str, content: str) -> dict:
    """模拟苹果手机发送短信"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "device": device,
        "content": content,
        "timestamp": timestamp,
        "status": "success"
    }

def record_send_time(record: dict) -> dict:
    """记录发送时间"""
    record["recorded_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    return record

def append_send_record(records: list, record: dict) -> list:
    """追加到发送记录列表"""
    records.append(record)
    return records

def check_ban_status(serial: str) -> bool:
    """检测苹果封禁状态"""
    # TODO: 待实现 - 接入苹果封禁检测API
    # 需要对接苹果 GSX (Global Service Exchange) 或 MDM 封禁查询接口
    # 当前默认返回 False（未封禁），后续需实现以下逻辑：
    #   1. 通过 Apple Business Manager API 查询设备激活锁状态
    #   2. 检查序列号是否在 GSX 黑名单中
    #   3. 返回封禁状态及原因
    return False

def continue_send() -> dict:
    """继续发送"""
    return {"action": "continue"}
