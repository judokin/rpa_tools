"""
# 适用环境python3
"""
import os
import platform
import shutil
import time
import traceback
import uuid
import json
import requests
import subprocess
from playwright import sync_api
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import pandas as pd

from datetime import datetime, timedelta

def get_last_day_of_previous_month():
    # 获取当前日期
    current_date = datetime.now()
    
    # 计算当月第一天
    first_day_current = current_date.replace(day=1)
    
    # 计算上个月最后一天
    last_day_previous = first_day_current - timedelta(days=1)
    
    return last_day_previous

# 获取并格式化结果
last_day = get_last_day_of_previous_month()
path_name = last_day.strftime('%Y%m')
last_day = last_day.strftime('%Y-%m-%d')
dowload_path = f'D:\data\亚马逊ASIN紫鸟点击率\{path_name}'
os.makedirs(dowload_path, exist_ok=True)
print("上个月最后一天:", last_day)

df = pd.read_excel(R'D:\data\亚马逊ASIN紫鸟点击率\亚马逊ASIN紫鸟点击率-取数店铺list.xlsx')
datas = [df.loc[i]['店铺'] for i in range(len(df))]
datas_dict = {}
for data in datas:
    data_split = data.split('-')
    if data_split[1] not in datas_dict:
        datas_dict[data_split[1]] = []
    datas_dict[data_split[1]].append(str('gb' if data_split[2] == 'UK' else data_split[2].lower()))
    #data_v2 = data_split[1] + '-' + str('gb' if data_split[2] == 'UK' else data_split[2].lower())

def kill_process():
    """
    杀紫鸟客户端进程
    """
    # 确认是否继续
    os.system('taskkill /f /t /im SuperBrowser.exe')


def start_browser():
    """
    启动客户端
    :return:
    """
    try:
        if is_windows:
            cmd = [client_path, '--run_type=web_driver', '--ipc_type=http', '--port=' + str(socket_port)]
        elif is_mac:
            cmd = ['open', '-a', client_path, '--args', '--run_type=web_driver', '--ipc_type=http',
                   '--port=' + str(socket_port)]
        else:
            exit()
        subprocess.Popen(cmd)
        time.sleep(5)
    except Exception:
        print('start browser process failed')
        return


def update_core():
    """
    下载所有内核，打开店铺前调用，需客户端版本5.285.7以上
    因为http有超时时间，所以这个action适合循环调用，直到返回成功
    """
    data = {
        "action": "updataCore",
        "requestId": str(uuid.uuid4()),
    }
    data.update(user_info)
    while True:
        result = send_http(data)
        print(result)
        if result is None:
            print("等待客户端启动...")
            time.sleep(2)
            continue
        if result.get("statusCode") is None or result.get("statusCode") == -10003:
            print("当前版本不支持此接口，请升级客户端")
            return
        elif result.get("statusCode") == 0:
            print("更新内核完成")
            return
        else:
            print(f"等待更新内核: {json.dumps(result)}")
            time.sleep(2)


def send_http(data):
    """
    通讯方式
    :param data:
    :return:
    """
    try:
        url = 'http://127.0.0.1:{}'.format(socket_port)
        response = requests.post(url, json.dumps(data).encode('utf-8'), timeout=120)
        return json.loads(response.text)
    except Exception as err:
        print(err)


def delete_all_cache():
    """
    删除所有店铺缓存
    非必要的，如果店铺特别多、硬盘空间不够了才要删除
    """
    if not is_windows:
        return
    local_appdata = os.getenv('LOCALAPPDATA')
    cache_path = os.path.join(local_appdata, 'SuperBrowser')
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)


def delete_all_cache_with_path(path):
    """
    :param path: 启动客户端参数使用--enforce-cache-path时设置的缓存路径
    删除所有店铺缓存
    非必要的，如果店铺特别多、硬盘空间不够了才要删除
    """
    if not is_windows:
        return
    cache_path = os.path.join(path, 'SuperBrowser')
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)


def open_store(store_info, isWebDriverReadOnlyMode=0, isprivacy=0, isHeadless=0, cookieTypeSave=0, jsInfo=""):
    request_id = str(uuid.uuid4())
    data = {
        "action": "startBrowser"
        , "isWaitPluginUpdate": 0
        , "isHeadless": isHeadless
        , "requestId": request_id
        , "isWebDriverReadOnlyMode": isWebDriverReadOnlyMode
        , "cookieTypeLoad": 0
        , "cookieTypeSave": cookieTypeSave
        , "runMode": "1"
        , "isLoadUserPlugin": False
        , "pluginIdType": 1
        , "privacyMode": isprivacy
    }
    data.update(user_info)

    if store_info.isdigit():
        data["browserId"] = store_info
    else:
        data["browserOauth"] = store_info

    if len(str(jsInfo)) > 2:
        data["injectJsInfo"] = json.dumps(jsInfo)

    r = send_http(data)
    if str(r.get("statusCode")) == "0":
        return r
    elif str(r.get("statusCode")) == "-10003":
        print(f"login Err {json.dumps(r, ensure_ascii=False)}")
        exit()
    else:
        print(f"Fail {json.dumps(r, ensure_ascii=False)} ")
        exit()


