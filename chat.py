from openai import OpenAI
import time


def typewriter_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


def chat(model, api_key, base_url):

    client = OpenAI(api_key=api_key, base_url=base_url)

    print("开始与DeepSeek的对话。输入'退出'来结束对话。")

    messages = [
        {"role": "system", "content": "您是一位擅长代数几何码和代数函数域的数学教授，且习惯用$公式$表示数学公式"}
    ]
    while True:
        user_input = input("你: ")
        if user_input.lower() == '退出':
            print("对话结束。")
            break

        messages.append({"role": "user", "content": f"{user_input}"})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=0.1,
                timeout=None
            )

            print("DeepSeek: ", end="", flush=True)  # 实时输出前缀
            full_response = []
            reasoning_log = []

            # 实时处理每个chunk
            for chunk in response:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", "") or ""
                reasoning = getattr(delta, "reasoning_content", "") or ""

                # 状态跟踪变量
                is_new_answer = False

                # 处理推理内容
                if reasoning:
                    # 如果是首次出现推理内容
                    if not hasattr(response, '_seen_reasoning'):
                        print("\n【推理过程】", end="", flush=True)
                        response._seen_reasoning = True

                    typewriter_print(reasoning)
                    reasoning_log.append(reasoning)
                    hasattr(response, '_seen_answer') and delattr(response, '_seen_answer')

                # 处理正式回答内容
                if content:
                    # 如果是从推理切换到回答
                    if hasattr(response, '_seen_reasoning') and not hasattr(response, '_seen_answer'):
                        print("\n【最终回答】", end="", flush=True)  # 添加明确的分隔标识
                        response._seen_answer = True
                        is_new_answer = True

                    # 如果是首次回答且没有推理过程
                    if not hasattr(response, '_seen_reasoning') and not hasattr(response, '_seen_answer'):
                        print("\n【回答】", end="", flush=True)
                        response._seen_answer = True
                        is_new_answer = True

                    # 格式化输出（如果是新回答的第一个字符前加空格）
                    formatted_content = f" {content.strip()}" if is_new_answer and content.startswith(' ') else content
                    typewriter_print(formatted_content)
                    full_response.append(content)

                # 每轮对话结束后重置状态
            print()  # 保证最后换行
            messages.append({"role": "assistant", "content": ''.join(full_response)})

        except Exception as e:
            print(f"API调用失败：{str(e)}")
