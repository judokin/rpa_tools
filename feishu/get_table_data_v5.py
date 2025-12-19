import json
#import config
import requests
import os
import time
import importlib.util
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.utils import get_column_letter

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

def download_file_excel(file_name, temp_url):
    headers = {
        'Authorization': 'Bearer ' + tenant_access_token
    }
    response = requests.get(temp_url, headers=headers, stream=True)

    if response.status_code == 200:
        # 确保 Content-Type 是文件类型，而不是 JSON 错误信息
        # Excel 文件的 Content-Type 通常是 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # 但对于 tmp_url 接口，可能只是 'application/octet-stream'
        
        # 成功的下载流程：
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: 
                    file.write(chunk)
        print(f"文件已成功保存为: {file_name}")
    else:
        # 如果不是 200，明确打印出 API 返回的错误内容，有助于排查
        try:
            error_msg = response.json()
        except requests.exceptions.JSONDecodeError:
            error_msg = response.text
            
        print(f"下载失败，状态码: {response.status_code}，响应: {error_msg}")
        
def download_file(file_name, url):
    headers = {
        'Authorization': 'Bearer ' + tenant_access_token
    }
    #url = "https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url?file_tokens=FM5ebnCXJo36FLx9ii4cMrsKn9c&extra=%7B%22bitablePerm%22%3A%7B%22tableId%22%3A%22tblux7wXHLPNgroJ%22%2C%22rev%22%3A3%7D%7D"
    #response = requests.request("GET", url, headers=headers, data=payload)
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        # 将文件保存到本地 
        # file_name = "test"
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉保持活动的空块
                    file.write(chunk)
        print(f"文件已成功保存为: {file_name}")
    else:
        print(f"下载失败，状态码: {response.status_code}，响应: {response.text}")

def reset_fields(data, record_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/D53CbpqTwaQdUxsjIgqckk43nOb/tables/tblKnzLNWu488kpA/records/{record_id}"
    
    # 定义请求头
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

def get_table_data():
    import datetime
    # https://wit0jhu6kvu.feishu.cn/base/CUgObJq4aas1busUW5HcU4scnSd?table=tblcscrczF5v3pCm&view=vewA4pwieU
    # 查询多维表格数据
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/CUgObJq4aas1busUW5HcU4scnSd/tables/tblcscrczF5v3pCm/records/search?page_size=999"

    # 定义请求头
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
        "Content-Type": "application/json"
    }

    data = {}
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 输出返回的状态码和响应数据
    print("Status Code:", response.status_code)
    data_json = {}
    try:
        data_json = response.json()
        print("Response JSON:", response.json())
    except ValueError:
        pass
        print("Response Text:", response.text)
    #datas = []
    for items in data_json['data']['items']:
        if len(items['fields']) == 0:
            continue
        file_tmp_name = '船期'
        if "状态" in items['fields'] and items['fields']['状态'] not in ['未处理', '进行中']:
            print("状态 =", items['fields']['状态'])
            continue
        if "船期" in items['fields']:
            print(items['fields']['船期'][0]['text'])
            file_tmp_name += items['fields']['船期'][0]['text']+"-"
        if "人员" in items['fields']:
            print(items['fields']['人员'][0]['name'])
            file_tmp_name += items['fields']['人员'][0]['name']+"_"
        file_tmp_name += items['fields']['店铺'] + ".xlsx"
        file_name = r'D:\data\walmart_sku_excel' + '\\' + file_tmp_name
        download_file_excel(file_name, items['fields']['附件'][0]["url"])
        print(items)
        break


if __name__ == "__main__":
    get_table_data()
