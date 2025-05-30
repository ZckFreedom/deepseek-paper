import requests
import json


def send_api_request(url, headers, data, response_processor):
    """通用API请求发送器"""
    response = requests.post(
        url,
        headers=headers,
        json=data,
        stream=False
    )

    if response.status_code != 200:
        error_info = f"API请求失败 ({response.status_code}): {response.text}"
        raise ConnectionError(error_info)

    try:
        result = response.json()
        return response_processor(result)
    except KeyError as e:
        raise ValueError(f"API响应解析失败: {str(e)} 字段缺失")
    except json.JSONDecodeError:
        raise ValueError("无效的API响应格式")


def build_prompt(text):
    """构建平台特定的提示词"""
    base_prompt = (
        "请严格遵循以下要求处理文本内容：\n"
        "1. 仅修改英文文本内容且完全保持文本原意\n"
        "2. 保持所有LaTeX命令和数学公式原样\n"
        "3. 修正英语语法错误\n"
        "4. 优化英语学术表达，符合数学期刊用语\n"
        "5. 仅输出处理后的文本内容\n"
        "需要处理的文本内容：\n"
    )

    return base_prompt + text


def handle_deepseek(text, model, api_key, base_url):
    """处理DeepSeek系列模型"""
    url = base_url or "https://api.deepseek.com/v1/chat/completions"

    # 根据模型调整参数
    model_map = {
        "deepseek-r1": "deepseek-r1",
        "deepseek-chat": "deepseek-chat"
    }

    prompt = build_prompt(text)

    data = {
        "model": model_map[model],
        "messages": [
            {"role": "system", "content": "You are a professional editor of academic papers in mathematics."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 8192
    }

    return send_api_request(
        url=url,
        headers={"Authorization": f"Bearer {api_key}"},
        data=data,
        response_processor=lambda r: r['choices'][0]['message']['content']
    )


def handle_deepseek_aliyun(text, model, api_key, base_url):
    """处理DeepSeek系列模型"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = build_prompt(text)

    model_map = {
        "deepseek-r1-aliyun": "deepseek-r1",
        "deepseek-chat-aliyun": "deepseek-chat"
    }

    data = {
        "model": model_map[model],
        "messages": [
            {"role": "system", "content": "You are a professional editor of academic papers in mathematics."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }

    return send_api_request(
        url=base_url,
        headers=headers,
        data=data,
        response_processor=lambda r: r['choices'][0]['message']['content']
    )


def handle_deepseek_siliconflow(text, model, api_key, base_url):
    """处理DeepSeek系列模型"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = build_prompt(text)

    model_map = {
        "deepseek-r1-siliconflow": "deepseek-ai/DeepSeek-R1",
        "deepseek-chat-siliconflow": "deepseek-ai/DeepSeek-V3"
    }

    data = {
        "model": model_map[model],
        "messages": [
            {"role": "system", "content": "You are a professional editor of academic papers in mathematics."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }

    return send_api_request(
        url=base_url,
        headers=headers,
        data=data,
        response_processor=lambda r: r['choices'][0]['message']['content']
    )


def get_api_correction(text, model, api_key, base_url=""):
    """统一API入口"""
    model_handlers = {
        "deepseek-r1": handle_deepseek,
        "deepseek-chat": handle_deepseek,
        "deepseek-r1-aliyun": handle_deepseek_aliyun,
        "deepseek-chat-aliyun": handle_deepseek_aliyun,
        "deepseek-r1-siliconflow": handle_deepseek_siliconflow,
        "deepseek-chat-siliconflow": handle_deepseek_siliconflow
    }

    if model not in model_handlers:
        raise ValueError(f"不支持的模型: {model}")

    return model_handlers[model](text, model, api_key, base_url)
