import os
import datetime
import pandas as pd
# 定义默认前缀
DEFAULT_PREFIX = "SK-"
# 默认告警时间
DEFAULT_WARN_TIME = 12

def read_excel(filepath):
    df = pd.read_excel(filepath)
    print(filepath, os.path.exists(filepath), len(df))
    df['账号'] = filepath.split("/")[0]
    filter_df = pd.DataFrame()
    for i in range(len(df)):
        if df.loc[i][3].replace("-", "").isdigit():
            continue
        # 追加元素到filter_df
        filter_df = filter_df._append(df.loc[i], ignore_index=True)
    return filter_df
def format_date(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y/%m/%d')
        return date_obj
    except ValueError:
        return None
def run():
    # 前一天的时间
    dattetime_str = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
    # 当天的时间
    dattetime_str = (datetime.datetime.now()-datetime.timedelta(days=0)).strftime("%Y%m%d")
    filter_dfs = pd.DataFrame()
    for folder_name in os.listdir("./"):
        if folder_name.find("亚马逊-") == -1: continue
        #print(folder_name + "/" + dattetime_str+".xlsx")
        filter_df = read_excel(folder_name + "/" + dattetime_str+".xlsx")
        filter_dfs = filter_dfs._append(filter_df, ignore_index=True)
    #重置filter_dfs的索引 1重置为日期，2重置为时间，3重置为订单号
    filter_dfs.rename(columns={0:"每页位置", 1:"日期",2:"时间",3:"订单号", 4:"订单状态"}, inplace=True)
    # 转换时间字符串为datetime类型
    filter_dfs['日期时间'] = filter_dfs['日期'] + ' ' + filter_dfs['时间'].str.replace(' PST', '')
    filter_dfs['日期时间'] = filter_dfs['日期时间'].str.replace(' PDT', '')
    try:
        filter_dfs['日期时间'] = pd.to_datetime(filter_dfs['日期时间'])
    except:
        pass
    # 筛选出日期时间为十一天后的数据
    refilter_dfs = filter_dfs[
        (filter_dfs['日期时间'] <= (datetime.datetime.now()-datetime.timedelta(days=DEFAULT_WARN_TIME))) &
        (filter_dfs['订单号'].str.find(DEFAULT_PREFIX) == 0)
        ]
    #按账号来分组
    message_text = "(官网数据)"
    
    for name, group in refilter_dfs.groupby(['账号']):
        message_text += f"{name[0]}店铺有{len(group)}个订单需要解锁，请及时处理！\n"
        shop_name = name[0].split("亚马逊-")[1].replace("-", "").split("（")[0]
        excel_file_name = f"./{shop_name}要解锁订单号汇总_" + dattetime_str + ".xlsx"
        group.to_excel(excel_file_name, index=False)
        upload_file(excel_file_name)
        #upload_order_id(shop_name, refilter_dfs)
    if len(refilter_dfs.groupby(['账号'])) > 0:
        print(message_text)
        send_message(message_text)
    else:
        message_text = "(官网数据) 目前0单要解锁"
        print(message_text)
        send_message(message_text)


def send_message(message, webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/e49f7f96-12a2-494e-b724-56b0de221f84"):
    import requests
    import json
    # 发送的消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    # 发送请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 打印结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")

def upload_file(file_path):
    import json
    # 指定文件路径
    config_file_path = r"D:\rpa_tools\feishu\config.py"

    # 加载模块
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_file_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
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
        "parent_node": (None, "BtPpfCshYlMwoJdER0Ec2ayWnHe"), # 文件夹，固定
        "size": (None, file_size),
        "file": (os.path.basename(file_path), open(file_path, "rb"))
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        print("File uploaded successfully:", response.json())
    else:
        print("Failed to upload file:", response.status_code, response.text)
    return response.text
if __name__ == "__main__":
    run()
    #os.system("python read_orders.py")