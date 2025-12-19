import json
import requests
import pandas as pd
from datetime import datetime
import importlib.util

# 指定文件路径
config_file_path = r"D:\rpa_tools\feishu\config.py"

# 加载模块
spec = importlib.util.spec_from_file_location("config", config_file_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# 获取访问令牌
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
payload = json.dumps({
    "app_id": config.app_id,
    "app_secret": config.app_secret
})
headers = {
    'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print("Token Status Code:", response.status_code)
tenant_access_token = response.json()["tenant_access_token"]

def get_table_data():
    # 查询多维表格数据
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/PHYRb04hHaE7aQsUeancUeSxnXg/tables/tbl7npO3aKkjV9ls/records/search?page_size=999"

    headers = {
        "Authorization": "Bearer " + tenant_access_token,
        "Content-Type": "application/json"
    }
    page_token = ''
    while True:
        data = {}
        if page_token:
            data = {"page_token": page_token}
        print(data)
        # 处理数据并创建DataFrame
        processed_data = []
        response = requests.post(url, headers=headers, json=data)

        print("API Status Code:", response.status_code)
        for i in range(10):
            try:
                data_json = response.json()
                break
            except ValueError:
                print("Response Text:", response.text)
                return None

        import pdb;pdb.set_trace()
        for item in data_json['data']['items']:
            record = {}
            fields = item['fields']
            record_id = item['record_id']
            
            # 处理普通字段
            record['record_id'] = record_id
            record['sessions'] = fields.get('sessions', 0)
            record['广告展示量'] = fields.get('广告展示量', 0)
            record['广告点击率'] = fields.get('广告点击率', 0)
            record['广告点击量'] = fields.get('广告点击量', 0)
            record['订单量'] = fields.get('订单量', 0)
            record['销量'] = fields.get('销量', 0)
            
            # 处理嵌套字典字段（列表类型）
            spu_list = fields.get('SPU', [])
            record['SPU'] = spu_list[0].get('text', '') if spu_list and len(spu_list) > 0 else ''
                
            category_list = fields.get('二级分类', [])
            record['二级分类'] = category_list[0].get('text', '') if category_list and len(category_list) > 0 else ''
                
            platform_list = fields.get('平台', [])
            record['平台'] = platform_list[0].get('text', '') if platform_list and len(platform_list) > 0 else ''
                
            site_list = fields.get('站点', [])
            record['站点'] = site_list[0].get('text', '') if site_list and len(site_list) > 0 else ''
            
            # 处理时间戳字段
            date_timestamp = fields.get('日期')
            if date_timestamp:
                record['日期'] = datetime.fromtimestamp(date_timestamp / 1000)
            else:
                record['日期'] = None
                
            processed_data.append(record)
        page_token = data_json['data']['page_token']
        print('total =', data_json['data']['total'])
        if data_json['data']['total'] == 0:
            break

    
    # 创建DataFrame
    df = pd.DataFrame(processed_data)
    
    # 重新排列列的顺序
    column_order = ['record_id', '日期', 'SPU', '二级分类', '平台', '站点', 
                   'sessions', '广告展示量', '广告点击率', '广告点击量', '订单量', '销量']
    
    # 只保留存在的列
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns + [col for col in df.columns if col not in existing_columns]]
    
    print("数据预览:")
    print(df.head())
    print(f"总共获取到 {len(df)} 条记录")
    
    # 保存为Excel文件
    excel_filename = f"feishu_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(excel_filename, index=False, engine='openpyxl')
    print(f"数据已成功保存到: {excel_filename}")
    
    return df

if __name__ == "__main__":
    df = get_table_data()