import requests
import json
url = "https://api.coze.cn/v3/chat"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer pat_ogp6m0feq3BZviV1yncWdnxk95dACt7REgFCtEnxIYjXBemYWNr1fhokeTooRMme",
}
payload = {
    "bot_id": "7454401268396769280",
    "user_id": "123456789",
    "stream": True,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": '[{"type":"text","text":"这个地毯好漂亮"}]',
            "content_type": "object_string",
        }
    ],
}

response = requests.post(url, json=payload, headers=headers, stream=True)

if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            #print(line.decode("utf-8"))
            try:
                #json.loads(line.decode()[5:])
                content = json.loads(line.decode()[5:])['content']
                if content.find("评论内容") >= 0:
                    print(content)
                    break
            except:
                pass
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
