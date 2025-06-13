from openai import OpenAI
import time
from filefunctions import save_to_file,load_python_file

Function_MAP = {
    "1": "generation",
    "2": "comments",
    "3": "optimization",
    "4": "conversion",
}

Extend_MAP = {
    "1": "py",
    "2": "sage",
    "3": "mag",
}


def prompt_map(choice, ex):
    prompt_maps = {
        "1": f"请帮我生成一段能够实现以下要求的{ex}代码：",
        "2": f"请按照要求帮我给下面一段{ex}代码添加注释：",
        "3": f"请按照要求帮我优化下面一段{ex}代码，并在优化部分添加注释：",
        "4": f"请将下面的SageMath代码转换为Magma代码，仅输出转换后的Magma代码",
    }
    return prompt_maps.get(choice, None)


def select_code():
    print("请选择要使用的代码：")
    print("1. Python\n"
          "2. SageMath\n"
          "3. Magma\n"
          )
    choice = input("请输入选项编号 (1-3)：").strip()
    return Extend_MAP.get(choice, 'py')


def select_function():
    print("请选择需要的功能：")
    print("1. 代码生成\n"
          "2. 代码添加注释\n"
          "3. 代码优化\n"
          "4. SageMath代码转Magma代码\n"
          )
    choice = input("请输入选项编号 (1-4)：").strip()

    func = Function_MAP.get(choice, None)
    if choice == "4":
        return func, prompt_map(choice, ""), "sage", "mag"

    code_ex = select_code()
    return func, prompt_map(choice, code_ex), code_ex, code_ex


def typewriter_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


def codefile(model, api_key, base_url):
    func, base_prompt, input_ex, output_ex = select_function()

    if not func:
        print("请重新启动并输入正确编号。")
        return 0

    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": "您是一位精通编程的数学教授"}
    ]
    try:
        user_input = input("请输入要求: ")
        prompt = base_prompt + user_input
        prompt += f"仅输出结果中的{output_ex}代码:\n"

        filename = input("请输入文件名：")
        if func == 'generation':
            content = ''
        else:
            content = load_python_file(filename, input_ex, 'codes')
        prompt += content

        messages.append({"role": "user", "content": prompt})
        print("开始请求deepseek并生成代码")
        response = client.chat.completions.create(
            model=model,  # 指定请求的版本
            messages=messages,
            stream=True,
            temperature=0.3,
            timeout=None
        )

        print("DeepSeek: ", end="", flush=True)  # 实时输出前缀
        full_code = []

        for chunk in response:
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", "") or ""
            reasoning = getattr(delta, "reasoning_content", "") or ""

            if reasoning:
                # 如果是首次出现推理内容
                if not hasattr(response, '_seen_reasoning'):
                    print("\n【推理过程】", end="", flush=True)
                    response._seen_reasoning = True

                typewriter_print(reasoning)
                hasattr(response, '_seen_answer') and delattr(response, '_seen_answer')

            if content:
                full_code.append(content)

        full_code = "".join(full_code)

        save_to_file(full_code, filename, output_ex, "codes")

    except Exception as e:
        print(f"处理时出错，请重试,{str(e)}")
