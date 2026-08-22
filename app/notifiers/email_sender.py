"""
邮件通知模块
支持 HTML 格式邮件
"""

import os
import smtplib
from datetime import datetime
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# 邮件模板路径（基于模块文件位置定位，不依赖运行时工作目录）
# app/notifiers/email_sender.py -> 项目根目录/templates/email_template.html
TEMPLATE_PATH = Path(__file__).resolve().parent.parent.parent / 'templates' / 'email_template.html'


def load_template():
    """
    加载邮件模板

    返回:
        str: 模板内容
    """
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[失败] 邮件: 未找到邮件模板文件 {TEMPLATE_PATH}")
        return None
    except Exception as e:
        print(f"[失败] 邮件: 读取模板失败 - {e}")
        return None


def send_email(message, title="随机一言"):
    """
    发送邮件通知

    参数:
        message (str): 邮件内容
        title (str): 邮件标题，默认"随机一言"

    返回:
        bool: 成功返回 True，失败返回 False
    """
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT', '587')
    username = os.getenv('SMTP_USERNAME')
    password = os.getenv('SMTP_PASSWORD')
    email_from = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')

    # 检查必要配置
    if not all([smtp_host, username, password, email_from, email_to]):
        print("[失败] 邮件: 配置不完整")
        return False

    # 检查消息
    if not message:
        print("[失败] 邮件: 消息内容为空")
        return False

    try:
        # 加载模板
        template = load_template()
        if not template:
            # 如果模板加载失败，使用纯文本
            msg = MIMEText(message, 'plain', 'utf-8')
        else:
            # 使用 HTML 模板
            # 替换变量
            date_str = datetime.now().strftime('%Y年%m月%d日 %H:%M')
            html_content = template.replace('{content}', message).replace('{date}', date_str)

            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        msg['Subject'] = title
        msg['From'] = formataddr(['随机一言', email_from])
        msg['To'] = email_to

        # 连接 SMTP 服务器
        if smtp_port == '465':
            server = smtplib.SMTP_SSL(smtp_host, int(smtp_port))
        else:
            server = smtplib.SMTP(smtp_host, int(smtp_port))
            server.starttls()

        server.login(username, password)
        server.sendmail(email_from, [email_to], msg.as_string())
        server.quit()

        print(f"[成功] 邮件: 已发送至 {email_to}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[失败] 邮件: 认证失败，请检查用户名和密码")
        return False
    except smtplib.SMTPConnectError:
        print("[失败] 邮件: 无法连接到 SMTP 服务器")
        return False
    except Exception as e:
        print(f"[失败] 邮件: {e}")
        return False


if __name__ == '__main__':
    """测试代码（在项目根目录运行: python -m app.notifiers.email_sender）"""
    send_email("生活明朗，万物可爱。", "测试邮件")