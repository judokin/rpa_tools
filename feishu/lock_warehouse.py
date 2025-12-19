import json
import config
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
print(response.status_code)
print(response.text)
tenant_access_token = response.json()["tenant_access_token"]

# 定义请求头
headers = {
  'Authorization': 'Bearer ' + tenant_access_token
}


def get_table_data():
    # 查询多维表格数据
    # 定义目标URL
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/AMGjbywniabr1Os0phvcKPVenhd/tables/tblWZWLW24tKmHyM/records/search?page_size=1000"
    # https://wit0jhu6kvu.feishu.cn/base/AMGjbywniabr1Os0phvcKPVenhd?table=tbltznhmUZJ4MfyC&view=vewdTsEhbe

    # 定义请求体
    data = {}

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 输出返回的状态码和响应数据
    print("Status Code:", response.status_code)
    response_json = {}
    try:
        response_json = response.json()
        #print("Response JSON:", response_json)
    except ValueError:
        print("Response Text:", response.text)
    return response_json

def insert_table_data(data={"fields":{}}):
    # https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/AMGjbywniabr1Os0phvcKPVenhd/tables/tbltznhmUZJ4MfyC/records"
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())

# 获取群成员列表
def get_group_members(chat_id='oc_6cb224fd44af0f6a41d1e426c5b7c057'):
    params = {
        'page_size': '100',
    }
    response = requests.get(
        f'https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members',
        params=params,
        headers=headers,
    )
    return response.json()

def reset_fields(data, record_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/KP5ubEedLatObjs2EBccwPiEnSf/tables/tbltznhmUZJ4MfyC/records/{record_id}"
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
if __name__ == '__main__':
    insert_table_data()
    import pdb;pdb.set_trace()
    pass