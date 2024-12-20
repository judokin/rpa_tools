
import requests

# cli_a7d537a861a1d00e

# WPFHqIYtyVbRRifSA0Hl6f4YMtJzwVoB

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

url = "https://open.feishu.cn/open-apis/bitable/v1/apps/RSf3bhBf4aVyNKsNVpicxZD4nBg/tables/tbl1mILKyyn6fzFK/records/search?page_size=20"
payload = json.dumps({})


headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {tenant_access_token}'
}

response = requests.request("POST", url, headers=headers, data=payload)
res_json = response.json()
for item in res_json['data']['items']:
    if len(item['fields']) == 0:
        continue
    print(item['fields'])
import pdb;pdb.set_trace()
pass