def close_store(browser_oauth):
    request_id = str(uuid.uuid4())
    data = {
        "action": "stopBrowser"
        , "requestId": request_id
        , "duplicate": 0
        , "browserOauth": browser_oauth
    }
    data.update(user_info)

    r = send_http(data)
    if str(r.get("statusCode")) == "0":
        return r
    elif str(r.get("statusCode")) == "-10003":
        print(f"login Err {json.dumps(r, ensure_ascii=False)}")
        exit()
    else:
        print(f"Fail {json.dumps(r, ensure_ascii=False)} ")
        exit()


def get_browser_list() -> list:
    request_id = str(uuid.uuid4())
    data = {
        "action": "getBrowserList",
        "requestId": request_id
    }
    data.update(user_info)

    r = send_http(data)
    if str(r.get("statusCode")) == "0":
        print(r)
        return r.get("browserList")
    elif str(r.get("statusCode")) == "-10003":
        print(f"login Err {json.dumps(r, ensure_ascii=False)}")
        exit()
    else:
        print(f"Fail {json.dumps(r, ensure_ascii=False)} ")
        exit()


# 获取playwright浏览器会话
def get_browser_context(playwright, port):
    browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:" + str(port))
    context = browser.contexts[0]
    return context


def open_ip_check(browser_context, ip_check_url):
    """
    打开ip检测页检测ip是否正常
    :param browser_context: playwright浏览器会话
    :param ip_check_url ip检测页地址
    :return 检测结果
    """
    try:
        page = browser_context.pages[0]
        page.goto(ip_check_url)
        success_button = page.locator('//button[contains(@class, "styles_btn--success")]')
        success_button.wait_for(timeout=60000)  # 等待查找元素60秒
        print("ip检测成功")
        return True
    except PlaywrightTimeoutError:
        print("ip检测超时")
        return False
    except Exception as e:
        print("ip检测异常:" + traceback.format_exc())
        return False


def open_launcher_page(browser_context, launcher_page):
    page = browser_context.pages[0]
    page.goto(launcher_page)
    time.sleep(6)


def get_exit():
    """
    关闭客户端
    :return:
    """
    data = {"action": "exit", "requestId": str(uuid.uuid4())}

    data.update(user_info)

    print('@@ get_exit...' + json.dumps(data))
    send_http(data)


def use_one_browser_run_task(playwright, browser, download = False):
    """
    打开一个店铺运行脚本
    :param playwright: playwright浏览器会话
    :param browser: 店铺信息
    """
    # 如果要指定店铺ID, 获取方法:登录紫鸟客户端->账号管理->选择对应的店铺账号->点击"查看账号"进入账号详情页->账号名称后面的ID即为店铺ID
    store_id = browser.get('browserOauth')
    store_name = browser.get("browserName")
    # 打开店铺
    print(f"=====打开店铺：{store_name}=====")
    ret_json = open_store(store_id)
    print(ret_json)
    store_id = ret_json.get("browserOauth")
    if store_id is None:
        store_id = ret_json.get("browserId")
    browser_context = get_browser_context(playwright, ret_json.get('debuggingPort'))
    page = browser_context.pages[0]
    if download:
        #page.goto(f"https://sellercentral.amazon.de/brand-analytics/download-manager")
        # download_dir = "D:\data\亚马逊ASIN紫鸟点击率\\"
        for k, v in datas_dict.items():
            if store_name.find(k) < 0:
                continue
            for country in v:
                year = last_day[0:4]
                page.goto(f"https://sellercentral.amazon.com/brand-analytics/dashboard/brand-catalog-performance?view-id=brand-catalog-performance-default-view&reporting-range=monthly&monthly-year={year}&{year}-month={last_day}&country-id={country}")
                page.locator('.css-14njiag').nth(0).click(); 
                 # 等待至少一个下载按钮出现
                page.wait_for_selector("text=下载", timeout=10000)
                time.sleep(10)
                buttons = page.locator("span[class^='css-']:has-text('下载')").all()
                print(f"检测到 {len(buttons)} 个下载按钮")
                for i, button in enumerate(buttons):
                    print(f"处理第 {i+1}/{len(buttons)} 个下载")
                    try:
                        # 使用下载事件监听器（更可靠）
                        with page.expect_download() as download_handler:
                            button.click()
                        # 获取下载对象
                        download = download_handler.value
                        print(download.suggested_filename)
                        file_name = download.suggested_filename.split("_搜索目录绩效_简单_")
                        save_name = store_name.split("（子")[0] + "-" + file_name[0] + "_" + file_name[1]
                        save_name = save_name.replace("--", "-")
                        # 等待下载完成并保存到特定路径
                        download.save_as(f"{dowload_path}\{save_name}")
                        # 打印下载目录
                        print(f"已保存: {dowload_path}\{save_name}")
                        #print(download.dir)
                    except:
                        pass
                    if i >= len(v) - 1:
                        break
                #import pdb;pdb.set_trace()
                break
        pass
    else:
        for k, v in datas_dict.items():
            if store_name.find(k) < 0:
                continue
            for country in v:
                year = last_day[0:4]
                page.goto(f"https://sellercentral.amazon.com/brand-analytics/dashboard/brand-catalog-performance?view-id=brand-catalog-performance-default-view&reporting-range=monthly&monthly-year={year}&{year}-month={last_day}&country-id={country}")
                print(store_name, country)
                # https://sellercentral.amazon.de/brand-analytics/download-manager
                time.sleep(10)
                # import pdb;pdb.set_trace()
                page.click("id=GenerateDownloadButton")
                time.sleep(3)
                page.click("id=downloadModalGenerateDownloadButton")
                time.sleep(10)
                # import pdb;pdb.set_trace()
                pass
    # 获取playwright浏览器会话
    #browser_context = get_browser_context(playwright, ret_json.get('debuggingPort'))
    if browser_context is None:
        print(f"=====关闭店铺：{store_name}=====")
        close_store(store_id)
        return

    # 获取ip检测页地址
    ip_check_url = ret_json.get("ipDetectionPage")
    if not ip_check_url:
        print("ip检测页地址为空，请升级紫鸟浏览器到最新版")
        print(f"=====关闭店铺：{store_name}=====")
        close_store(store_id)
        exit()
    # 执行脚本
    try:
        ip_usable = open_ip_check(browser_context, ip_check_url)
        if ip_usable:
            print("ip检测通过，打开店铺平台主页")
            open_launcher_page(browser_context, ret_json.get("launcherPage"))
            # 打开店铺平台主页后进行后续自动化操作
        else:
            print("ip检测不通过，请检查")
    except:
        print("脚本运行异常:" + traceback.format_exc())
    finally:
        print(f"=====关闭店铺：{store_name}=====")
        close_store(store_id)


