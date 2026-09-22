"""
一言 API 接口（多源适配）
通过环境变量 YIYAN_SOURCE 选择一言来源:
    - apihz:     接口盒子随机一言（默认，需 YIYAN_API_ID / YIYAN_API_KEY）
                 官网: https://www.apihz.cn/
    - hitokoto:  一言 hitokoto.cn（无需 key）
                 文档: https://developer.hitokoto.cn/sentence/

各源统一返回:
    {'text': '一言内容', 'tips': '来源信息'}
失败返回 None
"""

import os
import time

import requests

REQUEST_TIMEOUT = 10
RETRY_COUNT = 3


def _request_with_retry(url, params=None):
    """带重试的 GET 请求，最多 RETRY_COUNT 次，退避间隔递增。"""
    response = None
    for attempt in range(RETRY_COUNT):
        if attempt > 0:
            time.sleep(attempt * 2)
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == RETRY_COUNT - 1:
                raise e
            print(f"请求失败（第 {attempt + 1} 次），即将重试: {e}")
    return None


def _get_apihz():
    """接口盒子随机一言。返回统一结构或 None。"""
    api_id = os.getenv('YIYAN_API_ID', '')
    api_key = os.getenv('YIYAN_API_KEY', '')

    if not api_id or not api_key:
        print("错误: apihz 源需要配置 YIYAN_API_ID 或 YIYAN_API_KEY 环境变量")
        return None

    try:
        url = 'https://cn.apihz.cn/api/yiyan/api.php'
        response = _request_with_retry(url, params={'id': api_id, 'key': api_key})
        result = response.json()

        if result.get('code') == 200:
            return {'text': result.get('msg', ''), 'tips': '接口盒子随机一言'}
        print(f"API 错误 (code={result.get('code')}): {result.get('msg', '未知错误')}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None


def _get_hitokoto():
    """一言 hitokoto.cn（无需 key）。返回统一结构或 None。"""
    try:
        # c=d/i/h: 文学/诗词/影视分类
        url = 'https://v1.hitokoto.cn/'
        response = _request_with_retry(url + '?c=d&c=i&c=h')
        result = response.json()

        text = result.get('hitokoto', '')
        if not text:
            print("API 错误: 返回内容为空")
            return None

        source = result.get('from') or ''
        author = result.get('from_who') or ''
        tips_parts = [part for part in (f"《{source}》" if source else '', author) if part]
        tips = 'hitokoto · ' + (' '.join(tips_parts) if tips_parts else '一言')
        return {'text': text, 'tips': tips}
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None


# 源注册表：新增来源时实现一个 _get_xxx 函数并登记到这里
SOURCES = {
    'apihz': _get_apihz,
    'hitokoto': _get_hitokoto,
}


def get_hitokoto():
    """
    获取随机一言（根据 YIYAN_SOURCE 环境变量选择来源，默认 apihz）

    返回:
        dict: {'text': '一言内容', 'tips': '来源信息'}
        或 None: 失败时返回 None
    """
    source = os.getenv('YIYAN_SOURCE', 'apihz').strip().lower()

    if source not in SOURCES:
        print(f"错误: 未知的 YIYAN_SOURCE '{source}'，可选值: {', '.join(SOURCES)}")
        return None

    return SOURCES[source]()


if __name__ == '__main__':
    """测试代码（在项目根目录运行: python -m app.api）"""
    result = get_hitokoto()
    if result:
        print(f"一言: {result['text']}")
        print(f"来源: {result['tips']}")
    else:
        print("获取失败")
