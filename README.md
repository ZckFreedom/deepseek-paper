# deepseek-paper
> 准备条件：
> 电脑安装Python3.10及以上版本，并将python加入环境变量中。
> 如需要论文润色，则需要将latex也加入环境变量中。
> 在命令行使用即可，目前暂不支持额外交互界面。

1、Git下载项目
   ```
    git clone --depth=1 https://github.com/ZckFreedom/deepseek-paper.git
    cd deepseek-paper
   ```
>  也可直接下载zip压缩包。

2、在'config.ini'中填入对应的api-key。目前仅支持Deepseek官方。

>  建议创建‘config_private.ini’文件并在其中填入api-key，这样保证每次项目更新时不需要重新配置

    
3、安装依赖
    ```
    pip install -r requirements.txt
    ```

4、运行
    ```
    python main.py
    ```


5、选择模型及对应功能，Paper功能要求将需要处理的tex文件放到当前目录的paper_ai文件夹内。处理完成后会在paper_ai文件夹内创建diff-out文件夹并存入对比文件diff_tex。

> [!NOTE]
> 1、默认Open-ai SDK格式调用，如果需要其他方式参考api_interface文件。
> 
> 2、使用推理模型时，latexdiff导出文件会有数学符号错误会导致自动编译失败，需要自行在texstudio等软件中检查错误重新编译一遍即可。
>
> 3、在api_interface或api_interface_sdk文件中可以修改build_prompt函数更改要求。


# 2025/6/13更新
1、选择模型删除了出Deepseek官方之外的所有模型选项。

2、Chat功能新增了支持对话内容编译成pdf并查看，所有文件保存在当前目录的chat_content文件夹中，注意及时清理。

3、Paper功能现在支持选择全文润色或者仅修改语法错误，仅修正语法建议选择Deepseek-V3。

4、优化了Code功能文件夹结构。
