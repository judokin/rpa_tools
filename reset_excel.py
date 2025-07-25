import pandas as pd
import os
# C:\Users\Administrator\Desktop\Super Browser\亚马逊-北蓉-北美（子账号）\FBA18VBT9P7G_v2
import pymupdf as fitz  # PyMuPDF
def read_fnsku_from_pdf(input_pdf):
    # 打开输入 PDF 文件
    doc = fitz.open(input_pdf)
    # 创建一个新的 PDF 文档
    new_doc = fitz.open()

    for page_num in range(len(doc)):
        # 获取每一页
        page = doc[page_num]

        # 创建一个新页，将原页内容复制到新页
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.show_pdf_page(new_page.rect, doc, page_num)

        # 获取每页的文本块
        blocks = page.get_text("blocks")
        for block in blocks:
            x0, y0, x1, y1, text, _, _ = block
            name = text.split("\n")[0]
            print("读取pdf中的SKU为", name)
            break
        break
    return name
def read_products_pdf(dir_path):
    sku2fnsku = {}
    excel_file_name_list = []
    for path in os.listdir(dir_path):
        if not os.path.isdir(dir_path):
            continue
        #print(dir_path + '\\' + path)
        for excel_name in os.listdir(dir_path + '\\' + path + "\\"):
            if not excel_name.endswith(".xlsx"):
                continue
            excel_file_name_list.append(dir_path + '\\' + path + "\\" + excel_name)
        for pdf_name in os.listdir(dir_path + '\\' + path + "\\商品标签"):
            pdf_full_name = dir_path + '\\' + path + "\\商品标签\\" + pdf_name
            fn_skuname = read_fnsku_from_pdf(pdf_full_name)
            pdf_name = pdf_name.replace(".pdf", "")
            print(f"{pdf_name} {fn_skuname}")
            sku2fnsku[pdf_name] = fn_skuname
    return sku2fnsku, excel_file_name_list
def run(dir_path):
    sku2fnsku, excel_file_name_list = read_products_pdf(dir_path)
    for excel_file_name in excel_file_name_list:
        print("reading ", excel_file_name)
        df = pd.read_excel(excel_file_name, header=None)
        # df.loc[5] 加一格，内容为 
        sku_start = 6
        try:
            if df.loc[sku_start].values[-1] == 'FNSKU':
                continue
        except:
            continue
            pass
        df.loc[sku_start, "snsku"] = "FNSKU"
        for i in range(1, len(df)-6):
            sku_start += 1
            print("sku_start =", sku_start)
            sku_str = df.loc[sku_start].values[0]
            df.loc[sku_start, 'snsku'] = sku2fnsku[sku_str]
        df.to_excel(excel_file_name, index=False, header=None)
        print("save to", excel_file_name)

if __name__ == '__main__':
    dir_path = r'C:\Users\Administrator\Desktop\Super Browser\亚马逊-灿东-欧洲（子账号）\FBA15K9FD8W0_v2'
    run(dir_path)

    