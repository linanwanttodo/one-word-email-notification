"""
随机一言 - 主程序
获取一言并根据配置发送通知
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from api import get_hitokoto
from serverchan import send_serverchan
from email_sender import send_email


def main():
    """主函数"""
    print("=" * 60)
    print("随机一言")
    print("=" * 60)

    # 获取一言
    print("\n正在获取一言...")
    result = get_hitokoto()

    if not result:
        print("[失败] 获取一言失败")
        return

    message = result['text']
    print(f"[成功] 获取成功: {message}\n")

    # 获取通知方式
    notify_type = os.getenv('NOTIFY_TYPE', '').lower()
    if not notify_type:
        print("[警告] 未配置通知方式，请检查 .env 文件中的 NOTIFY_TYPE")
        return

    # 解析通知方式
    notifiers = [n.strip() for n in notify_type.split(',')]

    print("-" * 60)
    print("发送通知")
    print("-" * 60)

    # 发送通知
    for notifier in notifiers:
        if notifier == 'serverchan':
            print("\n[Server酱]")
            send_serverchan(message, "每日一言")
        elif notifier == 'email':
            print("\n[邮件]")
            send_email(message, "随机一言")
        else:
            print(f"\n[警告] 未知的通知方式: {notifier}")

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
