import pymupdf as fitz  # PyMuPDF
import os
import json
import pandas as pd
from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator
#import fitz  # PyMuPDF
import os
if os.path.exists("dev_config.py"):
    import dev_config as config
else:
    import config
import traceback
from feishu.send import send_message
#Imports Searchable PDFs and prints x,y coordinates

def reset_main_pdf_v2(input_pdf):
    fp = open(input_pdf, 'rb')
    output_pdf = input_pdf.replace("_temp.pdf", ".pdf")
    output_excel = input_pdf.replace("_temp.pdf", "_part_1.xlsx")


    manager = PDFResourceManager()
    laparams = LAParams()
    dev = PDFPageAggregator(manager, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, dev)
    pages = PDFPage.get_pages(fp)
    rg_data_0 = []
    rg_data_1 = []
    for page in pages:
        #print(' - Processing  -')
        interpreter.process_page(page)
        layout = dev.get_result()
        x, y, text = -1, -1, ''
        fba_regions = []
        fba_regions_dict = {}
        address_regions = []
        address_regions_dict = {}
        textboxes_infolist = []
        for textbox in layout:
            if isinstance(textbox, LTText):
                for line in textbox:
                    for char in line:
                        # If the char is a line-break or an empty space, the word is complete
                        if isinstance(char, LTAnno) or char.get_text() == ' ':
                            if x != -1:
                                #print('At %r is text: %s' % ((x, y), text))
                                textboxes_infolist.append([x, y, text])
                            x, y, text = -1, -1, ''
                        elif isinstance(char, LTChar):
                            text += char.get_text()
                            if x == -1:
                                x, y, = char.bbox[0], char.bbox[3]
        for textbox_info in textboxes_infolist:
            if textbox_info[2] == '目的地：' or len(fba_regions) > 0:
                fba_regions.append(textbox_info)
                fba_regions_dict[textbox_info[2]] = textbox_info
                if len(fba_regions) > 2 and fba_regions[-1][1] != fba_regions[-2][1]:
                    break
        for textbox_info in textboxes_infolist:
            if textbox_info[2] == 'Created:':
                break
            if textbox_info[2] == '发货地：' or len(address_regions) > 0:
                address_regions.append(textbox_info)
                address_regions_dict[textbox_info[2]] = textbox_info
                if len(address_regions) > 3 and address_regions[-1][1] != address_regions[-2][1]:
                    break
        rg_data_0.append([fba_regions, fba_regions_dict])
        rg_data_1.append([address_regions, address_regions_dict])
        #print(fba_regions)
        
        #print(fba_regions_dict)
        # If the last symbol in the PDF was neither an empty space nor a LTAnno, print the word here
        if x != -1:
            print('Atttt %r is text: %s' % ((x, y), text))
        #break
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
        # 定义横向缩放矩阵
        for i, block in enumerate(blocks):
            # 获取文本块的坐标和内容
            x0, y0, x1, y1, text, _, _ = block
            if "目的地" in text:
                regions = rg_data_0[i][0]
                regions_dict = rg_data_0[i][1]
                y0 += regions_dict['目的地：'][1] - regions_dict['FBA:'][1] + config.destination_y0
                x0 += regions[2][0] - regions[0][0] + config.destination_y1
                y1 = y0 + (regions[1][1] - regions[-1][1])+1
                #print(f"{x0}, {y0}, {x1}, {y1}")
                # 绘制白色矩形覆盖原文本
                new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                #new_page.draw_rect([x0, y0, x1, y1], color=(0, 0, 0), fill=(0, 0, 0))
            if "发货地" in text:
                regions = rg_data_1[i][0]
                regions_dict = rg_data_1[i][1]
                y0 += regions[0][1] - regions[1][1] + config.address_y0
                y1 = y0 + (regions[1][1] - regions[-1][1]) + config.address_y1
                # 在该文本区域绘制一个黑色矩形覆盖
                #new_page.draw_rect([x0, y0, x1, y1], color=(0, 0, 0), fill=(0, 0, 0))
                new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                #import pdb;pdb.set_trace()
                pass
    # 将新文档保存为指定文件名
    new_doc.save(output_pdf)
    # 关闭文档
    doc.close()
    new_doc.close()
    fp.close()
    print(f"新文件已保存为: {output_pdf}")
    print(f"删除旧的pdf", input_pdf)
    if config.remove_file:
        try:
            os.remove(input_pdf)
            # 运行失败时清理没用的excel
            if os.path.exists(output_excel):
                os.remove(output_excel)
        except:
            pass
