import requests
import configparser

# 创建ConfigParser对象
config = configparser.ConfigParser()

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
        print("Access Token Info:", access_token_info)
        return access_token_info
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response content:", response.text)


def generate_sign(params, access_token, app_key, timestamp, app_id):
    import hashlib
    import urllib.parse
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    import base64
    """
    生成签名并进行AES加密和URL编码。

    :param params: dict, 业务请求参数
    :param access_token: str, 访问令牌
    :param app_key: str, 应用密钥
    :param timestamp: str, 时间戳
    :param app_id: str, 应用ID，用作AES加密密钥
    :return: dict, 包含生成的签名和编码后的签名
    """
    # 添加固定参数
    params.update({
        'access_token': access_token,
        'app_key': app_key,
        'timestamp': timestamp
    })

    # 按照key的ASCII排序
    sorted_params = sorted(params.items(), key=lambda item: item)

    # 拼接参数，忽略值为空的参数
    param_str = '&'.join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params if v not in [None, '']])

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
    access_token = get_access_token()
    # params, access_token, app_key, timestamp, app_id
    params = {}
    app_key = config['DEFAULT']['appKey']
    timestamp = '1678900000'
    app_id = config['DEFAULT']['appId']
    sign = generate_sign(params, access_token["accessToken"], app_key, timestamp, app_id)
    response = requests.get('https://openapi.lingxing.com/erp/sc/data/seller/lists')
    print(response.text)

if __name__ == '__main__':
    #get_access_token()
    get_seller_list()