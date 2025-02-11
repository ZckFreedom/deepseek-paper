import os
import re
from pathlib import Path


def merge_tex_files(src_file, corrected_dir, output_dir):
    """合并校正后的分块文件"""

    # 获取分块文件列表并按数字排序
    base_name = Path(src_file).stem
    chunk_files = sorted(
        [f for f in os.listdir(corrected_dir) if f.startswith(base_name)],
        key=lambda x: int(re.search(r'part(\d+)', x).group(1))
    )

    # 重建完整内容，首先是头部文件
    preamble_tex_path = os.path.join(corrected_dir, "preamble.tex")
    preamble_tex_content = open(preamble_tex_path, 'r', encoding='utf-8').read()
    merged_content = [preamble_tex_content]

    # 文章主体
    for file_name in chunk_files:
        with open(Path(corrected_dir) / file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            merged_content.append(content)

    tail_tex_path = os.path.join(corrected_dir, "tail.tex")
    tail_tex_content = open(tail_tex_path, 'r', encoding='utf-8').read()
    merged_content.append(tail_tex_content)

    # 组合完整文档
    final_content = '\n'.join(merged_content)

    # 保存合并文件
    merged_path = Path(output_dir) / f"merged_{Path(src_file).name}"
    with open(merged_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    return merged_path


'''
merged_file = merge_tex_files(
        src_file="C:/Users/zhu20/Desktop/研究工作/论文/编码/123123/1.tex",
        corrected_dir="C:/Users/zhu20/Desktop/研究工作/论文/编码/123123/corrected_tex",
        output_dir="C:/Users/zhu20/Desktop/研究工作/论文/编码/123123/corrected_tex"
    )
'''