import requests
import json

def send_message(message, webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/1b314b2d-d723-4ee7-ab06-fe8d26943f38"):
    # 发送的消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    # 发送请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 打印结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")