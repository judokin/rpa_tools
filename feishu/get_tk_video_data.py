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
        (now + datetime.timedelta(hours=i)).replace(minute=0, second=0, microsecond=0)
        for i in range(1, 11)
    ]
    # 输出结果
    for dt in next_10_hours:
        print(dt)
    return next_10_hours
def get_table_data():
    date_ranges = date_range()
    # 查询多维表格数据
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables/tblux7wXHLPNgroJ/records/search?page_size=999"

    # 定义请求头
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
        "Content-Type": "application/json"
    }

    # 将'YYYY-MM-DD HH:MM:SS'替换为一个实际的日期时间字符串
    # timestamp = int(time.mktime(time.strptime('2025-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    # 定义请求体
    # data = {'fields': {'上传日期': timestamp}}

    data = {"sort": [
        {
        "field_name": "上传日期",
        "desc": True
        }
    ]
    }
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
    newest_day = ''
    break_times = 0
    update_datas_list = []
    for items in data_json['data']['items']:
        date_time = items['fields']['上传日期']
        date_dir = time.strftime("%Y-%m-%d", time.localtime(date_time/1000))
        if newest_day == '':
            newest_day = date_dir
        elif newest_day != date_dir:
            break_times += 1
            if break_times >= 1:
                break
        folder_path = f"d://tk_video//{date_dir}//"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_name = folder_path + items['fields']['视频'][0]['name']
        if not os.path.exists(file_name):
            download_file(file_name, items['fields']['视频'][0]['url'])
        if '能否发布' in items['fields'] and items['fields']['能否发布'] == True:
            continue
        items['datetime'] = str(date_ranges[len(update_datas_list)])
        items['file_name'] = file_name
        print(file_name, items)
        update_datas_list.append(items)
        # 只限10个视频
        if len(update_datas_list) == len(date_ranges):
            break
        #import pdb;pdb.set_trace()
        pass
    open("d:\\tk_video\\update_datas_list.json","w").write(json.dumps(update_datas_list,indent=4).encode().decode("utf8"))
    datas = json.loads(open("d:\\tk_video\\update_datas_list.json","r").read())

if __name__ == "__main__":
    get_table_data()
