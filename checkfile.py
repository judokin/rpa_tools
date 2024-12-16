from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class MyHandler(FileSystemEventHandler):
    # def on_modified(self, event):
    #     print(f"文件被修改: {event.src_path}")

    def on_created(self, event):
        os.system(f'python D:\\reset_pdf.py')

    # def on_deleted(self, event):
    #     print(f"文件被删除: {event.src_path}")

path = "D:\\rpa_log"
# 判断文件夹是否存在，如果不存在则创建
if not os.path.exists(path):
    os.mkdir(path)
    # 创建一个文件，以当前时间命名
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

print("监控已启动，按 Ctrl+C 停止")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
