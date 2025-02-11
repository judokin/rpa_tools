import json
# import feishu.config as fsconfig
import requests
import os
import datetime
import importlib.util
import pandas as pd
from messange import send
# 指定文件路径
config_file_path = r"D:\rpa_tools\feishu\config.py"

# 加载模块
spec = importlib.util.spec_from_file_location("config", config_file_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

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

def upload_file(file_path):
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
        "file_type": (None, "xls"),

        "parent_node": (None, "MDKzfVTgKlewMPdjgLCcy6NunKJ"), # 文件夹，固定
        "size": (None, file_size),
        "file": (os.path.basename(file_path), open(file_path, "rb"))
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        print("File uploaded successfully:", response.json())
    else:
        print("Failed to upload file:", response.status_code, response.text)
    return response.json()
def import_tasks_by_data(data):
    headers = {
        "Authorization": f"Bearer {tenant_access_token}"
    }
    res = requests.post("https://open.feishu.cn/open-apis/drive/v1/import_tasks", headers=headers, data=json.dumps(data))
    res_json = res.json()
    print(res_json)
    return res_json
def list_files():
    url = 'https://open.feishu.cn/open-apis/drive/v1/files'
    params = {
        'direction': 'DESC',
        'folder_token': 'MDKzfVTgKlewMPdjgLCcy6NunKJ',
        'order_by': 'EditedTime'
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}"
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()
    print(res_json)
    return res_json
def delete_file(file_token, type=''):
    url = f'https://open.feishu.cn/open-apis/drive/v1/files/{file_token}?type={type}'  # 替换 :file_token 为实际的文件标识符
    headers = {
        'Authorization': f"Bearer {tenant_access_token}"
    }

    response = requests.delete(url, headers=headers)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
def clear_tables():
    url = "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/HdwSsEP8thucYCtpoUdcGzk9nid/sheets/query"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    data = response.json() 
    print(data)
    
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HdwSsEP8thucYCtpoUdcGzk9nid/dimension_range"

    data = {
        "dimension": {
            "sheetId": data['data']['sheets'][0]['sheet_id'],
            "majorDimension": "ROWS",
            "startIndex": 2,
            "endIndex": data['data']['sheets'][0]['grid_properties']['row_count']
        }
    }

    response = requests.delete(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    print(response.json())

def insert_tables():
    url = "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/HdwSsEP8thucYCtpoUdcGzk9nid/sheets/query"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    data = response.json() 
    print(data)
    

    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HdwSsEP8thucYCtpoUdcGzk9nid/values_batch_update"
    sheet_id = data['data']['sheets'][0]['sheet_id']
    data = {}
    data['valueRanges'] = []
    df = pd.read_excel(f"./库存_v2.xlsx")
    df = df.fillna('')
    for index, row in df.iterrows():
        #print(index, list(row.values))
        sheet_index = index + 2
        data['valueRanges'].append({
            "range": f"{sheet_id}!A"  + str(sheet_index) + ":J"  + str(sheet_index),
            "values": [list(row.values)]
        })
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    res = response.json()
    print(res)
    # if res['msg'] != 'success':
    #     import pdb;pdb.set_trace()
    #     pass

def run_v1():
    res_json = list_files()
    for item in res_json['data']['files']:
        if item['name'] not in ['库存.xlsx', '库存']:
            continue
        print(item['name'], item['token'])
        if item['name'].find('xlsx') > 0:
            delete_file(item['token'], type='file')
        else:
            delete_file(item['token'], type='sheet')
    #import pdb;pdb.set_trace()
    file_token = upload_file("./库存.xlsx")['data']['file_token']
    data = {
        "file_extension": "xlsx",
        "file_name": "库存",
        "file_token": file_token,
        "point": {
            "mount_key": "MDKzfVTgKlewMPdjgLCcy6NunKJ",
            "mount_type": 1
        },
        "type": "sheet"
    }
    import_tasks_by_data(data)
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send(f"库存表格上传完成, 上传时间为：{datetime_str}")

if __name__ == "__main__":
    clear_tables()
    insert_tables()
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send(f"库存表格上传完成, 上传时间为：{datetime_str}")