import requests
import configparser
import time
import datetime
import copy
import pandas as pd

import logging
import os
APP_SECRET = "ysy0Gtn1pDRdQTGshcl1fA=="
APP_ID = "ak_rhvvA99g8tNpb"
# 创建logs文件夹（如果不存在）
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# 设置日志文件路径
log_file = os.path.join(log_folder, 'app.log')
# 配置日志记录器
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file,  # 设置日志文件路径
                    filemode='a')  # 追加模式，如果文件不存在则创建

# 获取一个名为'logger'的日志记录器
logger = logging.getLogger('logger')

# 创建ConfigParser对象
config = configparser.ConfigParser()
pre_day = 11
# 读取INI文件
config.read('config.ini')
def get_access_token():
    # 定义请求的URL
    url = 'https://openapi.lingxing.com/api/auth-server/oauth/access-token'

    # 准备表单数据
    data = {
        'appSecret': APP_SECRET,
        'appId': APP_ID
    }

    # 发送POST请求
    response = requests.post(url, data=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容（假设响应是JSON格式）
        access_token_info = response.json()
        #print("Access Token Info:", access_token_info)
        return access_token_info
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response content:", response.text)


def generate_sign(params, access_token, timestamp, app_id):
    import hashlib
    import urllib.parse
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    import base64
    """
    生成签名并进行AES加密和URL编码。

    :param params: dict, 业务请求参数
    :param access_token: str, 访问令牌G
    :param timestamp: str, 时间戳
    :param app_id: str, 应用ID，用作AES加密密钥
    :return: dict, 包含生成的签名和编码后的签名
    """
    # 添加固定参数
    params.update({
        'access_token': access_token,
        'app_key': app_id,
        'timestamp': timestamp
    })
    # 按照key的ASCII排序
    sorted_params = sorted(params.items(), key=lambda item: item)

    # 拼接参数，忽略值为空的参数
    param_str = '&'.join([f"{k}={v}" for k, v in sorted_params if v not in [None, '']])
    param_str = param_str.replace(" ", "")
    param_str = param_str.replace("'", '"')
    print("param_str =", param_str)
    # 生成MD5签名并转换为大写
    md5_hash = hashlib.md5(param_str.encode('utf-8')).hexdigest().upper()

    # AES加密配置
    key = app_id.encode('utf-8')  # AES密钥需要为bytes
    cipher = AES.new(key, AES.MODE_ECB)

    # 加密MD5值，填充PKCS5
    encrypted = cipher.encrypt(pad(md5_hash.encode('utf-8'), AES.block_size))

    # 将加密后的字节转为Base64编码字符串
    encrypted_sign = base64.b64encode(encrypted).decode('utf-8')

    # URL编码签名
    url_encoded_sign = urllib.parse.quote(encrypted_sign)

    return {
        'sign': md5_hash,
        'encrypted_sign': url_encoded_sign
    }

# get 请求 https://openapi.lingxing.com/erp/sc/data/seller/lists
def get_seller_list():
    import time
    access_token = get_access_token()
    # params, access_token, app_key, timestamp, app_id
    params = {}
    # appSecret
    access_token = access_token['data']['access_token']
    timestamp = str(int(time.time()))
    app_id = APP_ID
    sign = generate_sign(params, access_token, timestamp, app_id)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    url = 'https://openapi.lingxing.com/erp/sc/data/seller/lists?' + ext_url
    response = requests.get(url)
    resp = response.json()
    count = 1
    shops = []
    for i,d in enumerate(resp['data']):
        if d['country'] != '美国':
            continue
        shops.append(d)
        count += 1
    return shops

def order_list_by_shop(sid):
    access_token = get_access_token()
    start_date = (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # import pdb;pdb.set_trace()
    start_date = "2025-03-2"
    end_date = "2025-03-07"
    params = {
            "sid":int(sid),
            "sort_desc_by_date_type": 1,
            "length": 5000,
            "fulfillment_channel": 1,
            "start_date": start_date,
            "end_date": end_date
            }
    print(params)
    # appSecret
    headers = {
        'Content-Type': 'application/json'
    }
    access_token = access_token['data']['access_token']
    timestamp = str(int(time.time()))
    app_id = APP_ID
    sign = generate_sign(params, access_token, timestamp, app_id)
    #print(sign)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    url = 'https://openapi.lingxing.com/erp/sc/data/mws/orders?' + ext_url
    print(url)
    print(headers)
    headers = {}
    response = requests.post(
        url,
        headers=headers,
        json=params,
    )
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容（假设响应是JSON格式）
        res = response.json()
        print("", res)
        return res 
    else:
        print("Response content:", response.text)

def most_order_list_by_shop(sid, offset=0, length=20):
    
    start_date = (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # params = {
    #         "sids":[int(sid)],
    #         "length": length,
    #         "offset": offset * length,
    #         "start_date": start_date,
    #         "end_date": end_date
    #         }
    sid = 271 
    msku = 'KR1006-Brick-17X47-17X30'
    standard_price =  29.99
    sale_price =  20
    asin = 'B0DT5DZH7Y'
    params = {"pricing_params":[{
             "sid": sid,
             "msku": msku,
             "standard_price": standard_price,
             "sale_price": sale_price,
            "start_date": "2025-11-10", # Optional, add if needed
            "end_date": "2035-11-13",   # Optional, add if needed
             "asin": asin # Including ASIN as per the interpretation of the prompt
            }]}
    #params = {}
    headers = {
        'Content-Type': 'application/json'
    }
    access_token = get_access_token()
    access_token = access_token['data']['access_token']
    timestamp = str(int(time.time()))
    app_id = APP_ID
    #
    import json
    print("params =", json.dumps(params))
    sign = generate_sign(params, access_token, timestamp, app_id)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    api_url = "https://openapi.lingxing.com/erp/sc/listing/ProductPricing/pricingSubmit"
    #url = 'https://openapi.lingxing.com/order/amzod/api/orderList?' + ext_url
    url = api_url + '?' + ext_url
    print(url)
    headers = {}
    import json
    for try_time in range(10):
        if try_time > 0:
            time.sleep(5)
            print("刚刚请求失败了，重试中~~~", try_time)
        try:
            response = requests.post(
                url,
                headers=headers,
                json=params,
                timeout=30
            )
            # 检查响应状态码
            res = response.json()
            print(res)
            import pdb;pdb.set_trace()
            if response.status_code == 200:
                # 解析响应内容（假设响应是JSON格式）
                res = response.json()
                return res
            else:
                print("Response content:", response.text)
            break
        except Exception as e:
            print(e)
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
def cancelOrder(sid, seller_fulfillment_order_id):
    access_token = get_access_token()
    params = {
            "sid":int(sid),
            "seller_fulfillment_order_id": seller_fulfillment_order_id
            }
    headers = {
        'Content-Type': 'application/json'
    }
    access_token = access_token['data']['access_token']
    timestamp = str(int(time.time()))
    app_id = config['DEFAULT']['appId']
    sign = generate_sign(params, access_token, timestamp, app_id)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    url = 'https://openapi.lingxing.com/order/amzod/api/cancelOrder?' + ext_url
    headers = {}
    for try_time in range(5):
        if try_time > 0:
            time.sleep(1)
            print("刚刚请求失败了，重试中~~~", try_time)
        try:
            response = requests.post(
                url,
                headers=headers,
                json=params,
                timeout=30
            )
            # 检查响应状态码
            if response.status_code == 200:
                # 解析响应内容（假设响应是JSON格式）
                res = response.json()
                return res
            else:
                print("Response content:", response.text)
            break
        except Exception as e:
            print(e)
def del_orderby(sid, seller_fulfillment_order_ids):
    for seller_fulfillment_order_id in seller_fulfillment_order_ids:
        res = cancelOrder(sid, seller_fulfillment_order_id)
        print("取消订单~~~", seller_fulfillment_order_id)
        if res['code'] == 0:
            logger.info(f"取消订单~~~{seller_fulfillment_order_id} 店铺sid {sid} 状态: {res['code']} {str(res['message'])}")
        else:
            logger.info(f"取消订单~~~{seller_fulfillment_order_id} 店铺sid {sid} 状态: {res['code']} {str(res['error_details'])}")
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
    "app_id": APP_ID,
    "app_secret": APP_SECRET
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
def run():
    #get_access_token()
    shops = get_seller_list()
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
    message_text = ""
    for s in shops:
        offset = 0
        length = 1000
        records = []
        while True:
            orders = most_order_list_by_shop(s['sid'], offset, length)
            if len(orders['data']['records']) == 0:
                break
            offset += 1
            orders_copy = copy.deepcopy(orders)
            records += orders_copy['data']['records']
        sk_record = [record for record in records if record['seller_fulfillment_order_id'].find('SK-') == 0 and record['order_status'] == 'Received']
        filter_record = [record for record in records if record['seller_fulfillment_order_id'].find('SK-') == 0 and record['purchase_date_local'] < (datetime.datetime.now() - datetime.timedelta(days=pre_day)).strftime("%Y-%m-%d") and record['order_status'] == 'Received']
        ext_str = "\n"
        if len(filter_record) > 0:
            ext_str = "已用领星接口自动取消\n"
        message_text += datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  + f" {s['name']:>15} 的锁仓订单量为 {len(sk_record):>5}, 需要解锁的订单量为 {len(filter_record):>5}  {ext_str}"
        df = pd.DataFrame(sk_record)
        df.to_excel(f"./SK开头的订单_{s['name']}_{datetime_str}.xlsx")
        upload_file(f"./SK开头的订单_{s['name']}_{datetime_str}.xlsx")
        df = pd.DataFrame(filter_record)
        df.to_excel(f"./要取消的订单_{s['name']}_{datetime_str}.xlsx")
        upload_file(f"./要取消的订单_{s['name']}_{datetime_str}.xlsx")
        del_orderby(s['sid'], [r['seller_fulfillment_order_id'] for r in filter_record])
    print(message_text)
    send_message(message_text)

if __name__ == '__main__':

    #shops = get_seller_list()
    offset = 0
    length = 1000
    #for s in shops:
    orders = most_order_list_by_shop('', offset, length)
    pass

