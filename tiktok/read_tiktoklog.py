# 读取D:\tiktok_log 文件夹下的所有文件,取出日期最新的一个文件夹
import os
path = r'D:\\tiktok_log'
filelist =[p for p in os.listdir(path) if os.path.isdir(os.path.join(path, p))]
filelist.sort()
recheck_list = []
for png in os.listdir(path + "\\" + filelist[-1]):
    if not png.startswith("评论"):
        continue
    ym_png = png.replace("评论", "要码")
    if not os.path.exists(path + "\\" + filelist[-1] + "\\" + ym_png):
        url = png.replace("评论_", "https://").replace("_", "/").replace(".png", "")
        recheck_list.append(url)
reset_file = "d://tiktok_link.csv"
lines = []
print(len(recheck_list))
# for line in open(reset_file, encoding="utf-8"):
#     line = line.strip()
#     if line in recheck_list:
#         print(line)
#         continue
#     lines.append(line)
# open(reset_file, 'w', encoding="utf-8").write("\n".join(lines))
