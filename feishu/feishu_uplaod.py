import json
import feishu.config as fsconfig
import requests
import os
def upload_file(file_path, parent_node = "ReVffyLIal2KuGdpGRNcZNJ0njd"):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    payload = json.dumps({
    "app_id": fsconfig.app_id,
    "app_secret": fsconfig.app_secret
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    tenant_access_token = response.json()["tenant_access_token"]

    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    # file_path = "d://test//FBA18PLZLJ0Y.zip"
    # 判断文件大小
    file_size = os.stat(file_path).st_size
    headers = {
        "Authorization": f"Bearer {tenant_access_token}"
    }
    files = {
        "file_name": (None, os.path.basename(file_path)),
        "parent_type": (None, "explorer"),
        "parent_node": (None, parent_node), # 文件夹，固定
        "size": (None, file_size),
        "file": (os.path.basename(file_path), open(file_path, "rb"))
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        print("File uploaded successfully:", response.json())
    else:
        print("Failed to upload file:", response.status_code, response.text)
    return response.text
if __name__ == "__main__":
    upload_file("d://test//FBA18PLZLJ0Y.zip")