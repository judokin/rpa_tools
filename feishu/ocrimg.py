import json
import config
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
with open('tenant_access_token', 'w') as f:
    f.write(tenant_access_token)
    
    
import requests
import base64

def recognize_image(image_path, access_token):
    # 读取图片并转换为 Base64
    with open(image_path, 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # 设置请求体
    data = {
        "image": image_base64
    }
    
    # 发送 POST 请求
    url = 'https://open.feishu.cn/open-apis/optical_char_recognition/v1/image/basic_recognize'
    response = requests.post(url, headers=headers, json=data)
    
    # 返回完整的响应信息（包含状态码和头部）
    return response

# 使用示例
if __name__ == "__main__":
    # 替换为你的实际参数
    image_path = r"D:\rpa_tools\报关\20251120-101700.jpg"  # 图片文件路径
    image_path = r"D:\rpa_tools\报关\20251120-101734.jpg"  # 图片文件路径
    #access_token = "t-g104bk937BG6I2XQOEGULG4TY4T3DDDI6R7FLYOX"  # 访问令牌
    
    result = recognize_image(image_path, tenant_access_token)
    
    print(f"Status Code: {result.status_code}")
    print("Headers:")
    for key, value in result.headers.items():
        print(f"  {key}: {value}")
    print("Body:")
    print(result.text)