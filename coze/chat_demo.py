import json
import requests
import os
tenant_access_token = "pat_ogp6m0feq3BZviV1yncWdnxk95dACt7REgFCtEnxIYjXBemYWNr1fhokeTooRMme"
url = " https://api.coze.cn/v3/chat"
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {tenant_access_token}'
}
payload = {
    "bot_id": "7453287258314784818",
    "user_id": "123456789",
    "stream": True,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": '[{"type":"image","file_url":"https://m.media-amazon.com/images/I/81yhL1cX04L._AC_SY450_.jpg"},{"type":"text","text":"帮我看看这张图片里都有什么"}]',
            "content_type": "object_string"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)
res_json = response.json()

url = "https://api.coze.cn/v3/chat/retrieve"
payload = {
    "conversation_id": res_json['data']['conversation_id'],
    "chat_id": "7453313107520421940"
}
response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)
import pdb;pdb.set_trace()
pass
'''
payload = json.dumps({
    "conversation_id":"7453308734677467172",
    "bot_id": "7453287258314784818",
    "user_id": "1",
    "stream": False,
    "additional_messages": [{
            "role": "user",
            "content": "提取这个图片的特征，https://m.media-amazon.com/images/I/81yhL1cX04L._AC_SY450_.jpg",
            "content_type": "text"
        }]
})

response = requests.request("POST", url, headers=headers, data=payload)
print(response.status_code)
print(response.text)
import pdb;pdb.set_trace()
pass
'''