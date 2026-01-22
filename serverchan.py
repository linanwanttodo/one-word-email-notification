"""
Server酱 通知模块
通过 Server酱 发送微信推送通知
"""

import requests
import os


def send_serverchan(message, title="每日一言"):
    """
    发送 Server酱 通知

    参数:
        message (str): 通知内容
        title (str): 通知标题，默认"每日一言"

    返回:
        bool: 成功返回 True，失败返回 False
    """
    key = os.getenv('SERVERCHAN_KEY')

    if not key:
        print("[失败] Server酱: 未配置 SERVERCHAN_KEY")
        return False

    if not message:
        print("[失败] Server酱: 消息内容为空")
        return False

    try:
        url = f"https://sctapi.ftqq.com/{key}.send"
        data = {
            "title": title,
            "desp": message
        }

        response = requests.post(url, data=data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get('code', -1) == 0:
                print("[成功] Server酱: 发送成功")
                return True
            else:
                print(f"[失败] Server酱: {result.get('message', '发送失败')}")
                return False
        else:
            print(f"[失败] Server酱: HTTP {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        print("[失败] Server酱: 请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[失败] Server酱: {e}")
        return False
    except Exception as e:
        print(f"[失败] Server酱: {e}")
        return False


if __name__ == '__main__':
    """测试代码"""
    send_serverchan("这是一条测试消息")
