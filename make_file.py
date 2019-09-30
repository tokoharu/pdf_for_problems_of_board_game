"""
主にhaisaresu氏の詰連珠をPDF化させるために作成。
具体的なパスは自分の環境に合わせて直書きする必要がある。
参考
- https://qiita.com/meznat/items/31d947ed4826350fd9fa
- PILの参考ページ
"""

import os

import img2pdf
from pathlib import Path
from PIL import Image


def calc_center(width, height, image):
    w, h = image.size
    position = (width//2 - w//2, height//2 - h//2)
    print(position)
    return position


def ImageToPdf(outputpath, imagepath):
    '''
    outputpath: pathlib.Path()
    imagepath: pathlib.Path()
    '''

    lists = list(imagepath.glob("**/*"))  # 単フォルダ内を検索
    print(outputpath, imagepath)
    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    imgpath_str = str(imagepath)
    # Pathlib.WindowsPath()をstring型に変換しないとエラー
    files = [str(i) for i in lists if i.match("*.jpg") or i.match("*.png")]
    imgdata = [Image.open(img) for img in files]
    print(len(imgdata))
    imgs = []  # 最終的な画像のファイル名。中間ファイル。
    cur = 0

    while True:
        width = 400  # 1問の最大サイズ程度に
        height = 500  # 1問の最大サイズ程度に
        # ベースとなる画像の定義
        img = Image.new('RGB', size=(width * 3, height * 3), color="white")
        # 3x3につなげる。
        for i in range(3):
            for j in range(3):
                if cur >= len(imgdata):
                    continue
                img_read = imgdata[cur]
                w, h = calc_center(width, height, img_read)
                img.paste(img_read, (i * width + w, j * height + h))
                cur += 1
        filename = imgpath_str + os.sep + "tmp_{}.png".format(cur)
        print(filename)
        img.save(filename)
        imgs.append(filename)
        if cur >= len(imgdata):
            break

    data = img2pdf.convert(
        imgs,
        layout_fun=layout_fun
    )
    # 書き込み
    with open(outputpath, "wb") as f:
        f.write(data)
    print(outputpath.name + " :Done")
    # 中間ファイルを消す
    for filename in imgs:
        print("remove : ", filename)
        os.remove(filename)


def main():
    # 作業フォルダ
    base_path = "./../../Users/tokoharu/Pictures".replace("/", os.sep)

    # 作業フォルダ内のディレクトリだけを抽出する
    glob = Path(base_path).glob("*")
    # print(glob)
    glob_list = list(glob)
    imagefolderlist = list([item for item in glob_list if item.is_dir()])
    # outputpathに指定ディレクトリと同名を指定する
    outputpathlist = list(
        [item.with_name(item.name + ".pdf")
         for item in imagefolderlist])
    # それぞれのディレクトリに対して作る。
    for outputpath, imagepath in zip(outputpathlist, imagefolderlist):
        # "haisaresu"と書かれているディレクトリのみに作業場所を限定する。
        if imagepath.name.find("haisaresu") < 0:
            continue
        try:
            ImageToPdf(outputpath, imagepath)
        except:
            pass


main()
