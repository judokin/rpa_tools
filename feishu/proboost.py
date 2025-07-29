import json
#import config
import requests
import os
import time
import importlib.util
import pandas as pd

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
    headers = {
        'Authorization': 'Bearer ' + tenant_access_token
    }
    # https://wit0jhu6kvu.feishu.cn/wiki/RimPwb9MdiXiakkMVsHcZKcqnzc?table=tblux7wXHLPNgroJ&view=vewJIW54qS
    # url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/RimPwb9MdiXiakkMVsHcZKcqnzc/tables/tblux7wXHLPNgroJ/records/{record_id}"
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables/tblux7wXHLPNgroJ/records/{record_id}"
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

def add_fields(data):
    headers = {
        'Authorization': 'Bearer ' + tenant_access_token
    }
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/CqTzbZpM6a3k0ZszsEbcqWKPn6f/tables/tblkKMD0P1b1RZCP/records/batch_create"
    response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
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
def get_link_data():
    local_folder = "D:\\tiktok_log\\tk_link\\"
    file_list = sorted(os.listdir(local_folder))
    datas = json.loads(open(local_folder + file_list[-1],"r").read())
    return datas
def get_table_data():
    # date_ranges = date_range()
    # 查询多维表格数据
    # url = "https://open.feishu.cn/open-apis/bitable/v1/apps/NZk0b8qpPaHCAgsslNscShbpnsg/tables/tblux7wXHLPNgroJ/records/search?page_size=9999"
    # "https://wit0jhu6kvu.feishu.cn/base/CqTzbZpM6a3k0ZszsEbcqWKPn6f?table=tblkKMD0P1b1RZCP&view=vewMJxfRJB"
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/CqTzbZpM6a3k0ZszsEbcqWKPn6f/tables/tblkKMD0P1b1RZCP/records/search?page_size=9999"

    # 定义请求头
    headers = {
        "Authorization": "Bearer " + tenant_access_token,
        "Content-Type": "application/json"
    }

    # 将'YYYY-MM-DD HH:MM:SS'替换为一个实际的日期时间字符串
    # timestamp = int(time.mktime(time.strptime('2025-01-03 00:00:00', '%Y-%m-%d %H:%M:%S'))) * 1000
    # 定义请求体
    # data = {'fields': {'上传日期': timestamp}}

    # data = {"sort": [
    #     {
    #     "field_name": "上传日期",
    #     "desc": True
    #     }
    # ] 
    # }
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
    #update_datas_list = []
    #link_datas = get_link_data()
    links = []
    for items in data_json['data']['items']:
        links.append(items['fields']['链接'][0]['text'])

    excel_datas = pd.read_excel(r"D:\proboost\filtered_data.xlsx")
    add_data = {"records": []}
    for i in range(len(excel_datas)):
        item = excel_datas.iloc[i]
        if item['商品链接'] in links:
            continue
        if 'nan' == str(item['区域分类']):
            item['区域分类'] = ''
        add_data['records'].append({"fields": {
            "GMV5万美金以上的款（品牌名称）": item["店铺名称"],
            "区域分类": item["区域分类"],
            "商品名称": item["商品名称"],
            "白底图或场景图": item["商品缩略图"],
            "链接": item["商品链接"]
        }})
    if len(add_data['records']) > 0:
        add_fields(add_data)
    pass
    '''
    {
        "records": [
            {
                "fields": {
                    "PID": "文本内容2"
                }
            }
        ]
    }
    '''
    add_data = {
        "records": [
        {
        "fields": {
            "GMV5万美金以上的款（品牌名称）": "店铺名称",
            "区域分类": "区域分类",
            "商品名称": "商品名称",
            "白底图或场景图": "商品缩略图",
            "链接": "商品链接"
        }},
        {
        "fields": {
            "GMV5万美金以上的款（品牌名称）": "店铺名称",
            "区域分类": "区域分类",
            "商品名称": "商品名称",
            "白底图或场景图": "商品缩略图",
            "链接": "商品链接"
        }}
    ]
    }
    import pdb;pdb.set_trace()
    add_fields(add_data)
    pass
    #     if '备注' not in items['fields']:
    #         continue
    #     date_time = items['fields']['上传日期']
    #     date_dir = time.strftime("%Y-%m-%d", time.localtime(date_time/1000))
    #     folder_path = f"d://tk_video//{date_dir}//"
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)
    #     file_name = folder_path + items['fields']['视频'][0]['name']
    #     # items['datetime'] = str(date_ranges[len(update_datas_list)])
    #     items['file_name'] = file_name
    #     #print(file_name, items)
    #     update_datas_list.append(items)
    # for index, link_item in enumerate(link_datas):
    #     for items in update_datas_list:
    #         # 正则提取英文数字
    #         import re
    #         pattern = r'\b\w+\b'
    #         fields_text = items['fields']['备注'][0]['text'].split('#')[0]
    #         link_item_text = link_item[2].split('#')[0]
    #         if "".join(re.findall(pattern, fields_text)) == "".join(re.findall(pattern, link_item_text)):
    #             # 格式为https://www.tiktok.com/@haleykgubler/video/7461931972605021471
    #             link_url = f"""https://www.tiktok.com/{link_item[3].split("/")[-1]}/video/{link_item[1].split("/")[5]}"""
    #             print("index=", index, "相等,拼接URL", link_url)
    #             reset_fields({"fields": {"视频编码": link_url}}, items['record_id'])
    #             break
    #         # else:
    #         #     if items['fields']['备注'][0]['text'].find(link_item[2].split(',')[0]) >= 0:
    #         #         print("index=", index, "不相等")
    #         #         import pdb;pdb.set_trace()
    #         #         pass
    #     #break
    # #import pdb;pdb.set_trace()
    # # pass
    # # open("d:\\tk_video\\tk_link_to_update.json","w").write(json.dumps(update_datas_list,indent=4).encode().decode("utf8"))
    # # datas = json.loads(open("d:\\tk_video\\tk_link_to_update.json","r").read())

if __name__ == "__main__":
    get_table_data()
