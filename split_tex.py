import os
import re


def split_tex_file(input_path, output_dir):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割导言区和正文
    preamble, body, tail = split_preamble(content)  # 返回文章的三个部分，摘要前的设置，摘要后参考文献前的文章主体，和参考文献
    chuncks = split_by_character_limit_with_protection(body)  # 按照section将文章主体分块

    # 生成分割文件,首先生成头部文件
    preamble_tex_path = os.path.join(output_dir, f"preamble.tex")
    output_files = [preamble_tex_path]
    preamble_tex_content = open(preamble_tex_path, 'w', encoding='utf-8')
    preamble_tex_content.write(preamble)

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # 文章主体按section分别生成
    for i, section_content in enumerate(chuncks, 1):
        full_content = section_content
        output_path = os.path.join(output_dir, f"{base_name}_part{i}.tex")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        output_files.append(output_path)

    # 尾部文件
    tail_tex_path = os.path.join(output_dir, f"tail.tex")
    output_files.append(tail_tex_path)
    tail_tex_content = open(tail_tex_path, 'w', encoding='utf-8')
    tail_tex_content.write(tail)

    return output_files


def split_preamble(content):
    begin_doc = '\\begin{abstract}'
    end_doc = '\\begin{thebibliography}'
    doc_start = content.find(begin_doc)
    doc_end = content.find(end_doc)

    if doc_start == -1:
        raise ValueError("未找到摘要")
    if doc_end == -1:
        raise ValueError("未找到参考文献")

    preamble = content[:doc_start]  # 摘要前的设置，不需要更改
    tail = content[doc_end:]  # 参考文献后的设置，不需要更改

    body = content[doc_start:doc_end].strip()
    return preamble, body, tail


def split_by_character_limit_with_protection(body, max_chars=4092):
    """
    将文件内容按照字符数限制分割成多个块，每块最多包含 max_chars 个字符。
    确保 LaTeX 的特殊结构（如数学公式、环境块等）不会被分割。

    参数:
        body (str): 文件内容字符串。
        max_chars (int): 每块的最大字符数，默认为 4096。

    返回:
        list: 包含分割后块的列表，每个块是一个字符串。
    """
    # 正则表达式匹配 LaTeX 环境块（如 \begin{...}...\end{...}）
    latex_env_pattern = re.compile(r'\\begin{([^}]*)}(.*?)\\end{\1}', re.DOTALL)

    # 正则表达式匹配行内数学公式（如 $...$ 或 \(...\)）
    inline_math_pattern = re.compile(r'(\$.*?\$|\\\(.*?\\\))', re.DOTALL)

    # 分割文件内容为逻辑单元（行或特殊结构）
    def split_into_logical_units(text):
        """
        将文本分割为逻辑单元，包括普通行和 LaTeX 特殊结构。
        """
        units = []
        pos = 0
        while pos < len(text):
            # 查找 LaTeX 环境块
            env_match = latex_env_pattern.search(text, pos)
            if env_match:
                start, end = env_match.span()
                # 添加环境块前的普通文本
                if start > pos:
                    units.extend(text[pos:start].split('\n'))
                # 添加完整的环境块
                units.append(env_match.group(0))
                pos = end
                continue

            # 查找行内数学公式
            math_match = inline_math_pattern.search(text, pos)
            if math_match:
                start, end = math_match.span()
                # 添加数学公式前的普通文本
                if start > pos:
                    units.extend(text[pos:start].split('\n'))
                # 添加完整的数学公式
                units.append(math_match.group(0))
                pos = end
                continue

            # 如果没有匹配到特殊结构，则按行分割
            line_end = text.find('\n', pos)
            if line_end == -1:
                line_end = len(text)
            units.append(text[pos:line_end])
            pos = line_end + 1  # 跳过换行符

        return units

    # 获取逻辑单元
    logical_units = split_into_logical_units(body)

    # 按字符数限制组合逻辑单元
    chunks = []
    current_chunk = ""
    for unit in logical_units:
        # 如果当前块加上新单元的长度超过限制，则保存当前块并开始新块
        if len(current_chunk) + len(unit) + 1 > max_chars:  # 加 1 是为了考虑换行符
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = unit
        else:
            # 否则将当前单元添加到当前块中
            if current_chunk:
                current_chunk += '\n' + unit
            else:
                current_chunk = unit

    # 添加最后一个块（如果有内容）
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
