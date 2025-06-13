from openai import OpenAI


def build_prompt_polish(text):
    """构建平台特定的提示词"""
    base_prompt = (
        "请严格按照以下要求处理文本内容：\n"
        "1. 仅修改英文文本内容且保持所有LaTeX命令和数学公式原样\n"
        "2. 优化英语学术表达\n"
        "3. 仅输出原文本处理后对应的文本\n"
        "需要处理的文本内容：\n"
    )

    return base_prompt + text

def build_prompt_check(text):
    """构建平台特定的提示词"""
    base_prompt =  (
        "请严格按照以下要求处理文本内容：\n"
        "1. 仅修改英文文本内容且保持所有LaTeX命令和数学公式原样\n"
        "2. 仅检查文本中的英语语法错误，如无错误保持原样\n"
        "3. 仅输出原文本处理后对应的文本\n"
        "需要处理的文本内容：\n"
    )

    return base_prompt + text

def get_api_correction_sdk(text, model, api_key, base_url="", mode='1'):
    """统一API入口"""
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    if mode == '2':
        prompt = build_prompt_check(text)
    else:
        prompt = build_prompt_polish(text)

    completion = client.chat.completions.create(
        model=model,  # 指定请求的版本
        messages=[
            {"role": "system", "content": "You are a professional editor of IEEE TIT, Design Code and Crypt., Finite Fields and Their Appl."},
            {"role": "user", "content": prompt}],
        stream=False,
        temperature=0.3,
        timeout=None
    )

    return completion.choices[0].message.content
