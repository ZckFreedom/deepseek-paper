# deepseek-paper

命令行工具，用大语言模型辅助论文润色、对话和代码编写。所有模型统一通过 OpenAI 兼容 SDK 调用。

## 准备条件

- Python 3.10+，并加入环境变量。
- 论文 diff / 对话转 PDF 功能需要 LaTeX：`pdflatex`、`latexdiff`，中文对话还需 `xelatex` + `ctex`；均需加入环境变量。
- 目前只提供命令行交互，无图形界面。

## 安装

```bash
git clone --depth=1 https://github.com/ZckFreedom/deepseek-paper.git
cd deepseek-paper
pip install -r requirements.txt
python main.py
```

## 内置模型

启动时先选模型，再选功能。模型配置在 `config.ini`；建议把 API Key 填入 `config_private.ini`，优先级更高，且项目更新时不会被覆盖。

| 菜单 | 配置节 | 模型 ID | 服务方 |
|---|---|---|---|
| 1 | `deepseek-v4-pro` | `deepseek-v4-pro` | DeepSeek 官方 |
| 2 | `deepseek-v4-flash` | `deepseek-flash` | DeepSeek 官方 |
| 3 | `gpt-sol` | `gpt-6.1-sol` | OpenAI 兼容中转 |
| 4 | `gpt-astra` | `gpt-6-astra` | OpenAI 兼容中转 |
| 5 | `claude-opus` | `claude-opus-5.5` | OpenAI 兼容中转 |
| 6 | `kimi` | `kimi-k2-thinking` | Kimi（Moonshot）官方 |

说明：

- GPT / Claude 走 `tokenspark.uno/v1`，沿用中转平台提供的 Key。
- Kimi 走 `https://api.moonshot.cn/v1`，需要在 `config_private.ini` 的 `[kimi]` 中填入自己的 Moonshot API Key；模型 ID 可按账号可用模型修改。
- 其他 OpenAI 兼容服务：复制一个配置节，改 `MODEL` / `BASE_URL_OPENAI` / `API_KEY`，并在 `main.py` 的 `MODEL_MAP` 中加一项即可。

## 功能

运行 `python main.py`，选择功能：

1. **修改并润色论文** — 把待处理 `.tex` 放到 `paper_ai/`。可选「全文英文润色」或「仅修正英语语法错误」。结果存 `paper_ai/corrected_tex/`，差异对比存 `paper_ai/diff_output/`（含 `diff_result.tex` / `.pdf`）。
2. **对话** — 流式输出，区分【推理过程】和【回答】；`清空` 清历史、`重置` 改角色设定、`pdf` 把对话编译成 PDF。文件存 `chat_content/`。
3. **代码** — Python / SageMath / Magma 的代码生成、加注释、优化，以及 SageMath → Magma 转换。文件存 `codes/{python,sagemath,magma}/`。

提示词在 `api_interface_sdk.py`（论文）和各功能主文件中，可直接改 `build_prompt_*` 调整要求。旧版原生 HTTP 调用见 `api_interface.py`，当前主流程不使用。

## TeX 分块逻辑

`split_tex.py` 按 LaTeX 顶层章节切分正文：

- 以 `\chapter{...}` / `\section{...}` 为边界，**每个章节一个块**；`\subsection` 仍留在所属章节内。
- 摘要到首个章节之间的内容（含摘要）单独成块；导言区和参考文献不送模型处理。
- 兼容 `\section*`、`\section[短标题]{...}`、注释掉的 `\section`（不作为边界），参考文献同时支持 `\begin{thebibliography}` 和 `\bibliography{...}`。
- 不再使用早年的 4K/8K 字符上限切分。当前模型上下文普遍达到 1M 级别，按章节切分既保留语义完整性，也便于逐章核对。
- 合并时按 `part` 编号升序拼回，与原文件结构一致。

## 本次更新（2026-11-23）

- **分块改为按章节**：移除 `split_by_character_limit_with_protection` 的 4092 字符上限，新增 `split_by_section`，每章一块；数学公式、表格、图片环境不会被切断。
- **修复参考文献识别**：同时支持 `thebibliography` 环境与 `\bibliography` 命令，取先出现者作为正文结尾。
- **新增 Kimi**：菜单第 6 项，模型 `kimi-k2-thinking`，配置指向 Moonshot 官方 OpenAI 兼容接口。
- **模型菜单同步**：DeepSeek V4 Pro / Flash、GPT-sol / GPT-astra、Claude-Opus、Kimi 共 6 项，配置文件与菜单一一对应。
- **README 重写**：补充模型表、配置说明、分块规则和本次变更。

## 注意事项

1. 使用推理模型时，`latexdiff --math-markup=3` 可能引入数学符号问题导致自动编译失败，需在 TeXstudio 等工具中检查后手动重编译。
2. `chat_content/` 里的对话 PDF 会不断累积，记得定期清理。
3. `config_private.ini` 含 API Key，已加入 `.gitignore`，不要提交或分享。
