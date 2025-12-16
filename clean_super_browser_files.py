import os
import time
import datetime
import shutil

def clean_old_files(root_dir, days_old=7):
    """
    列出目录下的文件，并删除指定天数之前创建的文件
    规则:
    1. 文件/文件夹必须超过指定天数(days_old)
    2. 删除条件:
       - 文件夹: 名称以 'FBA' 开头 -> 删除整个文件夹
       - 文件: 文件名以 'FBA' 开头 OR 所在文件夹名称包含 '船' -> 删除文件
    """
    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        return

    now = time.time()
    cutoff_time = now - (days_old * 86400)
    
    print(f"Scanning directory: {root_dir}")
    print(f"Deleting items created before: {datetime.datetime.fromtimestamp(cutoff_time)}")
    print("-" * 50)

    count_deleted_files = 0
    count_deleted_folders = 0
    count_skipped = 0
    
    # Use topdown=True to allow modifying dirnames to skip deleted directories
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        
        # 1. Check and delete directories starting with FBA
        # Iterate over a copy of dirnames to safe remove
        for dirname in dirnames[:]:
            dir_full_path = os.path.join(dirpath, dirname)
            try:
                creation_time = os.path.getctime(dir_full_path)
                if creation_time < cutoff_time and dirname.startswith("FBA"):
                    try:
                        shutil.rmtree(dir_full_path)
                        print(f"[DELETED FOLDER] {dir_full_path} (Old & starts with 'FBA')")
                        dirnames.remove(dirname) # Stop os.walk from entering this directory
                        count_deleted_folders += 1
                    except Exception as e:
                         print(f"[ERROR] Could not delete folder {dir_full_path}: {e}")
                else:
                    # Keep folder for now (will be entered)
                    pass
            except Exception as e:
                print(f"Error accessing dir {dir_full_path}: {e}")

        # 2. Check files in the current directory (that wasn't deleted)
        parent_folder_name = os.path.basename(dirpath)
        is_ship_folder = "船" in parent_folder_name
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                creation_time = os.path.getctime(file_path)
                file_age_days = (now - creation_time) / 86400
                
                # Format creation time for display
                creation_date_str = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"Found file: {file_path}")
                print(f"  Created: {creation_date_str} ({file_age_days:.1f} days ago)")
                
                if creation_time < cutoff_time:
                    is_fba_file = filename.startswith("FBA")
                    
                    if is_fba_file or is_ship_folder:
                        try:
                            os.remove(file_path)
                            reason = []
                            if is_fba_file: reason.append("filename starts with 'FBA'")
                            if is_ship_folder: reason.append("folder contains '船'")
                            print(f"  [DELETED FILE] Matches criteria: {' or '.join(reason)}")
                            count_deleted_files += 1
                        except Exception as e:
                            print(f"  [ERROR] Could not delete file: {e}")
                    else:
                        print(f"  [KEPT] Old but doesn't match name criteria.")
                        count_skipped += 1
                else:
                    print(f"  [KEPT] Recent file.")
                    count_skipped += 1
                    
            except Exception as e:
                print(f"Error accessing {file_path}: {e}")
            
            print("-" * 30)

    print(f"\nSummary:")
    print(f"Deleted folders: {count_deleted_folders}")
    print(f"Deleted files: {count_deleted_files}")
    print(f"Kept files: {count_skipped}")

if __name__ == "__main__":
    target_dir = r"C:\Users\Administrator\Desktop\Super Browser"
    clean_old_files(target_dir)
