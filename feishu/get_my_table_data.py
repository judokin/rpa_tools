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
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/KP5ubEedLatObjs2EBccwPiEnSf/tables/tblWZWLW24tKmHyM/records/search?page_size=1000"

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

def reset_fields(data, record_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/KP5ubEedLatObjs2EBccwPiEnSf/tables/tblWZWLW24tKmHyM/records/{record_id}"
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
if __name__ == '__main__':
    pass
    response_json = get_table_data()
    acount_dict = {}
    count_dict = {}
    for item in response_json['data']['items']:
        if len(item['fields'].keys()) == 0:
            continue
        if '状态' in item['fields'] and item['fields']['状态'] == '已完成':
            continue
        if '状态' in item['fields'] and item['fields']['状态'] == '进行中':
            data = {
                "fields": {
                    "状态": "已完成",
                    "结束时间(不用写)": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
            #reset_fields(data, item['record_id'])
        if '状态' not in item['fields'] or item['fields']['状态'] == '未处理':
            data = {
                "fields": {
                    "状态": "进行中",
                    "开始时间(不用写)": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
            #reset_fields(data, item['record_id'])
        fields = item['fields']
        fields['record_id'] = item['record_id']
        ac = fields['店铺'].split('-')[0]
        country = fields['店铺'].split('-')[1]
        if ac not in acount_dict:
            acount_dict[ac] = {}
        if country not in acount_dict[ac]:
            acount_dict[ac][country] = []
        acount_dict[ac][country].append(fields)
        if ac+"-"+country not in count_dict:
            count_dict[ac+"-"+country] = 0
        count_dict[ac+"-"+country] += 1
    # 取数量最多的key
    count_dict = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
    max_key = list(count_dict.keys())[0]
    fbacode_list = acount_dict[max_key.split('-')[0]][max_key.split('-')[1]]
    open("d:\\rpa_tools\\rpa_config\\fbacode_list.json", "w", encoding='utf8').write(json.dumps(fbacode_list, ensure_ascii=False))
    json.loads(open("D:\\rpa_tools\\rpa_config\\fbacode_list.json","r", encoding="utf8").read())
    import pdb;pdb.set_trace()
    pass