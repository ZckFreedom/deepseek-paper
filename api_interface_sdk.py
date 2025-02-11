from openai import OpenAI


def build_prompt(text):
    """构建平台特定的提示词"""
    base_prompt = (
        "请严格遵循以下要求处理文本内容：\n"
        "1. 仅修改英文文本内容\n"
        "2. 保持所有LaTeX命令和数学公式原样\n"
        "3. 修正语法错误并优化学术表达\n"
        "4. 仅输出处理后的文本内容\n"
        "需要处理的文本内容：\n"
    )

    return base_prompt + text


'''
def send_api_request(url, headers, data, response_processor):
    """通用API请求发送器"""
    response = requests.post(
        url,
        headers=headers,
        json=data,
        stream=True
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


def handle_deepseek(text, model, api_key, base_url):
    """处理DeepSeek系列模型"""
    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = build_prompt(text)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "您是一位专业的数学学术论文编辑"}, {"role": "user", "content": prompt}],
        stream=False
    )

    return response.choices[0].message.content


def handle_deepseek_aliyun(text, model, api_key, base_url):
    """处理DeepSeek系列模型"""
    prompt = build_prompt(text)

    model_map = {
        "deepseek-r1-aliyun": "deepseek-r1",
        "deepseek-chat-aliyun": "deepseek-chat"
    }

    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=api_key,
        # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url=base_url,
    )

    completion = client.chat.completions.create(
        model=model_map[model],  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[{"role": "system", "content": "您是一位专业的数学学术论文编辑"}, {"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


def handle_spark(text, model, api_key, base_url):
    client = OpenAI(
        # 控制台获取key和secret拼接，假使控制台获取的APIPassword是123456
        api_key=api_key,
        base_url=base_url  # 指向讯飞星火的请求地址
    )
    prompt = build_prompt(text)

    completion = client.chat.completions.create(
        model=model,  # 指定请求的版本
        messages=[{"role": "system", "content": "您是一位专业的数学学术论文编辑"}, {"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
'''


def get_api_correction_sdk(text, model, api_key, base_url=""):
    """统一API入口"""
    model_map = {
        "deepseek-r1": "deepseek-r1",
        "deepseek-chat": "deepseek-chat",
        "4.0Ultra": "4.0Ultra",
        "generalv3.5": "generalv3.5",
        "deepseek-r1-aliyun": "deepseek-r1",
        "deepseek-chat-aliyun": "deepseek-v3",
        "deepseek-r1-siliconflow": "deepseek-ai/DeepSeek-R1",
        "deepseek-chat-siliconflow": "deepseek-ai/DeepSeek-V3"
    }

    if model not in model_map:
        raise ValueError(f"不支持的模型: {model}")

    client = OpenAI(
        # 控制台获取key和secret拼接，假使控制台获取的APIPassword是123456
        api_key=api_key,
        base_url=base_url  # 指向讯飞星火的请求地址
    )
    prompt = build_prompt(text)

    completion = client.chat.completions.create(
        model=model_map[model],  # 指定请求的版本
        messages=[{"role": "system", "content": "您是一位专业的数学学术论文编辑"}, {"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
