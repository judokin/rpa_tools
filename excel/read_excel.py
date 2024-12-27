import pandas as pd
import os
def get_size(sku):
    return sku.split("-")[-1] if sku.split("-")[-1].find("x") > 0 else sku.split("-")[-2]
def cm_to_inches(cm):
    """
    将厘米转换为英寸，保留两位小数
    :param cm: 输入的长度（厘米）
    :return: 转换后的长度（英寸），保留两位小数
    """
    if cm < 0:
        raise ValueError("长度不能为负数")
    inches = cm / 2.54
    return round(inches, 2)
def kg_to_pounds(kg):
    """
    将千克转换为英磅，保留四位小数
    :param kg: 输入的重量（千克）
    :return: 转换后的重量（英磅），保留四位小数
    """
    if kg < 0:
        raise ValueError("重量不能为负数")
    pounds = kg * 2.20462
    return round(pounds, 4)
def reset_excel():
    file_path = "D:\\data\\"
    excel_file = ""
    for file in os.listdir(file_path):
        if file.startswith("~"):
            continue
        excel_file = file_path + file
        break
    print(excel_file)
    #excel_file = "D:\\data\创建货件自动化测试sku+数量.xlsx"
    df = pd.read_excel(excel_file)
    if '大件|标准件' in list(df.keys()):
        df['大件/标准件'] = df['大件|标准件']
    try:
        df = df["店铺,站点,ASIN,SKU,数量,船期,合同号,工厂,发货方式,大件/标准件".split(",")]
    except:
        raise Exception("数列名错误，请检查列名是否正确")
    # 对每个SKU执行get_size函数
    df['尺寸'] = df['SKU'].apply(lambda x: get_size(x))
    config_path = "D:\\config\\"
    config_excel_file = ""
    for file in os.listdir(config_path):
        config_excel_file = config_path + file
    print(config_excel_file)
    #excel_file = "D:\\data\创建货件自动化测试sku+数量.xlsx"
    config_df = pd.read_excel(config_excel_file, sheet_name="尺寸信息表")
    result = pd.merge(df, config_df, on=["工厂", "尺寸"], how="inner")
    if len(df) != len(result):
        raise Exception("数据不一致")
    #print(result)
    ext_keys = "Units per box,Box length (in),Box width (in),Box height (in),Box weight (lb)".split(",")
    df = result["店铺,站点,ASIN,SKU,数量,船期,合同号,工厂,发货方式,大件/标准件".split(",")]
    #result['船期'] = result['船期'].dt.strftime('%Y/%m/%d')
    #result.to_excel("d:\\result.xlsx", index=False)
    df[ext_keys[0]] = result['单箱数量(pcs)']
    df[ext_keys[1]] = result['外箱规格长（cm）'].apply(lambda x: cm_to_inches(x))
    df[ext_keys[2]] = result['外箱规格宽（cm）'].apply(lambda x: cm_to_inches(x))
    df[ext_keys[3]] = result['外箱规格高（cm）'].apply(lambda x: cm_to_inches(x))
    df[ext_keys[4]] = result['箱重（kg）'].apply(lambda x: kg_to_pounds(x))
    df['船期'] = df['船期'].dt.strftime('%Y/%m/%d')
    print(result)
    #df.to_excel("d:\\final.xlsx", index=False)
if __name__ == '__main__':
    reset_excel()