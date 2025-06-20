import os
import subprocess
import platform

Mode_MAP = {
    "codes": "codes",
    "chat": "chat_content"
}

Ex_MAP ={
    "sage": "sagemath",
    "py": "python",
    "mag": "magma"
}

def sanitize_filename(input_str: str) -> str:
    """清理文件名中的非法字符"""
    # 替换非法字符为下划线
    valid_chars = "-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    cleaned = ''.join(c if c in valid_chars else '_' for c in input_str)
    # 去除首尾空白并限制长度
    return cleaned.strip()[:10]


def get_unique_filename(base_name: str, ex: str, mode: str) -> str:
    """生成唯一的文件名"""
    target_dir = os.path.join(os.getcwd(), Mode_MAP[mode])
    if mode == 'codes':
        target_dir = target_dir + '/' + Ex_MAP[ex]

    file_path = os.path.join(target_dir, f"{base_name}.{ex}")
    if not os.path.exists(file_path):
        return file_path
    counter = 1
    new_name = f"{base_name}_{counter}.{ex}"
    file_path = os.path.join(target_dir, new_name)
    while os.path.exists(file_path):
        counter += 1
        new_name = f"{base_name}_{counter}.{ex}"
        file_path = os.path.join(target_dir, new_name)
    return file_path


def save_to_file(content: str, filename: str, ex: str, mode: str):
    """安全保存内容到文件"""
    try:
        # 验证文件路径安全性
        if os.path.isabs(filename):
            raise ValueError("绝对路径不被允许")

        # 检查文件是否已存在，并生成完整路径
        full_path = get_unique_filename(filename, ex, mode)

        # 写入文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write("% Auto-generated by DeepSeek API\n\n")
            f.write(content)

        print(f"成功保存到：{full_path}")
        return full_path

    except Exception as e:
        print(f"保存文件时出错：{str(e)}")


def load_python_file(filename, ex, mode):
    # 生成完整路径
    full_path = os.getcwd() +'/' + Mode_MAP[mode]+ '/' + Ex_MAP[ex] + '/' + f"/{filename}.{ex}"

    # 读取文件
    print(f"正在读取{filename}文件的代码")
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

            return content
    except Exception as e:
        print(f"读取文件时出错：{str(e)}")


def compile_latex_and_open(tex_file_path):
    """
    编译 LaTeX 文件并打开生成的 PDF
    """
    # 获取文件所在目录和基本文件名
    tex_dir = os.path.dirname(tex_file_path)
    base_name = os.path.splitext(os.path.basename(tex_file_path))[0]
    pdf_path = os.path.join(tex_dir, f"{base_name}.pdf")

    # 尝试使用 pdflatex 编译
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file_path],
            cwd=tex_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print("pdflatex 编译成功！")
        else:
            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", tex_file_path],
                cwd=tex_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
        )
        open_pdf(pdf_path)

    except Exception as e:
        print(f"编译过程中发生异常: {str(e)}")


def open_pdf(pdf_path):
    """根据操作系统打开 PDF 文件"""
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', pdf_path])
        elif platform.system() == 'Windows':  # Windows
            os.startfile(pdf_path)
        else:  # Linux 及其他
            subprocess.run(['xdg-open', pdf_path])
        print(f"已打开 PDF 文件: {pdf_path}")
    except Exception as e:
        print(f"无法打开 PDF 文件: {str(e)}")