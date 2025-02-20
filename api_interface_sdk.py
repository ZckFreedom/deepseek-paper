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


def get_api_correction_sdk(text, model, api_key, base_url=""):
    """统一API入口"""
    model_map = {
        "deepseek-r1": "deepseek-r1",
        "deepseek-chat": "deepseek-chat",
        "deepseek-r1-aliyun": "deepseek-r1",
        "deepseek-chat-aliyun": "deepseek-v3",
        "deepseek-r1-siliconflow": "deepseek-ai/DeepSeek-R1",
        "deepseek-chat-siliconflow": "deepseek-ai/DeepSeek-V3",
        "deepseek-r1-tencent": "deepseek-r1",
        "deepseek-chat-tencent": "deepseek-v3",
        "deepseek-r1-scnet": "DeepSeek-R1-Distill-Qwen-32B"
    }

    if model not in model_map:
        raise ValueError(f"不支持的模型: {model}")
        
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    prompt = build_prompt(text)

    completion = client.chat.completions.create(
        model=model_map[model],  # 指定请求的版本
        messages=[{"role": "system", "content": "您是一位专业的数学学术论文编辑"}, {"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
