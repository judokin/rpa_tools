import requests
import configparser
import time
import datetime
import copy
import pandas as pd

import logging
import os

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
        'appSecret': config['DEFAULT']['appSecret'],
        'appId': config['DEFAULT']['appId']
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
    :param access_token: str, 访问令牌
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
    app_id = config['DEFAULT']['appId']
    sign = generate_sign(params, access_token, timestamp, app_id)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    url = 'https://openapi.lingxing.com/erp/sc/data/seller/lists?' + ext_url
    response = requests.get(url)
    resp = response.json()
    count = 1
    shops = []
    for i,d in enumerate(resp['data']):
        shops.append(d)
        count += 1
    return shops

def order_list_by_shop(sid):
    access_token = get_access_token()
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
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
    app_id = config['DEFAULT']['appId']
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

def most_order_list_by_shop(sid, offset=0, length=100):
    access_token = get_access_token()
    start_date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    params = {
            "sid": str(sid),
            "length": length,
            "page": offset * length,
            "start_date": start_date,
            "end_date": end_date
            }
    headers = {
        'Content-Type': 'application/json'
    }
    print(params)
    access_token = access_token['data']['access_token']
    timestamp = str(int(time.time()))
    app_id = config['DEFAULT']['appId']
    sign = generate_sign(params, access_token, timestamp, app_id)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    #url = 'https://openapi.lingxing.com/order/amzod/api/orderList?' + ext_url
    url = 'https://openapi.lingxing.com/erp/sc/routing/order/Order/getOrderList?' + ext_url
    headers = {}
    for try_time in range(20):
        if try_time > 0:
            time.sleep(5)
            print("刚刚请求失败了，重试中~~~", try_time)
        try:
            response = requests.post(
                url,
                headers=headers,
                json=params,
                timeout=90
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
def send_message(message, webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/c6418617-4971-41b2-a00f-60b27e72007f"):
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
                timeout=60
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
    config_file_path = r"/root/rpa_tools/feishu/config.py"

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
def excute_sql(sql):
    import os
    import json
    import datetime
    import mysql.connector
    from mysql.connector import Error
    import sys
    import concurrent.futures

    # 配置数据库信息
    DB_CONFIG = {
        "host": "116.63.47.216",
        "user": "zhuzhenjin",
        "password": "plORmnE*KYnQRvF8",
        "database": "luyao"
    }
    """执行一个批次的SQL语句，每batch_size条提交一次"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()  # 批量提交
        print("SQL语句已成功执行！")
    except Error as e:
        message = f"数据库错误: {e}"
        print(message)
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def select_excute_sql(sql):
    import os
    import json
    import datetime
    import mysql.connector
    from mysql.connector import Error
    import sys
    import concurrent.futures
    import pandas as pd
    # 配置数据库信息
    DB_CONFIG = {
        "host": "116.63.47.216",
        "user": "zhuzhenjin",
        "password": "plORmnE*KYnQRvF8",
        "database": "luyao"
    }
    """执行SQL语句，如果是查询则返回DataFrame，非查询返回影响行数"""
    connection = None
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 执行SQL语句
        cursor.execute(sql)
        
        # 判断是否为查询语句
        if cursor.description:  # 有结果集返回说明是查询
            # 获取列名
            columns = [col[0] for col in cursor.description]
            # 获取数据并转换为DataFrame
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            return df
        else:  # 非查询语句
            connection.commit()
            return cursor.rowcount  # 返回受影响行数
            
    except Error as e:
        print(f"数据库错误: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        # 确保连接关闭
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def convert_unicode_in_json(json_str):
    import re
    def replace_match(match):
        return chr(int(match.group(1), 16))
    # 匹配 u 后跟4位十六进制数
    return re.sub(r'u([0-9a-fA-F]{4})', replace_match, json_str)
def get_order_detail_by_order_id(oid):
    access_token = get_access_token()
    start_date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    params = {
            "order_id": str(oid),
            }
    headers = {
        'Content-Type': 'application/json'
    }
    print(params)
    access_token = access_token['data']['access_token']
    timestamp = str(int(time.time()))
    app_id = config['DEFAULT']['appId']
    sign = generate_sign(params, access_token, timestamp, app_id)
    ext_url = f"access_token={access_token}&app_key={app_id}&timestamp={timestamp}&sign={sign['encrypted_sign']}"
    #url = 'https://openapi.lingxing.com/order/amzod/api/orderList?' + ext_url
    url = 'https://openapi.lingxing.com/erp/sc/data/mws/orderDetail?' + ext_url
    headers = {}
    for try_time in range(20):
        if try_time > 0:
            time.sleep(5)
            print("刚刚请求失败了，重试中~~~", try_time)
        try:
            response = requests.post(
                url,
                headers=headers,
                json=params,
                timeout=90
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
def up_data():
    from pymysql.converters import escape_string
    import json
    select_sql = '''select * from lingxing_push_orders where data_text like '%"warehouse_name": "测款发货仓"%' or data_text like '%u6d4bu6b3eu53d1u8d27u4ed3%'; '''
    #select_sql = '''select * from lingxing_push_orders where data_text like '%113-3002979-1772231%'; '''
    dt = select_excute_sql(select_sql)
    sum_str = 0
    for i in range(len(dt)):
        #print(dt.iloc[i])
        converted_data = convert_unicode_in_json(dt.iloc[i]['data_text'])
        json_obj = json.loads(converted_data)
        print(json_obj, json_obj['platform_list'][0])
        print(json_obj, json_obj['platform_list'])
        oid = json_obj['platform_list'][0]
        res = get_order_detail_by_order_id(oid)
        detail_text = json.dumps(res, ensure_ascii=False)
        id_str = dt.iloc[i]['id'] 
        sql = f''' update lingxing_push_orders set detail='{escape_string(detail_text)}' where id={id_str};  '''
        excute_sql(sql)
        sum_str += 1
        pass
    message_text = f'本次更新lingxing_push_orders数据{sum_str}条'
    print(message_text)
    send_message(message_text)
    pass
def run():
    import json
    import time
    #get_access_token()
    shops = get_seller_list()
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")
    message_text = ""
    #sids = [str(s['sid']) for s in shops]
    records = []
    for s_str in shops:
        print(s_str)
        sids = [str(s_str['sid'])]
        offset = 0
        length = 100
        while True:
            orders = most_order_list_by_shop(",".join(sids), offset, length)
            print(orders)
            time.sleep(1)
            if len(orders['data']) == 0:
                break
            offset += 1
            orders_copy = copy.deepcopy(orders)
            records += orders_copy['data']
    count_sql = '''select count(*) from lingxing_push_orders'''
    df_start = select_excute_sql(count_sql)
    for record in records:
        data_text = json.dumps(record)
        sql = f"""INSERT IGNORE INTO lingxing_push_orders (status, data_text, message, order_number) VALUES ('unsent', '{data_text}', '', '{record['order_number']}')""";
        while True:
            try:
                excute_sql(sql)
                break
            except:
                message_text = f'lingxing_push_orders 插入失败:{sql}'
                send_message(message_text)
                time.sleep(10)
                pass
        pass
    df_end = select_excute_sql(count_sql)
    sum = str(df_end.loc[0].values[0] - df_start.loc[0].values[0])
    records_sum = len(records)
    message_text = f'本次新增lingxing_push_orders数据{sum}条 采集到记录{records_sum}'
    print(message_text)
    send_message(message_text)

def up_index():
    from pymysql.converters import escape_string
    import json
    select_sql = '''select * from lingxing_push_orders where data_text like '%"warehouse_name": "测款发货仓"%' or data_text like '%u6d4bu6b3eu53d1u8d27u4ed3%'; '''
    #select_sql = '''select * from lingxing_push_orders where data_text like '%113-3002979-1772231%'; '''
    dt = select_excute_sql(select_sql)
    sum_str = 0
    for i in range(len(dt)):
        #print(dt.iloc[i])
        converted_data = convert_unicode_in_json(dt.iloc[i]['data_text'])
        json_obj = json.loads(converted_data)
        oid = json_obj['platform_list'][0]
        group_sql = f'''
        WITH t AS (
    SELECT
        order_number,
        1 AS tid
    FROM lingxing_push_orders lpo
    WHERE lpo.data_text LIKE '%{oid}%'
    GROUP BY lpo.order_number
)
SELECT
    *,
    ROW_NUMBER() OVER(ORDER BY order_number ASC) as row_num
FROM t
ORDER BY order_number ASC;
        '''
        gpdt = select_excute_sql(group_sql)
        print("gpdt =", len(gpdt))
        if len(gpdt) > 1:
            for index in range(len(gpdt)):
                id_str = gpdt.iloc[index]['order_number'] 
                row_num = gpdt.iloc[index]['row_num'] 
                row_num = index + 1
                print("row_num", row_num, id_str)
                sql = f''' update lingxing_push_orders set row_num='{row_num}' where order_number='{id_str}';  '''
                print(sql)
                excute_sql(sql)
                sum_str += 1
        pass
    message_text = f'本次更新lingxing_push_orders inex数据{sum_str}条'
    print(message_text)
    send_message(message_text)
    pass
if __name__ == '__main__':
    try:
        run()
        up_data()
        up_index()
        os.system('python /root/rpa_tools/xiaoxuanchuang/push_data.py')
    except Exception as e:
        print(e)
        send_message(str(e))
