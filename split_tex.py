import os
import re


def split_tex_file(input_path, output_dir):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割导言区和正文
    preamble, body, tail = split_preamble(content)  # 返回文章的三个部分：摘要前的设置，摘要后参考文献前的文章主体，和参考文献
    chuncks = split_by_section(body)  # 按顶层章节切分，每章一块

    # 生成分割文件，首先生成头部文件
    preamble_tex_path = os.path.join(output_dir, f"preamble.tex")
    output_files = [preamble_tex_path]
    with open(preamble_tex_path, 'w', encoding='utf-8') as f:
        f.write(preamble)

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # 每个章节单独生成一个文件
    for i, section_content in enumerate(chuncks, 1):
        output_path = os.path.join(output_dir, f"{base_name}_part{i}.tex")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(section_content)
        output_files.append(output_path)

    # 尾部文件
    tail_tex_path = os.path.join(output_dir, f"tail.tex")
    output_files.append(tail_tex_path)
    with open(tail_tex_path, 'w', encoding='utf-8') as f:
        f.write(tail)

    return output_files


def split_preamble(content):
    begin_doc = '\\begin{abstract}'
    end_doc = '\\begin{thebibliography}'
    end_docbib = '\\bibliography'
    doc_start = content.find(begin_doc)
    doc_end = content.find(end_doc)
    doc_endbib = content.find(end_docbib)

    if doc_start == -1:
        raise ValueError("未找到摘要")
    # 同时兼容 thebibliography 环境与 \bibliography 命令，取先出现者
    end_candidates = [pos for pos in (doc_end, doc_endbib) if pos != -1]
    if not end_candidates:
        raise ValueError("未找到参考文献")
    doc_end = min(end_candidates)

    preamble = content[:doc_start]  # 摘要前的设置，不需要更改
    tail = content[doc_end:]  # 参考文献部分，不需要更改
    body = content[doc_start:doc_end].strip()
    return preamble, body, tail


# 匹配顶层章节标题：\chapter{...} / \section{...}，支持带 * 和 [短标题] 的形式。
# 不匹配 \subsection / \subsubsection，也不匹配以 % 开头的注释行。
SECTION_PATTERN = re.compile(
    r'^\s*\\(?:chapter|section)\*?(?:\s*\[[^\]]*\])?\s*\{'
)


def split_by_section(body):
    r"""
    按 LaTeX 章节切分正文，每个 \chapter / \section 为一个块。

    摘要及其后、首个章节标题之前的内容单独成块；
    章节内的数学公式、表格、图片等环境保持完整，不会被切断。
    现代大模型上下文足够长，不再按字符数强行拆散章节。
    """
    chunks = []
    current_lines = []

    def flush():
        chunk = '\n'.join(current_lines).strip()
        if chunk:
            chunks.append(chunk)
        current_lines.clear()

    for line in body.splitlines():
        is_section = (
            SECTION_PATTERN.match(line) is not None
            and not line.lstrip().startswith('%')
        )
        if is_section and current_lines:
            flush()
        current_lines.append(line)

    flush()
    return chunks
