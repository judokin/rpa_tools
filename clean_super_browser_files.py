import os
import time
import datetime

def clean_old_files(root_dir, days_old=7):
    """
    列出目录下的文件，并删除指定天数之前创建的文件
    """
    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        return

    now = time.time()
    cutoff_time = now - (days_old * 86400)
    
    print(f"Scanning directory: {root_dir}")
    print(f"Deleting files created before: {datetime.datetime.fromtimestamp(cutoff_time)}")
    print("-" * 50)

    count_deleted = 0
    count_skipped = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                creation_time = os.path.getctime(file_path)
                file_age_days = (now - creation_time) / 86400
                
                # Format creation time for display
                creation_date_str = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"Found: {file_path}")
                print(f"  Created: {creation_date_str} ({file_age_days:.1f} days ago)")
                
                if creation_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"  [DELETED] File is older than {days_old} days.")
                        count_deleted += 1
                    except Exception as e:
                        print(f"  [ERROR] Could not delete file: {e}")
                else:
                    print(f"  [KEPT] File is recent.")
                    count_skipped += 1
                    
            except Exception as e:
                print(f"Error accessing {file_path}: {e}")
            
            print("-" * 30)

    print(f"\nSummary:")
    print(f"Deleted files: {count_deleted}")
    print(f"Kept files: {count_skipped}")

if __name__ == "__main__":
    target_dir = r"C:\Users\Administrator\Desktop\Super Browser"
    clean_old_files(target_dir)
