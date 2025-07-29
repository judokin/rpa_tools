import configparser
from openai import OpenAI

# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取INI文件
config.read('config.ini')

# 获取API Key
api_key = config['DEFAULT']['api_key']

# 初始化DeepSeek客户端
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 定义消息
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]

# 发送请求
try:
    response = client.chat.completions.create(
        model="deepseek-reasoner",  # 使用DeepSeek的模型名称
        messages=messages
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")