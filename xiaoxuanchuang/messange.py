def send(text):
    import requests
    import json
    # 替换为你的飞书 Webhook URL
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/c6418617-4971-41b2-a00f-60b27e72007f"

    # 发送的消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    # 发送请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 打印结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")
