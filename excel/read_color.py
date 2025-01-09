import pandas as pd

if __name__ == '__main__':

    df = pd.read_excel('24年TOP300上传.xlsx')
    colors = []
    for i in range(len(df)):
        color = df.loc[i, 'SKU']
        if "Color: " not in color:
            continue
        color = color.split("Color: ")[-1]
        color = color.split("|")[0].strip()
        color_brack = color
        color = color.replace(" ", "")
        #color = color.replace("", "")
        if color not in colors:
            colors.append(color)
            print(i, color, color_brack)
    import pdb;pdb.set_trace()
    pass
