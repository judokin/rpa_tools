import requests

url = "https://api.coze.cn/v3/chat"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer pat_ogp6m0feq3BZviV1yncWdnxk95dACt7REgFCtEnxIYjXBemYWNr1fhokeTooRMme",
}
payload = {
    "bot_id": "7453287258314784818",
    "user_id": "123456789",
    "stream": True,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": '[{"type":"image","file_url":"https://m.media-amazon.com/images/I/81yhL1cX04L._AC_SY450_.jpg"},{"type":"text","text":"帮我看看这张图片中地毯的风格是，并具体描述一下。"}]',
            "content_type": "object_string",
        }
    ],
}

response = requests.post(url, json=payload, headers=headers, stream=True)

if response.status_code == 200:
    print("Streamed response:")
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
