
import requests


import json
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

payload = json.dumps({
  "app_id": "",
  "app_secret": ""
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)



# url = "https://open.feishu.cn/open-apis/auth/v3/user_access_token/internal/"

# payload = json.dumps({
#   "app_id": "cli_a7d537a861a1d00e",
#   "app_secret": "WPFHqIYtyVbRRifSA0Hl6f4YMtJzwVoB"
# })
# headers = {
#   'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)
# print(response.text)
# import pdb;pdb.set_trace()
# import pdb;pdb.set_trace()
tenant_access_token = response.json()["tenant_access_token"]


url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?obj_type=wiki&token=RimPwb9MdiXiakkMVsHcZKcqnzc"
payload = ''

headers = {
  'Authorization': 'Bearer ' + tenant_access_token
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
print(response.text)
# import pdb;pdb.set_trace()




# url = "https://open.feishu.cn/open-apis/bitable/v1/apps/" + res_json['data']['node']['obj_token'] + "/tables?page_size=20"
# payload = ''


# headers = {
#   'Authorization': 'Bearer ' + tenant_access_token
# }

# response = requests.request("GET", url, headers=headers, data=payload)
# print(response.text)
# import pdb;pdb.set_trace()
# pass



url = "https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables"


url = "https://open.feishu.cn/open-apis/bitable/v1/apps/" + res_json['data']['node']['obj_token'] + "/tables"
params = {
    "page_size": 20
}

response = requests.get(url, headers=headers, params=params)
print("Status Code:", response.status_code)
print("Response Body:", response.json())
# url = "https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables"
headers = {
    "Authorization": "Bearer u-fSQxDQ3ht62FkA4X2JFceDglla1l0kZFNq2004.8a6N9"
}
print(headers)
print(tenant_access_token)
params = {
    "page_size": 20
}

response = requests.get(url, headers=headers, params=params)

# 输出响应状态码和内容
print("Status Code:", response.status_code)
print("Response Body:", response.json())