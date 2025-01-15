import requests
import json
import datetime
import pandas as pd
from messange import send
base_url = "http://122.224.27.106:5190"
res = requests.get(base_url + "/luyao/gettoken?id=luyao&code=d0d4e4f9870fb6b476e3d0f4e68f076a")
res_json = res.json()
TOKEN = res_json['data']['token']
print(TOKEN)

# 飞书部分
import importlib.util
# 指定文件路径
config_file_path = r"D:\rpa_tools\feishu\tat.py"
# 加载模块
spec = importlib.util.spec_from_file_location("tat", config_file_path)
tat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tat)
tenant_access_token = tat.tenant_access_token
print(tenant_access_token)
# 定义请求头
headers = {
    "Authorization": "Bearer " + tenant_access_token,
    "Content-Type": "application/json"
}

def post_info_by_data(data, type="getstock"):
    res = requests.post(base_url + f"/luyao/{type}?token={TOKEN}", data=json.dumps(data))
    res_json = res.json()
    return res_json

def add_fields(datas):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/Q6AnbNQkuaiSwYsV6tycPLajny6/tables/tblaBNQLTbsFbLrp/records/batch_create"
    response = requests.post(url, headers=headers, json=datas)
    print(response.status_code)
    print(response.json())

def delete_all_fields(datas):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/Q6AnbNQkuaiSwYsV6tycPLajny6/tables/tblaBNQLTbsFbLrp/records/batch_delete"
    response = requests.post(url, headers=headers, json=datas)
    print(response.status_code)
    print(response.json())
def get_table_data():
    # 查询多维表格数据
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/Q6AnbNQkuaiSwYsV6tycPLajny6/tables/tblaBNQLTbsFbLrp/records/search?page_size=10000"
    data = {}
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 输出返回的状态码和响应数据
    print("Status Code:", response.status_code)
    data_json = {}
    try:
        data_json = response.json()
        #print("Response JSON:", response.json())
    except ValueError:
        pass
        #print("Response Text:", response.text)
    return data_json

if __name__ == "__main__":
    data = {}
    res_json = post_info_by_data(data)
    df = pd.DataFrame(res_json["data"])
    df_filtered = df[df["更新时间"].notna()]
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
    df_filtered.to_excel(f"./库存_{datetime_str}.xlsx", index=False)
    df_filtered.to_excel(f"./库存.xlsx", index=False)
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send(f"库存更新完成, 更新时间为：{datetime_str}")
    # while True:
    #     res_json = get_table_data()
    #     #要删除的数据
    #     delete_datas = {
    #         "records": []
    #     }
    #     for item in res_json["data"]["items"]:
    #         print(item["record_id"])
    #         delete_datas['records'].append(item["record_id"])
    #     if len(delete_datas['records']) == 0:
    #         print('开始删除完成')
    #         break
    #     elif len(delete_datas['records']) > 0:
    #         print('开始删除,数据量为：', len(delete_datas['records']))
    #     delete_all_fields(delete_datas)
    # datas = {
    #     "records": [
    #         # {
    #         #     "fields": {
    #         #         "PID": "文本内容2"
    #         #     }
    #         # },
    #         #             {
    #         #     "fields": {
    #         #         "PID": "文本内容3"
    #         #     }
    #         # }
    #     ]
    # }
    # df_filtered['录入时间'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # for index, row in df_filtered.iterrows():
    #     fields = {}
    #     for col in df_filtered.columns:
    #         if isinstance(row[col], str):
    #             fields[col] = row[col].replace("\n", "").strip()
    #         else:
    #             fields[col] = row[col]
    #     datas['records'].append({'fields': fields})
    # add_fields(datas)