def set_main_pdf(input_pdf):
    # 输出的 PDF 文件名
    #input_pdf = glv['config']['账号路径'] + glv['h_title'] + "\\" + glv['h_title'] + "_temp.pdf"
    output_pdf = input_pdf.replace("_temp.pdf", ".pdf")

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
            if "目的地" in text:
                x0 += 12
                y0 += 10
                y1 = y0 + 8
                # 在该文本区域绘制一个黑色矩形覆盖
                #new_page.draw_rect([x0, y0, x1, y1], color=(0, 0, 0), fill=(0, 0, 0))
                new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                #import pdb;pdb.set_trace()
                pass
            if "发货地" in text:
                y0 += 10
                y1 = y0 + 8
                # 在该文本区域绘制一个黑色矩形覆盖
                #new_page.draw_rect([x0, y0, x1, y1], color=(0, 0, 0), fill=(0, 0, 0))
                new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                #import pdb;pdb.set_trace()
                pass
    # 将新文档保存为指定文件名
    new_doc.save(output_pdf)
    # 关闭文档
    doc.close()
    new_doc.close()
    print(f"新文件已保存为: {output_pdf}")
    print(f"删除旧的pdf", input_pdf)
    if config.remove_file:
        os.remove(input_pdf)
def set_sku_pdf(input_pdf):
    # 输入的 PDF 文件名
    #input_pdf = "PPDD46-black&brown-9x12_temp.pdf"
    pdf_dir = os.path.dirname(input_pdf)
    if not input_pdf.endswith("_temp.pdf"):
        print(input_pdf, "跳过")
        return ""
    sku = file_name=os.path.basename(input_pdf).split('_temp')[0]
    output_pdf = pdf_dir + "\\" + sku + ".pdf"
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
            # 检查文本是否包含 "新品"
            if "新品" in text:
                # 添加白色矩形覆盖
                y0 += (10 + config.sku_y0)
                y1 = y0 + 10
                new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))

                # 在白色区域内添加文本 "MADE IN CHINA" 和 "skuxxx"
                new_page.insert_text(
                    (x0, y0 + 8),  # 设置插入文本的位置
                    "MADE IN CHINA " + sku,
                    fontsize=8,       # 字体大小
                    color=(0, 0, 0),  # 黑色字体
                )
    
    # 将新文档保存为指定文件名
    new_doc.save(output_pdf)
    print(f"新文件已保存为: {output_pdf}")

    # 关闭文档
    doc.close()
    new_doc.close()
    if config.remove_file:
        os.remove(input_pdf)
import zipfile

def compress_folder_to_zip(folder_path):
    # 获取文件夹的绝对路径和名称
    folder_path = os.path.abspath(folder_path)
    folder_name = os.path.basename(folder_path)
    
    # 设置压缩文件路径
    zip_file_path = os.path.join(os.path.dirname(folder_path), f"{folder_name}.zip")
    
    # 创建压缩文件
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 添加文件到 zip 中，同时保持文件的相对路径
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    
    print(f"压缩完成: {zip_file_path}")
if __name__ == '__main__':
    config_path = "D:\\rpa.txt"
    with open(config_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        #print(html_content)
        json_data = json.loads(html_content)
        save_path = json_data["账号路径"]
    for d in os.listdir(save_path):
        if d != 'test' and config.test_mode:
            continue
        for code in os.listdir(save_path + "\\" + d):
            path = save_path + "\\" + d + "\\" + code
            if code.find("FBA") != 0 or code.endswith(".zip"):
                continue
            if not os.path.isdir(path):
                continue
            print(path)
            for header_dir in os.listdir(path):
                header_path = path + "\\" + header_dir
                for header_file in os.listdir(header_path):
                    if header_file.endswith("temp.pdf"):
                        try:
                            #print(header_path + "\\" + header_file)
                            reset_main_pdf_v2(header_path + "\\" + header_file)
                        except Exception as e:
                            traceback.print_exc()
                    if not os.path.exists(header_path + "\\商品标签"):
                        continue
                    for sku_pdf in os.listdir(header_path + "\\商品标签\\"):
                        if sku_pdf.endswith("temp.pdf"):
                            try:
                                pass
                                set_sku_pdf(header_path + "\\商品标签\\" + sku_pdf)
                                #print(header_path + "\\商品标签\\" + sku_pdf)
                            except Exception as e:
                                traceback.print_exc()
                                pass
            if not os.path.exists(path + ".zip"):
                compress_folder_to_zip(path)
                from feishu.feishu_uplaod import upload_file
                res_text = upload_file(path + ".zip")
                try:
                    upload_res = json.loads(res_text)
                    if upload_res['msg'] == "Success":
                        message = path + ".zip上传成功"
                        send_message(message)
                except:
                    send_message(path + ".zip上传失败:" + res_text)
