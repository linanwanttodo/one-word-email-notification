"""
通知渠道包

统一导出各通知渠道的发送函数。
新增通知渠道时，在对应模块中实现发送函数并在此导出即可。
"""

from app.notifiers.serverchan import send_serverchan
from app.notifiers.email_sender import send_email

__all__ = ["send_serverchan", "send_email"]