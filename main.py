from chat import chat
from paper import paper


if __name__ == "__main__":
    print("目前支持1：修改并润色论文，2：对话")
    choice = input("请输入选项：").strip()
    if choice == 1:
        paper()
    elif choice == 2:
        chat()
    else:
        print("开启对话功能")
        chat()
