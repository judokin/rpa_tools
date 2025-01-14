import json
import importlib.util

# 指定文件路径
config_file_path = r"D:\rpa_tools\feishu\config.py"

# 加载模块
spec = importlib.util.spec_from_file_location("config", config_file_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

import requests
import os
from datetime import datetime
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
payload = json.dumps({
"app_id": config.app_id,
"app_secret": config.app_secret
})
headers = {
'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
# print(response.status_code)
# print(response.text)
tenant_access_token = response.json()["tenant_access_token"]

# 定义请求头
headers = {
  'Authorization': 'Bearer ' + tenant_access_token
}

def reset_fields(data, record_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables/tblux7wXHLPNgroJ/records/{record_id}"
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
if __name__ == '__main__':
    datas = json.loads(open("D:\\rpa_tools\\tiktok\\config.json", "r").read())
    reset_fields(datas['data'], datas['record_id'])