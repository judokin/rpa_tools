import requests
import json
import socket

# 获取当前计算机名称
computer_name = socket.gethostname()

print(f"当前计算机名称是: {computer_name}")
# 替换为你的飞书 Webhook URL
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/5fcfee0a-7752-4439-8143-d5e49a9be9bc"

# 发送的消息内容
message = {
    "msg_type": "text",
    "content": {
        "text": f"{computer_name}电脑重启了，请注意查看情况"
    }
}
# 发送请求
response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

# 打印结果
if response.status_code == 200:
    print("消息发送成功")
else:
    print(f"消息发送失败: {response.text}")
