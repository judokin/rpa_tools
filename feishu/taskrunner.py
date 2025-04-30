from apscheduler.schedulers.blocking import BlockingScheduler
import os
def job():
    os.system("python D:\\rpa_tools\\feishu\\feishu_uplaod_tk_mp4.py")

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour=13, minute=45)
scheduler.add_job(job, 'cron', hour=9, minute=45)

if __name__ == "__main__":
    print("任务已启动，每天9:45, 13:45 运行一次")
    scheduler.start()