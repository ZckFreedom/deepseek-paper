import os
import configparser
from split_tex import split_tex_file
from api_interface import get_api_correction
from api_interface_sdk import get_api_correction_sdk
from merge_tex import merge_tex_files
import subprocess
from pathlib import Path
import shutil

MODEL_MAP = {
    "1": "deepseek-r1",
    "2": "deepseek-chat",
    "3": "deepseek-r1-aliyun",
    "4": "deepseek-chat-aliyun",
    "5": "deepseek-r1-siliconflow",
    "6": "deepseek-chat-siliconflow"
}


def select_model():
    """模型选择界面"""
    print("请选择要使用的API模型：")
    print("1. DeepSeek-R1\n2. DeepSeek-Chat\n"
          "3. Bailian-deepseek-r1\n4. Bailian-deepseek-chat\n"
          "5. Siliconflow-deepseek-r1\n6. Siliconflow-deepseek-chat")
    choice = input("请输入选项编号 (1-8)：").strip()
    return MODEL_MAP.get(choice, "deepseek-r1")


def generate_diff(original, corrected, output_dir):
    """生成LaTeX差异文档"""
    diff_path = Path(output_dir) / "diff_result.tex"

    try:
        # 生成diff文件
        subprocess.run(
            ["latexdiff", original, corrected, "--flatten"],
            check=True,
            stdout=open(diff_path, 'w', encoding='utf-8')
        )

        # 生成PDF对比文档
        subprocess.run(
            ["pdflatex", "-output-directory", output_dir, diff_path],
            check=True
        )
        print(f"差异文档已生成：{diff_path.with_suffix('.pdf')}")
    except subprocess.CalledProcessError as e:
        print(f"生成差异文档失败：{str(e)}")


def main():
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 选择模型
    selected_model = select_model()
    api_key = config[selected_model]['API_KEY']

    print("请选择要使用的API调用：1：对应API调用\n2：统一Open-ai SDK调用")
    gpt_choice = input()

    if gpt_choice == '2':
        get_correction = get_api_correction_sdk
        base_url = config[selected_model].get('BASE_URL_OPENAI', '')  # 可选参数
    else:
        get_correction = get_api_correction
        base_url = config[selected_model].get('BASE_URL', '')  # 可选参数

    # 验证配置
    if not config.has_section(selected_model):
        raise ValueError(f"配置文件中缺少 {selected_model} 的配置")

    # 文件处理流程
    input_file = input("请输入要处理的TeX文件路径：")
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    output_dir = os.path.join(os.path.dirname(input_file), 'split_tex')
    corrected_dir = os.path.join(os.path.dirname(input_file), 'corrected_tex')

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(corrected_dir, exist_ok=True)

    # 拆分文件
    split_files = split_tex_file(input_file, output_dir)
    print(f"成功分割为 {len(split_files)} 个文件")
    split_files_body = split_files[1:len(split_files)-1]
    preamble_tex = split_files[0]
    tail_tex = split_files[-1]
    shutil.move(preamble_tex, os.path.join(corrected_dir, 'preamble.tex'))
    shutil.move(tail_tex, os.path.join(corrected_dir, 'tail.tex'))

    error_tex = []
    # 批量处理
    for i, file_path in enumerate(split_files_body, 1):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        try:
            corrected_content = get_correction(
                content,
                model=selected_model,
                api_key=api_key,
                base_url=base_url
            )

            output_path = os.path.join(
                corrected_dir,
                f"{base_name}_part{i}_corrected.tex"
            )

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            print(f"成功处理: {output_path}")

        except Exception as e:
            error_tex.append((i, file_path))
            print(f"处理文件 {file_path} 时出错: {str(e)}")

    error_num = 0
    print("正在处理", len(error_tex), "个错误文件")
    while len(error_tex) > 0 and error_num < 10:
        i, file_path = error_tex[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        try:
            corrected_content = get_correction(
                content,
                model=selected_model,
                api_key=api_key,
                base_url=base_url
            )

            output_path = os.path.join(
                corrected_dir,
                f"{base_name}_part{i}_corrected.tex"
            )

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)
            print(f"成功处理: {output_path}")
            error_tex.pop(0)

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")
            error_num += 1

    if len(error_tex) > 0:
        print("部分文件纠错失败，请注意单独处理!")
        print(error_tex)
        while len(error_tex) > 0:
            i, file_path = error_tex[0]
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            output_path = os.path.join(
                corrected_dir,
                f"{base_name}_part{i}_corrected.tex"
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            error_tex.pop(0)
    print("所有文件处理完成")

    # 合并校正后的文件
    merged_file = merge_tex_files(
        src_file=input_file,
        corrected_dir=corrected_dir,
        output_dir=corrected_dir
    )

    # 生成差异文档
    diff_dir = Path(os.path.dirname(input_file)) / "diff_output"
    diff_dir.mkdir(exist_ok=True)

    generate_diff(
        original=input_file,
        corrected=merged_file,
        output_dir=diff_dir
    )


if __name__ == "__main__":
    main()
