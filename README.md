# deepseek-paper
1、下载项目
   ```
    git clone --depth=1 https://github.com/ZckFreedom/deepseek-paper.git
    cd deepseek-paper
   ```

2、在'config.ini'中填入对应的api-key。目前支持Deepseek官方，阿里云百炼，硅基流动(SiliconFlow)，腾讯知识引擎原子能力，超算互联网的api调用。
    ```
    建议创建‘config_private.ini’文件并在其中填入api-key，这样保证每次项目更新时不需要重新配置
    ```
    
3、安装依赖
    ```
    pip install -r requirements.txt
    ```

4、运行
    ```
    python main.py
    ```


5、选择对应模型，使用电脑中的绝对路径输入的tex文件地址，处理完成后会在tex文件地址创建diff-out文件夹并存入对比文件diff_tex。

> [!NOTE]
> 1、默认Open-ai SDK格式调用，如果需要其他方式参考api_interface文件。
> 
> 2、latexdiff导出文件可能有一些符号错误会导致编译失败，需要自行在texstudio中编译一遍找出错误修改即可。
>
> 3、在api_interface或api_interface_sdk文件中可以修改build_promot函数更改要求。
