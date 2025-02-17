# deepseek-paper
在config.ini中填入对应的api-key。

1、安装依赖
    ```
    pip install -r requirements.txt
    ```

2、运行
    ```
    python main.py
    ```


3、选择对应模型，输入本地的tex文件地址，处理完成后会在tex文件地址创建diff-out文件夹并存入对比文件diff_tex。

> [!NOTE]
> latexdiff导出文件可能有一些符号错误会导致编译失败，需要自行在texstudio中编译一遍找出错误修改即可。

> 在api_interface或api_interface_sdk文件中可以修改build_promot函数更改要求。
