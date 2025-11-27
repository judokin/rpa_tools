import pandas as pd
import os
# C:\Users\Administrator\Desktop\Super Browser\亚马逊-北蓉-北美（子账号）\FBA18VBT9P7G_v2
try:
   import pymupdf as fitz  # PyMuPDF
except:
    import fitz
if os.path.exists("dev_config.py"):
    import dev_config as config
else:
    import config
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
def set_sku_pdf_v4(input_pdf):
    # 输入的 PDF 文件名
    #input_pdf = "PPDD46-black&brown-9x12_temp.pdf"
    pdf_dir = os.path.dirname(input_pdf)
    if not input_pdf.endswith("_temp.pdf"):
        print(input_pdf, "跳过")
        new_name = input_pdf.replace(".pdf", "_temp.pdf")
        os.rename(input_pdf, new_name)
        input_pdf = new_name

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
        for index, block in enumerate(blocks):
            x0, y0, x1, y1, text, _, _ = block
            print(index, text)
            if 1 == index:
                #import pdb;pdb.set_trace()
                font_num = new_page.insert_font(fontfile="D:\\rpa_tools\\华文宋体.ttf")
                # font_path = 'D:\\rpa_tools\\华文宋体.ttf'  # 你自己的字体路径
                # font = new_page.insert_font(
                #     fontfile=font_path,
                # )
                # 添加白色矩形覆盖
                y0 += (config.sku_y0)
                y1 = y0 + 10
                x1 = x1 + 50
                new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                new_page.add_redact_annot(
                    [x0, y0, x1, y1],
                    fill=(1, 1, 1)
                )
                new_page.apply_redactions()
                # 在白色区域内添加文本 "MADE IN CHINA" 和 "skuxxx"
                # new_page.insert_text(
                #     (x0, y0 + 8),  # 设置插入文本的位置
                #     text.replace(" Rugs ", " Mats "),
                #     fontsize=7,       # 字体大小
                #     color=(1, 1, 1),  # 黑色字体
                #     fontname="Times-Roman",
                # )
                
                text = text.replace("Rugs", " Mats ")
                text = text.replace("Rug", " Mat ")
                fontsize = 7
                color = (0, 0, 0)  # 白色字体
                fontname = "Times-Roman"

                # 创建 Shape 对象
                shape = new_page.new_shape()
                fixpoint = fitz.Point(x0, y0 + 8)
                matrix = fitz.Matrix(0.8, 1)   # 横向缩 0.8x，纵向不变
                # 插入带缩放的文本
                shape.insert_text(
                    (x0, y0 + 8),  # 插入位置
                    text,
                    fontsize=fontsize,
                    color=color,
                    fontname=fontname,
                    render_mode=0,   # 填充模式（正常文字）
                    morph=(fixpoint, matrix)   #  注意这里是 (Point, Matrix)
                )

                # 应用绘制到页面
                shape.commit()
                                
                
                # x = x0
                # y = y0 + 8
                # letter_spacing = -0.5
                # for ch in text.replace(" Rugs ", " Mats "):
                #     new_page.insert_text(
                #         (x, y),
                #         ch,
                #         fontsize=6,
                #         color=(1, 1, 1),
                #         fontname="Times-Roman",
                #     )
                #     # 计算下一个字的起点位置
                #     #w = new_page.get_text_length(ch, fontsize=7, fontname="Times-Roman")
                #     w = fitz.get_text_length(
                #         ch,
                #         fontname="Times-Roman",
                #         fontsize=7
                #     )
                #     x += w + letter_spacing
                
                
                # rect = fitz.Rect(x0, y0, x0 + 50, y0 + 10) 
                # new_page.insert_textbox(
                #     rect,
                #     text.replace(" Rugs ", " Mats "),
                #     fontname="Times-Roman",
                #     fontsize=9,
                #     color=(1, 1, 1),
                #     align=0,     # 左对齐
                # )
            # 检查文本是否包含 "新品"
            if "新品" in text:
                # 添加白色矩形覆盖
                y0 += (10 + config.sku_y0)
                y1 = y0 + 10
                #new_page.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                new_page.add_redact_annot(
                    [x0, y0, x1, y1],
                    fill=(1, 1, 1)
                )
                new_page.apply_redactions()
                # 在白色区域内添加文本 "MADE IN CHINA" 和 "skuxxx"
                sku_str = "NEW MADE IN CHINA " + sku
                new_page.insert_text(
                    (x0, y0 + 8),  # 设置插入文本的位置
                    sku_str[0:30],
                    fontsize=8,       # 字体大小
                    color=(0, 0, 0),  # 黑色字体
                )
                if len(sku_str) > 30 and not os.path.exists("d://set.txt"):
                    open("d://set.txt", "w").write("")
                    new_page.insert_text(
                        (x0, y0 + 20),  # 设置插入文本的位置
                        sku_str[30:],
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
        print(f"删除旧的pdf", input_pdf)
        os.remove(input_pdf)
def read_products_pdf(dir_path):
    sku2fnsku = {}
    excel_file_name_list = []
    pdf_full_name_list = []
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
            #pdf_name = pdf_name.replace(".pdf", "")
            print(f"{pdf_full_name} {fn_skuname}")
            pdf_full_name_list.append(pdf_full_name)
            sku2fnsku[pdf_name] = fn_skuname
    return pdf_full_name_list
def run(dir_path):
    pdf_full_name_list = read_products_pdf(dir_path)
    for pdf_file_name in pdf_full_name_list:
        print("reading ", pdf_file_name)
        set_sku_pdf_v4(pdf_file_name)

if __name__ == '__main__':
    dir_path = r'E:\360MoveData\Users\Administrator\Desktop\Super Browser\亚马逊--冬豚（子账号）\FBA19431MGBZ'
    run(dir_path)

    