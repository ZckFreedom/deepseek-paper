from openai import OpenAI


def build_prompt(text):
    """构建平台特定的提示词"""
    base_prompt = (
        "请严格遵循以下要求处理文本内容：\n"
        "1. 仅修改英文文本内容\n"
        "2. 保持所有LaTeX命令和数学公式原样\n"
        "3. 修正英语语法错误\n"
        "4. 优化英语学术表达，使其更符合数学专业期刊用语\n"
        "5. 仅输出处理后的文本内容\n"
        "需要处理的文本内容：\n"
    )

    return base_prompt + text


def get_api_correction_sdk(text, model, api_key, base_url=""):
    """统一API入口"""
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    prompt = build_prompt(text)

    completion = client.chat.completions.create(
        model=model,  # 指定请求的版本
        messages=[
            {"role": "system", "content": "You are a professional editor of academic papers in mathematics."},
            {"role": "user", "content": prompt}],
        stream=False,
        temperature=0.3,
        timeout=None
    )

    return completion.choices[0].message.content
