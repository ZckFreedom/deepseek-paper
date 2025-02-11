import configparser


def check_spark_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    required = ['APP_ID', 'API_KEY', 'API_SECRET']
    for model in ['spark-v4', 'spark-max']:
        if not config.has_section(model):
            print(f"❌ 缺失配置段: [{model}]")
            continue

        missing = [key for key in required if not config[model].get(key)]
        if missing:
            print(f"❌ [{model}] 缺少参数: {missing}")
        else:
            print(f"✅ [{model}] 配置完整")


if __name__ == "__main__":
    check_spark_config()