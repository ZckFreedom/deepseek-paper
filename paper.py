import os
from split_tex import split_tex_file
from api_interface_sdk import get_api_correction_sdk
from merge_tex import merge_tex_files
import subprocess
from pathlib import Path
import shutil


def generate_diff(original, corrected, output_dir):
    """生成LaTeX差异文档"""
    diff_path = Path(output_dir) / "diff_result.tex"

    try:
        # 生成diff文件
        subprocess.run(
            ["latexdiff --math-markup=3", original, corrected, "--flatten"],
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


def paper(model, api_key, base_url):
    print("请选择要使用的功能：")
    print("1. 全文英文润色\n"
          "2. 修正英语语法错误\n"
    )
    choice = input("请输入选项：").strip()
    get_correction = get_api_correction_sdk

    # 文件处理流程
    tex_dir_path = os.getcwd() + '/' + 'paper_ai'
    file_list = os.listdir(tex_dir_path)
    tex_files = [f for f in file_list if f.endswith('.tex')]
    tex_path = os.path.join(tex_dir_path, tex_files[0])
    base_name = os.path.splitext(os.path.basename(tex_path))[0]

    output_dir = os.path.join(tex_dir_path, 'split_tex')
    corrected_dir = os.path.join(tex_dir_path, 'corrected_tex')

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(corrected_dir, exist_ok=True)

    # 拆分文件
    split_files = split_tex_file(tex_path, output_dir)
    if choice == '2':
        prt = "开始修正英语语法错误"
    else:
        prt = "开始全文英文润色"

    print(f"{prt},成功分割为 {len(split_files)} 个文件,需要处理{len(split_files)-2}个文件")

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
                model=model,
                api_key=api_key,
                base_url=base_url,
                mode = choice
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
    print("正在处理", len(error_tex), "个错误文件(至多处理10次)")
    while len(error_tex) > 0 and error_num < 10:
        i, file_path = error_tex[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        try:
            corrected_content = get_correction(
                content,
                model=model,
                api_key=api_key,
                base_url=base_url,
                mode = choice
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
        src_file=tex_path,
        corrected_dir=corrected_dir,
        output_dir=corrected_dir
    )

    # 生成差异文档
    diff_dir = Path(tex_dir_path) / "diff_output"
    diff_dir.mkdir(exist_ok=True)

    generate_diff(
        original=tex_path,
        corrected=merged_file,
        output_dir=diff_dir
    )
