import json
#import config
import requests
import os
import time
import importlib.util

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
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/KP5ubEedLatObjs2EBccwPiEnSf/tables/tblWZWLW24tKmHyM/records/{record_id}"
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

def date_range():
    import datetime
    # 获取当前时间
    now = datetime.datetime.now()
    # 获取当前时间后面10个整点时间
    next_10_hours = [
        (now + datetime.timedelta(hours=i+4)).replace(minute=0, second=0, microsecond=0)
        for i in range(1, 11)
    ]
    # 输出结果
    for dt in next_10_hours:
        print(dt)
    return next_10_hours
def get_table_data():
    # date_ranges = date_range()
    # 查询多维表格数据
    # https://wit0jhu6kvu.feishu.cn/base/FoHwb0vWWavlg3sysDJcJpqwnAe?table=tblPUDb6EqFFI5R2&view=vewnkaFEBe
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/FoHwb0vWWavlg3sysDJcJpqwnAe/tables/tblPUDb6EqFFI5R2/records/search?page_size=999"

    # 定义请求头
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
        "Content-Type": "application/json"
    }

    # 将'YYYY-MM-DD HH:MM:SS'替换为一个实际的日期时间字符串
    # timestamp = int(time.mktime(time.strptime('2025-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    # 定义请求体
    # data = {'fields': {'上传日期': timestamp}}

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
    data_json = get_table_data()
    import pdb;pdb.set_trace()
    pass