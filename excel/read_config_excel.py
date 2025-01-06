import pandas as pd
import os
import pandas as pd
import os
global glv
glv = {}
glv['final_excel'] = "D:\\final.xlsx"
def get_size(sku):
    sku = str(sku).lower()
    return sku.split("-")[-1] if sku.split("-")[-1].find("x") > 0 else sku.split("-")[-2]
def check_size():
    import pandas as pd
    df = pd.read_excel(glv['final_excel'])
    max_size = 0
    max_size_code = ''
    for sku in df['SKU']:
        size_code = get_size(sku)
        now_size = int(size_code.split("x")[0]) * int(size_code.split("x")[1])
        if max_size < now_size:
            max_size = now_size
            max_size_code = size_code
    print(max_size_code, df['工厂'][0:1].values[0])
    config_path = "D:\\config\\"
    config_excel_file = ""
    for file in os.listdir(config_path):
        config_excel_file = config_path + file
    print("最大：", config_excel_file)

    config_df = pd.read_excel(config_excel_file, sheet_name="尺寸信息表")
    config_df['volume'] = config_df['外箱规格长（cm）'] * config_df['外箱规格宽（cm）'] * config_df['外箱规格高（cm）'] / 1000000
    max_volume = config_df[(config_df['尺寸'] == max_size_code) & (config_df['工厂'] == df['工厂'][0:1].values[0])]
    glv['max_volume'] = max_volume['volume'].values[0]
    glv['config_df'] = config_df
if __name__ == '__main__':
    check_size()