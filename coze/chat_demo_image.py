import requests
import json
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
    out_put = ""
    for line in response.iter_lines():
        if line:
            try:
                #json.loads(line.decode()[5:])
                content = json.loads(line.decode()[5:])['content']
                #print(content)
                # if content.find("评论内容") >= 0:
                #     print(content)
                #     break
                if content.find("{") >= 0:
                    continue
                if len(out_put) < len(content):
                    out_put = content
            except:
                pass
    for msg in payload['additional_messages']:
        for ct in json.loads(msg['content']):
            if ct['type'] == 'text':
                print(ct['text'])
            if ct['type'] == 'image':
                print(ct['file_url'])
    print(out_put)
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
