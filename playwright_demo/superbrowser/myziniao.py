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
import datetime
from read_html import read_page
from read_html import read_page_v2
import pandas as pd
import sys

datetime_str = datetime.datetime.now().strftime('%Y%m%d')

def send_message(message, webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/e49f7f96-12a2-494e-b724-56b0de221f84"):
    import requests
    import json
    # 发送的消息内容
    message = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    # 发送请求
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(message))

    # 打印结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")


def kill_process():
    """
    杀紫鸟客户端进程
    """
    # 确认是否继续
    #confirmation = input("在启动之前，需要先关闭紫鸟浏览器的主进程，确定要终止进程吗？(y/n): ")
    confirmation = 'y'
    if confirmation.lower() == 'y':
        if is_windows:
            os.system('taskkill /f /t /im SuperBrowser.exe')
        elif is_mac:
            os.system('killall ziniao')
            time.sleep(3)
    else:
        exit()


def start_browser(headerless=True):
    """
    启动客户端浏览器。

    :param headerless: 是否以无头模式启动浏览器。默认为 False。
    :return:
    """
    try:
        # 定义基础命令
        base_cmd = []

        if is_windows:
            base_cmd = [client_path, '--run_type=web_driver', '--ipc_type=http', f'--port={socket_port}']
        elif is_mac:
            base_cmd = ['open', '-a', client_path, '--args']
            # 将后续参数添加到列表中
            base_cmd.extend(['--run_type=web_driver', '--ipc_type=http', f'--port={socket_port}'])
        else:
            print("Unsupported operating system.")
            sys.exit(1)

        # 如果需要无头模式，添加相应的参数
        if headerless:
            if is_windows or is_mac:
                base_cmd.append('--headless')
            else:
                print("无头模式仅在 Windows 和 macOS 上支持。")
                sys.exit(1)

        # 启动浏览器进程
        subprocess.Popen(base_cmd)
        time.sleep(5)  # 等待浏览器启动

    except Exception as e:
        print('启动浏览器进程失败:', e)
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


def use_one_browser_run_task(playwright, browser):
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
    # 获取playwright浏览器会话
    browser_context = get_browser_context(playwright, ret_json.get('debuggingPort'))
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
            # 跳转到网址：sellercentral.amazon.com/orders-v3/all?page=1 
            print("开始执行脚本...")
            page = browser_context.pages[0]
            all_datas = []
            for i in range(1, 999):
                print(f"第{i}次访问")
                page.goto(f"https://sellercentral.amazon.com/orders-v3/ref=xx_myo_favb_xx?date-range=last-14&sort=ship_by_asc&page={i}")
                # 等待5秒
                page.wait_for_timeout(5000)
                if not os.path.exists(store_name):
                    os.mkdir(store_name)
                folder_name = f'''{store_name}/''' + datetime.datetime.now().strftime("%Y%m%d")
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                html_content = page.content()
                with open(f'{folder_name}/page_{i}.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"读取~~{folder_name}/page_{i}.html")
                datas, order_size = read_page_v2(f'{folder_name}/page_{i}.html')
                all_datas += datas
                # if i >= 1 + order_size // 100:
                #     break
                # 如果时间是10天以内，则停止访问
                try:
                    if datetime.datetime.now() - (pd.to_datetime(datas[-1][1] + " " + datas[-1][2])  + pd.Timedelta(hours=16)) <= pd.Timedelta(days=10):
                        break
                except:
                    break
                if len(datas) == 0:
                    break
            df = pd.DataFrame(all_datas)
            df.to_excel(f'{store_name}/{datetime.datetime.now().strftime("%Y%m%d")}.xlsx', index=False)
            if not os.path.exists(f"logs/{datetime_str}"):
                os.makedirs(f"logs/{datetime_str}")
            open(f"logs/{datetime_str}/{store_name}", "w").write("")
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
    for browser in browser_list:
        use_one_browser_run_task(playwright, browser)


if __name__ == "__main__":
    """ 需要从系统右下角角标将紫鸟浏览器退出后再运行"""
    is_windows = platform.system() == 'Windows'
    is_mac = platform.system() == 'Darwin'

    if not is_windows and not is_mac:
        print("webdriver/cdp只支持windows和mac操作系统")
        exit()

    if is_windows:
        client_path = R'D:\soft\ziniao\ziniao.exe'  # 客户端程序starter.exe的路径
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
    
    # 检查日志文件中已经存在的店铺，如果存在，则跳过
    import glob
    existing_stores = set([os.path.basename(file) for file in glob.glob(f"logs/{datetime_str}/*")])
    print("本次运行跳过以下店铺：\n", "\n".join(existing_stores))
    browser_list = [b for b in browser_list if b['platform_name']  in ['亚马逊-美国'] and b["browserName"] not in existing_stores]
    """循环打开所有店铺运行脚本"""
    # 统计消耗时间
    start_time = time.time()
    use_all_browser_run_task(sync_playwright, browser_list)
    end_time = time.time()
    msg = "=====直接爬官网，脚本运行完成=====,use time: %ss" % round((end_time - start_time), 2)
    print(msg)
    send_message(msg)
    os.system("python D:\\rpa_tools\\playwright_demo\\superbrowser\\read_orders.py")
    #sync_playwright.stop()

    """关闭客户端"""
    #get_exit()

