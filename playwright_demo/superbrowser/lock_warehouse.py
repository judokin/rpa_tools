import json
import requests
import os
#from datetime import datetime
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
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

# 定义请求头
headers = {
  'Authorization': 'Bearer ' + tenant_access_token
}


def get_pinyin_initial(char):
    """
    返回单个汉字的拼音首字母（大写）
    对于非汉字字符，返回原字符
    """
    if not ('\u4e00' <= char <= '\u9fff'):
        return char  # 非汉字直接返回
    
    # 汉字Unicode编码范围与拼音首字母映射表
    mappings = [
        (0xB0A1, 0xB0C4, 'A'), (0xB0C5, 0xB2C0, 'B'), (0xB2C1, 0xB4ED, 'C'),
        (0xB4EE, 0xB6E9, 'D'), (0xB6EA, 0xB7A1, 'E'), (0xB7A2, 0xB8C0, 'F'),
        (0xB8C1, 0xB9FD, 'G'), (0xB9FE, 0xBBF6, 'H'), (0xBBF7, 0xBFA5, 'J'),
        (0xBFA6, 0xC0AB, 'K'), (0xC0AC, 0xC2E7, 'L'), (0xC2E8, 0xC4C2, 'M'),
        (0xC4C3, 0xC5B5, 'N'), (0xC5B6, 0xC5BD, 'O'), (0xC5BE, 0xC6D9, 'P'),
        (0xC6DA, 0xC8BA, 'Q'), (0xC8BB, 0xC8F5, 'R'), (0xC8F6, 0xCBF9, 'S'),
        (0xCBFA, 0xCDD9, 'T'), (0xCDDA, 0xCEF3, 'W'), (0xCEF4, 0xD188, 'X'),
        (0xD1B9, 0xD4D0, 'Y'), (0xD4D1, 0xD7F9, 'Z')
    ]
    
    # 获取汉字的GB2312编码（兼容GBK）
    try:
        gb_code = char.encode('gb2312')
        if len(gb_code) < 2:
            return char
        code = (gb_code[0] << 8) | gb_code[1]
    except:
        return char  # 编码失败时返回原字符
    
    # 查找对应的拼音首字母
    for start, end, initial in mappings:
        if start <= code <= end:
            return initial
    
    return char  # 未找到映射时返回原字符

def hanzi_to_pinyin_initials(text):
    """
    将输入字符串中的每个汉字转换为拼音首字母
    非汉字字符保持不变
    返回转换后的字符串（大写形式）
    """
    return ''.join(get_pinyin_initial(char) for char in text)

def get_table_data():
    # 查询多维表格数据
    # 定义目标URL
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/AMGjbywniabr1Os0phvcKPVenhd/tables/tbltznhmUZJ4MfyC/records/search?page_size=1000"
    # https://wit0jhu6kvu.feishu.cn/base/AMGjbywniabr1Os0phvcKPVenhd?table=tbltznhmUZJ4MfyC&view=vewdTsEhbe

    # 定义请求体
    data = {}

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 输出返回的状态码和响应数据
    print("Status Code:", response.status_code)
    response_json = {}
    try:
        response_json = response.json()
        #print("Response JSON:", response_json)
    except ValueError:
        print("Response Text:", response.text)
    return response_json

def insert_table_data(data={"records": [{"fields": {}}]}):
    # https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records
    # url = "https://open.feishu.cn/open-apis/bitable/v1/apps/AMGjbywniabr1Os0phvcKPVenhd/tables/tbltznhmUZJ4MfyC/records"
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/AMGjbywniabr1Os0phvcKPVenhd/tables/tbltznhmUZJ4MfyC/records/batch_create"
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())

# 获取群成员列表
# chat_id 到这里根据群名称来查 https://open.feishu.cn/document/server-docs/group/chat/search?appId=cli_a7d537a861a1d00e
# 杭州陆遥科技有限公司 oc_ac8b83a078b491f9c11b995ff8228a7c
def get_group_members(chat_id='oc_6cb224fd44af0f6a41d1e426c5b7c057'):
    params = {
        'page_size': '100',
    }
    response = requests.get(
        f'https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members',
        params=params,
        headers=headers,
    )
    return response.json()

def format_members(members):
    members_list = []
    for member in members['data']['items']:
        if member['user_type'] != 'bot':
            members_list.append(member['union_id'])
    return members_list

def reset_fields(data, record_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/AMGjbywniabr1Os0phvcKPVenhd/tables/tbltznhmUZJ4MfyC/records/{record_id}"
    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
if __name__ == '__main__':
    ggm = get_group_members(chat_id='oc_9eee7160909f931df231ad5427af9bee')
    import pdb;pdb.set_trace()
    pass