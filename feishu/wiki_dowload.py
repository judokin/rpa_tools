
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
    print(response.status_code)
    print(response.text)
    tenant_access_token = response.json()["tenant_access_token"]
    with open('tenant_access_token', 'w') as f:
        f.write(tenant_access_token)
print(tenant_access_token)
#import pdb;pdb.set_trace()


headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {tenant_access_token}'
}
# 创建导出任务
url = "https://open.feishu.cn/open-apis/drive/v1/export_tasks"
payload = json.dumps({
	"file_extension": "xlsx",
	"token": "RSf3bhBf4aVyNKsNVpicxZD4nBg",
	"type": "bitable"
})


response = requests.request("POST", url, headers=headers, data=payload)
res_json = response.json()
print("ticket", res_json['data']['ticket'])
# 查看导出任务状态

url = "https://open.feishu.cn/open-apis/drive/v1/export_tasks/" + res_json['data']['ticket'] + "?token=RSf3bhBf4aVyNKsNVpicxZD4nBg"
payload = ''


headers = {
  'Authorization': 'Bearer t-g104ckdrDNHVC56YCNUDOWJ35AAX5ZMNAHC4PEGF'
}
file_token = ""
file_name = ""
for i in range(20):
    time.sleep(1)
    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = response.json()
    try:
        file_token = res_json['data']['result']['file_token']
        file_name = res_json['data']['result']['file_name']
    except:
        #import pdb;pdb.set_trace()
        pass
    if file_token != "":
        break
print(file_token)
# 下载导出结果
url = f"https://open.feishu.cn/open-apis/drive/v1/export_tasks/file/{file_token}/download"
 # 下载文件
response = requests.get(url, headers=headers, stream=True)

if response.status_code == 200:
    # 将文件保存到本地
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_name = f"d://data//{file_name}_{time_str}.xlsx"  # 替换为期望的文件名
    with open(file_name, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # 过滤掉保持活动的空块
                file.write(chunk)
    print(f"文件已成功保存为: {file_name}")
else:
    print(f"下载失败，状态码: {response.status_code}，响应: {response.text}")