import pandas as pd
def read_data():
    df = pd.read_excel("2025.01美国站地毯TOP30链接.xlsx")
    return df
from bs4 import BeautifulSoup
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    # 创建浏览器上下文
    context = browser.new_context()
    
    # 从cookies.json加载cookies
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
        
        # 修正cookies格式
        for cookie in cookies:
            # 确保包含必要字段
            same_site = cookie.get("sameSite")
            
            # 处理空值或缺失字段
            if not same_site:
                cookie["sameSite"] = "Lax"  # 默认值
            else:
                # 规范化字符串格式
                cookie["sameSite"] = str(same_site).capitalize()
            
            # 强制修正非法值
            if cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                cookie["sameSite"] = "Lax"
                
        context.add_cookies(cookies)
    
    # 创建页面并跳转
    page = context.new_page()
    df = pd.read_excel("2025.01美国站地毯TOP30链接.xlsx")
    datas = []
    for i in range(len(df)):
        ASIN = df.iloc[i]['ASIN']
        page_number = 1
        while True:
            break_while = False
            for trytimes in range(99):
                try:
                    page.goto(f"https://www.amazon.com/product-reviews/{ASIN}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&mediaType=media_reviews_only&pageNumber={page_number}&sortBy=recent")
                    # 等待页面加载完成
                    page.wait_for_load_state("networkidle")

                    #print(page.title())
                    print("page_number~~~", page_number, "ASIN~~~", ASIN)
                    content = page.content()
                    #print(page.content())
                    #open("html", "w", encoding="gbk", errors="ignore").write(content)
                    soup = BeautifulSoup(content, 'html.parser')
                    #open("cm_cr-review_list", "w", encoding="gbk", errors="ignore").write(str(soup.find(id="cm_cr-review_list")))
                    page_datas = []
                    aulist = soup.find(id="cm_cr-review_list").find_all(class_="a-unordered-list")
                    if len(aulist) == 0:
                        break_while = True
                        break
                    aoks = aulist[0].find_all(class_="aok-relative")
                    if len(aoks) == 0:
                        break_while = True
                        break
                    for aok in aoks:
                        data = {}
                        data['ASIN'] = ASIN
                        data['商品详情页链接'] = df.iloc[i]['商品详情页链接']
                        data['父ASIN'] = df.iloc[i]['父ASIN']
                        data['star_text'] = aok.find(class_="a-icon-alt").text
                        data['review_title'] = aok.find(class_="a-icon-alt").findNext().findNext().text
                        data['review_date'] = aok.find(class_="review-date").text
                        data['review_text_content'] = aok.find(class_="review-text-content").text
                        data['color_size_text'] = aok.find_all("a")[2].text
                        imgs = aok.find_all(class_="review-image-tile")
                        for i, img in enumerate(imgs):
                            data['src' + str(i)] = img.attrs['src'].replace("._SY88.jpg", "._SL1600_.jpg")
                        page_datas.append(data)
                    break
                except Exception as e:
                    print(e)
                    print("page goto, trytimes~~~~~", trytimes)
                    pass
            if break_while:
                break
            datas += page_datas
            page_number += 1
            print("save~~~~~~~~")
            dts = pd.DataFrame(datas)
            dts.to_excel("2025.01美国站地毯TOP30链接_reviews.xlsx", index=False)
    pass
    #browser.close()