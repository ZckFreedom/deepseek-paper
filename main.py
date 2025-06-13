from chat import chat
from paper import paper
from my_code import codefile
import configparser

MODEL_MAP = {
    "1": "deepseek-r1",
    "2": "deepseek-chat",
}


def select_model():
    """模型选择界面"""
    print("请选择要使用的API模型：")
    print("1. DeepSeek-R1\n2. DeepSeek-Chat\n")
    choice = input("请输入选项编号 (1-2)：").strip()
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

    print("目前支持:\n"
          "1：修改并润色论文\n"
          "2：对话\n"
          "3：代码\n")

    func = input("请输入选项：").strip()
    if func == '1':
        paper(model, api_key, base_url)
    elif func == '2':
        chat(model, api_key, base_url)
    elif func == '3':
        codefile(model, api_key, base_url)
    else:
        print("默认开启对话功能")
        chat(model, api_key, base_url)
