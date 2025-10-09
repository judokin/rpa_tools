from bs4 import BeautifulSoup
import re
def extract_numbers(s):
    return re.findall(r'\d+', s)
def read_page(page_name):
    file_path = page_name
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    datas = []
    for i, tr in enumerate(soup.find_all("tr")):
        tds = tr.find_all('td')
        if len(tds) < 10:
            continue
        try:
            day_str = tds[1].find_all('div')[4].text
            time_str = tds[1].find_all('div')[5].text
            order_status = tr.find_all(class_='order-status-column')[0].text
            datas.append([i, day_str, time_str, tr.find_all("td")[2].find('a').text, order_status])
        except:
            continue
    # soup 中找出类名为total-orders-heading的所有元素
    order_size = 0
    for element in soup.find_all(class_="total-orders-heading"):
        order_size = int(extract_numbers(element.find("span").text)[0])
        break
    return datas, order_size
def read_page_v2(page_name):
    file_path = page_name
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    datas = []
    for i, tr in enumerate(soup.find_all("tr")):
        tds = tr.find_all('td')
        if len(tds) < 8:
            continue
        try:
            day_str = tds[1].find_all('div')[4].text
            time_str = tds[1].find_all('div')[5].text
            order_status = tr.find_all(class_='order-status-column')[0].text
            datas.append([i, day_str, time_str, tr.find_all("td")[2].find('a').text, order_status])
        except:
            continue
    # soup 中找出类名为total-orders-heading的所有元素
    order_size = 0
    for element in soup.find_all(class_="total-orders-heading"):
        order_size = int(extract_numbers(element.find("span").text)[0])
        break
    return datas, order_size
if __name__ == '__main__':
    datas, order_size = read_page_v2('./亚马逊--冬豚（子账号）/20251009/page_1.html')
    print(len(datas), order_size)