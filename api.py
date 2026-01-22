"""
一言 API 接口
使用接口盒子官方 API 获取随机一言
官网: https://www.apihz.cn/
"""

import os
import requests
import json

# 从环境变量读取配置
YIYAN_API_ID = os.getenv('YIYAN_API_ID', '')
YIYAN_API_KEY = os.getenv('YIYAN_API_KEY', '')


def get_hitokoto():
    """
    获取随机一言

    返回:
        dict: 包含一言信息的字典
        {
            'text': '一言内容',
            'tips': '来源信息'
        }
        或 None: 失败时返回 None
    """
    if not YIYAN_API_ID or not YIYAN_API_KEY:
        print("错误: 未配置 YIYAN_API_ID 或 YIYAN_API_KEY 环境变量")
        return None
        
    try:
        # 使用接口盒子官方 API 的随机一言接口
        url = 'https://cn.apihz.cn/api/yiyan/api.php'
        
        params = {
            'id': YIYAN_API_ID,
            'key': YIYAN_API_KEY,
        }

        response = requests.get(url, params=params, timeout=10, verify=False)
        response.raise_for_status()

        result = response.json()

        if result.get('code') == 200:
            # API 返回的消息就是一言内容
            msg = result.get('msg', '')
            return {
                'text': msg,
                'tips': '接口盒子随机一言'
            }
        else:
            print(f"API 错误 (code={result.get('code')}): {result.get('msg', '未知错误')}")
            return None

    except requests.exceptions.Timeout:
        print("请求超时")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None


if __name__ == '__main__':
    """测试代码"""
    result = get_hitokoto()
    if result:
        print(f"一言: {result['text']}")
        print(f"来源: {result['tips']}")
    else:
        print("获取失败")
