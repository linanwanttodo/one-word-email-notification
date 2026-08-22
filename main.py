"""
随机一言 - 主程序入口
获取一言并根据配置发送通知

运行方式（在项目根目录）:
    python main.py
"""

import os

from dotenv import load_dotenv

# 加载环境变量（.env 文件）
load_dotenv()

from app.api import get_hitokoto
from app.notifiers import send_serverchan, send_email


def main():
    """主函数"""
    print("=" * 60)
    print("随机一言")
    print("=" * 60)

    # 获取一言
    print()
    print("正在获取一言...")
    result = get_hitokoto()

    if not result:
        print("[失败] 获取一言失败")
        return

    message = result['text']
    print(f"[成功] 获取成功: {message}")
    print()

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
            print()
            print("[Server酱]")
            send_serverchan(message, "每日一言")
        elif notifier == 'email':
            print()
            print("[邮件]")
            send_email(message, "随机一言")
        else:
            print()
            print(f"[警告] 未知的通知方式: {notifier}")

    print()
    print("=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()