import json
import config as fsconfig
import requests
import os
import sys
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
payload = json.dumps({
"app_id": fsconfig.app_id,
"app_secret": fsconfig.app_secret
})
headers = {
'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.status_code)
print(response.text)
tenant_access_token = response.json()["tenant_access_token"]
headers = {
    "Authorization": f"Bearer {tenant_access_token}"
}

# curl -i -X GET 'https://open.feishu.cn/open-apis/drive/v1/files?direction=DESC&folder_token=NG6mfLFkNl831dd3m4lcjHRQnig&order_by=EditedTime' -H 'Authorization: Bearer t-g1041gefUGFS7GUYUZD6QTK5XXX3DVV6DZLP4G7Z'
def get_file_list(parent_node):
    url = f"https://open.feishu.cn/open-apis/drive/v1/files?direction=DESC&folder_token={parent_node}&order_by=EditedTime"
    response = requests.get(url, headers=headers)
    return response.json()
def create_folder(folder_name, parent_node):
    url = "https://open.feishu.cn/open-apis/drive/v1/files/create_folder"
    payload = json.dumps({
        "name": folder_name,
        "folder_token": parent_node
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
def upload_file(file_path, parent_node):
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    # file_path = "d://test//FBA18PLZLJ0Y.zip"
    # 判断文件大小
    file_size = os.stat(file_path).st_size
    files = {
        "file_name": (None, os.path.basename(file_path)),
        "parent_type": (None, "explorer"),
        "parent_node": (None, parent_node), # 文件夹，固定
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
    res_json = get_file_list("UOwyfGIWFl7cCSd33OtchVRMnZq")
    excel_list = []
    for item in res_json['data']['files']:
        excel_list.append(item['name'])
    # 列出D:\tiktok下的文件名的日期的文件夹
    file_list = []
    tk_folder = "D://tk_datas//"
    for file_name in os.listdir(tk_folder):
        if not file_name.endswith(".xlsx"):
            continue
        if file_name in excel_list:
            continue
        file_list.append(file_name)
        print(file_name)
        upload_file(os.path.join(tk_folder, file_name), "UOwyfGIWFl7cCSd33OtchVRMnZq")
    # from messange import send
    # send(f'上传到{dest_folder}完成，文件总数：{len(mp4file_list)}')
    #import pdb;pdb.set_trace()
    # local_folder = tk_folder + max(file_list)
    # dest_folder = max(file_list)
    
    # if dest_folder in folder_list:
    #     print(f'folder {dest_folder} already exists')
    #     sys.exit(0)
    # #create_folder(dest_folder, "NG6mfLFkNl831dd3m4lcjHRQnig")
    # res_json = get_file_list("UOwyfGIWFl7cCSd33OtchVRMnZq")
    # folder_id = ''
    # for item in res_json['data']['files']:
    #     if item['name'] == dest_folder:
    #         folder_id = item['token']
    #         break
    # mp4file_list = os.listdir(local_folder)
    # for i, mp4files in enumerate(mp4file_list):
    #     print(mp4files, f"这是第{i+1}个,共{len(mp4file_list)}个文件")
    #     upload_file(os.path.join(local_folder, mp4files), folder_id)