def use_all_browser_run_task(playwright, browser_list):
    """
    循环打开所有店铺运行脚本
    :param playwright: playwright浏览器会话
    :param browser_list: 店铺列表
    """
    browser_list_v2 = []
    print("=====开始运行脚本=====")
    for browser in browser_list:
        if '北美' not in browser['tags']:
            continue
        if browser['browserName'].find('客服') > 0:
            continue
        if sum([1 if browser['browserName'].find(data.split('-')[1]) > 0 else 0 for data in datas]) == 0:
            continue
        print(browser)
        browser_list_v2.append(browser)
        #use_one_browser_run_task(playwright, browser)
    for browser in browser_list_v2:
        use_one_browser_run_task(playwright, browser)
        use_one_browser_run_task(playwright, browser, True)

if __name__ == "__main__":
    """ 需要从系统右下角角标将紫鸟浏览器退出后再运行"""
    is_windows = platform.system() == 'Windows'
    is_mac = platform.system() == 'Darwin'

    if not is_windows and not is_mac:
        print("webdriver/cdp只支持windows和mac操作系统")
        exit()

    if is_windows:
        client_path = R'C:\Users\Public\SuperBrowser\starter.exe'  # 客户端程序starter.exe的路径
    else:
        client_path = R'ziniao'  # 客户端程序名称
    socket_port = 16851  # 系统未被占用的端口

    user_info = {
        "company": "杭州陆遥科技有限公司",
        "username": "自动化专用",
        "password": "Huojian2024"
    }

    """  
    windows用
    有店铺运行的时候，会删除失败
    删除所有店铺缓存，非必要的，如果店铺特别多、硬盘空间不够了才要删除
    delete_all_cache()

    启动客户端参数使用--enforce-cache-path时用这个方法删除，传入设置的缓存路径删除缓存
    delete_all_cache_with_path(path)
    """

    # 终止紫鸟客户端已启动的进程
    kill_process()

    print("=====启动客户端=====")
    start_browser()
    print("=====更新内核=====")
    update_core()

    """获取店铺列表"""
    print("=====获取店铺列表=====")
    browser_list = get_browser_list()
    if browser_list is None:
        print("browser list is empty")
        exit()

    """获取playwright浏览器会话"""
    sync_playwright = sync_api.sync_playwright().start()

    """打开第一个店铺运行脚本"""
    #use_one_browser_run_task(sync_playwright, browser_list[0])

    """循环打开所有店铺运行脚本"""
    use_all_browser_run_task(sync_playwright, browser_list)

    sync_playwright.stop()

    """关闭客户端"""
    get_exit()
    import os
    os.system(r"python D:\data\亚马逊ASIN紫鸟点击率\insert_db_by_excel.py")
    import requests
    import json
    import socket

    # 获取当前计算机名称
    computer_name = socket.gethostname()

    print(f"当前计算机名称是: {computer_name}")
    # 替换为你的飞书 Webhook URL
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/c6418617-4971-41b2-a00f-60b27e72007f"

    # 发送的消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": f"{computer_name} ods_amazon_asin_click 数据下载完毕"
        }
    }

    # 发送请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 打印结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")

