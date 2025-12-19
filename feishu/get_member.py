
import requests


import json
import config
import os
import time
def is_file_updated_recently(file_path, threshold_hours=1.5):
    try:
        # 获取文件的最后修改时间
        modification_time = os.path.getmtime(file_path)
        # 当前时间
        current_time = time.time()
        # 判断是否超过指定的小时数
        time_difference = current_time - modification_time
        return time_difference <= threshold_hours * 3600
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在！")
        return False
# 如果文件存在，并且更新时间超过一小时，则重新获取token
if is_file_updated_recently("tenant_access_token"):
    with open('tenant_access_token') as f:
        tenant_access_token = f.read().strip()
else:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    payload = json.dumps({
    "app_id": config.app_id,
    "app_secret": config.app_secret
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    tenant_access_token = response.json()["tenant_access_token"]
print(tenant_access_token)
#import pdb;pdb.set_trace()

import requests

headers = {
    'Authorization': 'Bearer u-cRHsz9_UR88aTQV.2rmDo_0526xl45GXOgw01hOa0A9C',
}

params = {
    'page_size': '100',
}

response = requests.get(
    'https://open.feishu.cn/open-apis/im/v1/chats/oc_ac8b83a078b491f9c11b995ff8228a7c/members',
    params=params,
    headers=headers,
)
res_json = response.json()
print(res_json)

import pdb;pdb.set_trace()
pass