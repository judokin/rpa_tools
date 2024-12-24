import json
import config
import requests
import os
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
payload = json.dumps({
"app_id": config.app_id,
"app_secret": config.app_secret
})
headers = {
'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.status_code)
print(response.text)
tenant_access_token = response.json()["tenant_access_token"]
with open('tenant_access_token', 'w') as f:
    f.write(tenant_access_token)
url = "https://open.feishu.cn/open-apis/drive/explorer/v2/root_folder/meta"
headers = {
    "Authorization": f"Bearer {tenant_access_token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Response data:", response.json())
else:
    print("Failed to fetch data:", response.status_code, response.text)




url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
# headers = {
#     "Content-Type": "multipart/form-data",
#     "Authorization": "Bearer t-g104cobfWR7CS7JQT32Z6KY6A2R7IOOYJ7CT4F7K"
# }
file_path = "d://test//FBA18PLZLJ0Y.zip"

# 判断文件大小
file_size = os.stat(file_path).st_size
files = {
    "file_name": (None, os.path.basename(file_path)),
    "parent_type": (None, "explorer"),
    "parent_node": (None, "ReVffyLIal2KuGdpGRNcZNJ0njd"), # 文件夹，固定
    "size": (None, file_size),
    "file": (os.path.basename(file_path), open(file_path, "rb"))
}

response = requests.post(url, headers=headers, files=files)

if response.status_code == 200:
    print("File uploaded successfully:", response.json())
else:
    print("Failed to upload file:", response.status_code, response.text)