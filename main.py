from chat import chat
from paper import paper
from pyfile import pyfile
import configparser

MODEL_MAP = {
    "1": "deepseek-r1",
    "2": "deepseek-chat",
    "3": "deepseek-r1-aliyun",
    "4": "deepseek-v3-aliyun",
    "5": "deepseek-r1-siliconflow",
    "6": "deepseek-chat-siliconflow",
    "7": "deepseek-r1-tencent",
    "8": "deepsee-v3-tencent",
    "9": "deepseek-r1-scnet",
}


def select_model():
    """模型选择界面"""
    print("请选择要使用的API模型：")
    print("1. DeepSeek-R1\n2. DeepSeek-Chat\n"
          "3. Bailian-deepseek-r1\n4. Bailian-deepseek-chat\n"
          "5. Siliconflow-deepseek-r1\n6. Siliconflow-deepseek-chat"
          "7. Tencent-deepseek-r1\n8. Tencent-deepseek-chat\n"
          "9. Scnet-deepseek-r1")
    choice = input("请输入选项编号 (1-9)：").strip()
    return MODEL_MAP.get(choice, "deepseek-r1")


config = configparser.ConfigParser()
try:
    with open('config_private.ini') as f:
        config.read_file(f)
except FileNotFoundError:
    config.read('config.ini')

if __name__ == "__main__":
    select_model = select_model()

    # 验证配置
    if not config.has_section(select_model):
        raise ValueError(f"配置文件中缺少 {select_model} 的配置")

    model = config[select_model]['MODEL']
    api_key = config[select_model]['API_KEY']
    base_url = config[select_model].get('BASE_URL_OPENAI', '')

    print("本脚本使用统一Open-ai SDK调用，如果需要其他方法参考api_interface文件。")

    print("目前支持1：修改并润色论文，2：对话，3：Python代码")

    func = input("请输入选项：").strip()
    if func == '1':
        paper(model, api_key, base_url)
    elif func == '2':
        chat(model, api_key, base_url)
    elif func == '3':
        pyfile(model, api_key, base_url)
    else:
        print("默认开启对话功能")
        chat(model, api_key, base_url)
