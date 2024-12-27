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

# https://wit0jhu6kvu.feishu.cn/wiki/RimPwb9MdiXiakkMVsHcZKcqnzc?base_hp_from=larktab&table=tblux7wXHLPNgroJ&view=vewJIW54qS
# 多维表格数据
url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?obj_type=wiki&token=RimPwb9MdiXiakkMVsHcZKcqnzc"
payload = ''

headers = {
  'Authorization': 'Bearer ' + tenant_access_token
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
print(response.text)
# 查询多维表格数据

# 定义目标URL
url = "https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables/tblux7wXHLPNgroJ/records/search?page_size=20"

# 定义请求头
headers = {
    "Authorization": "Bearer u-d3nx2rlzlat8Y.3UQFv3Togln0bR0kvHqW20llW8a7Md",
    "Content-Type": "application/json"
}

# 定义请求体
data = {'fields': {'上传日期': 1735056000000}}

# 发送 POST 请求
response = requests.post(url, headers=headers, json=data)

# 输出返回的状态码和响应数据
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except ValueError:
    print("Response Text:", response.text)
print("\n\n\n\n\n\n\n")
headers = {
  'Authorization': 'Bearer ' + tenant_access_token
}
url = "https://open.feishu.cn/open-apis/drive/v1/medias/U1FCbmYFNofR5uxtoqmcRlgSnDc/download?extra=%7B%22bitablePerm%22%3A%7B%22tableId%22%3A%22tblux7wXHLPNgroJ%22%2C%22rev%22%3A3%7D%7D"
#response = requests.request("GET", url, headers=headers, data=payload)
response = requests.get(url, headers=headers, stream=True)

if response.status_code == 200:
    import time
    # 将文件保存到本地
    file_name = "test"
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_name = f"d://test//{file_name}_{time_str}.mp4"  # 替换为期望的文件名
    with open(file_name, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # 过滤掉保持活动的空块
                file.write(chunk)
    print(f"文件已成功保存为: {file_name}")
else:
    print(f"下载失败，状态码: {response.status_code}，响应: {response.text}")
print(response.text)
import pdb;pdb.set_trace()
pass
