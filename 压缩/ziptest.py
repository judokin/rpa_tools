import os
import zipfile

def compress_folder_to_zip(folder_path):
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

# 调用函数
compress_folder_to_zip(r"D:\test\FBA18PLZLJ0Y")
