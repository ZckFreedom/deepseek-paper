import os
from openai import OpenAI


Function_MAP = {
    "1": "generation",
    "2": "comments",
    "3": "optimization",
}

Prompt_MAP = {
    "1": "请帮我生成一段能够实现以下要求的sagemath代码：",
    "2": "请按照要求帮我给下面一段sagemath代码添加注释：",
    "3": "请按照要求帮我优化下面一段sagemath代码，并在优化部分添加注释：",
}


def select_function():
    print("请选择需要的功能：")
    print("1. 代码生成\n"
          "2. 代码添加注释\n"
          "3. 代码优化\n"
          )
    choice = input("请输入选项编号 (1-3)：").strip()
    return Function_MAP.get(choice, None), Prompt_MAP.get(choice, None)


def sanitize_filename(input_str: str) -> str:
    """清理文件名中的非法字符"""
    # 替换非法字符为下划线
    valid_chars = "-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cleaned = ''.join(c if c in valid_chars else '_' for c in input_str)
    # 去除首尾空白并限制长度
    return cleaned.strip()[:10]


def get_unique_filename(base_name: str) -> str:
    """生成唯一的文件名"""
    counter = 1
    new_name = f"{base_name}_{counter}.sage"
    while os.path.exists(f"{new_name}.sage"):
        counter += 1
        new_name = f"{base_name}_{counter}.sage"
    return new_name


def save_api_response_to_file(content: str, filename: str):
    """安全保存内容到文件"""
    try:
        # 验证文件路径安全性
        if os.path.isabs(filename):
            raise ValueError("绝对路径不被允许")

        # 检查文件是否已存在，并生成完整路径
        if os.path.exists(f"{filename}.sage"):
            unique_name = get_unique_filename(filename)
            full_path = os.getcwd() + '/' + unique_name
        else:

            full_path = os.getcwd() + f"/{filename}.sage"

        # 写入文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write("# Auto-generated by DeepSeek API\n\n")
            f.write(content)

        print(f"成功保存到：{full_path}")

    except Exception as e:
        print(f"保存文件时出错：{str(e)}")


def load_python_file(filename):
    # 生成完整路径
    full_path = os.getcwd() + f"/{filename}.sage"

    # 读取文件
    print(f"正在读取{filename}文件的代码")
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

            return content
    except Exception as e:
        print(f"读取文件时出错：{str(e)}")


def sagefile(model, api_key, base_url):

    func, base_prompt = select_function()
    if not func:
        print("请重新启动并输入正确编号。")
        return 0

    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": "您是一位数学软件SagaMath的程序员"}
    ]
    try:
        user_input = input("请输入要求: ")
        prompt = base_prompt + user_input
        prompt += "仅输出结果中的python代码:\n"

        filename = input("请输入文件名：")
        if func == 'generation':
            content = ''
        else:
            content = load_python_file(filename)
        prompt += content

        messages.append({"role": "user", "content": prompt})
        print("开始请求deepseek并生成代码")
        completion = client.chat.completions.create(
            model=model,  # 指定请求的版本
            messages=messages,
            stream=False,
            temperature=0.3,
            timeout=None
        )

        return_content = completion.choices[0].message.content
        reason_content = completion.choices[0].message.reasoning_content
        print("推理过程：", end='')
        print(reason_content)

        save_api_response_to_file(return_content, filename)

    except Exception as e:
        print(f"处理时出错，请重试,{str(e)}")
