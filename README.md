# deepseek-paper
1、下载项目
   ```
    git clone --depth=1 https://github.com/ZckFreedom/deepseek-paper.git
    cd deepseek-paper
    ```

2、在'config.ini'中填入对应的api-key。

3、安装依赖
    ```
    pip install -r requirements.txt
    ```

4、运行
    ```
    python main.py
    ```


5、选择对应模型，输入本地的tex文件地址，处理完成后会在tex文件地址创建diff-out文件夹并存入对比文件diff_tex。

> [!NOTE]
> 建议选择Open-ai SDK调用。
> 
> latexdiff导出文件可能有一些符号错误会导致编译失败，需要自行在texstudio中编译一遍找出错误修改即可。
> 
> 在api_interface或api_interface_sdk文件中可以修改build_promot函数更改要求。
