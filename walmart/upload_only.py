# 设置当前目录为d:\rpa_tools
import os
import sys
import json

# 添加父目录到Python路径，确保可以导入feishu模块
parent_dir = r"D:\rpa_tools"
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
current_directory = r"d:\rpa_tools"
os.chdir(current_directory)
from feishu.send import send_message
def compress_folder_to_zip(folder_path):
    import os
    import zipfile
    # 获取文件夹的绝对路径和名称
    folder_path = os.path.abspath(folder_path)
    folder_name = os.path.basename(folder_path)
    
    # 设置压缩文件路径
    zip_file_path = os.path.join(os.path.dirname(folder_path), f"{folder_name}.zip")
    
    # 创建压缩文件
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 添加文件到 zip 中，同时保持文件的相对路径
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    
    print(f"压缩完成: {zip_file_path}")
def compress_and_upload(path):
    compress_folder_to_zip(path)
    from feishu.feishu_uplaod import upload_file
    res_text = upload_file(path + ".zip", parent_node='SZAtfM6FWlYadAddkrMcLgbCn5f')
    try:
        upload_res = json.loads(res_text)
        if upload_res['msg'] == "Success":
            message = path + ".zip上传成功"
            send_message(message, webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/7f3a0e71-4197-4d8c-a548-a03be2c9b373")
    except:
        message = path + ".zip上传成功"
        send_message(message, webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/7f3a0e71-4197-4d8c-a548-a03be2c9b373")
if __name__ == '__main__':
   name = open(r"D:\data\code\resetname.txt").read()
   pdf_directory = r"D:\data\walmart整理结果" + f"\{name}"
   compress_and_upload(pdf_directory)
    # test_path = r"C:\Users\Administrator