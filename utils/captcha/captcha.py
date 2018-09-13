# coding=utf-8
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont
from io import StringIO,BytesIO
from string import printable


def create_captcha():
    font_path = "utils/captcha/font/Arial.ttf"
    font_color = (randint(150, 200), randint(0, 150), randint(0, 150))
    line_color = (randint(0, 150), randint(0, 150), randint(150, 200))
    point_color = (randint(0, 150), randint(50, 150), randint(150, 200))
    width, height = 100, 40

    #画布
    image = Image.new('RGB', (width, height), (200, 200, 200))
    #画笔
    draw = ImageDraw.Draw(image)
    #字体
    font = ImageFont.truetype(font_path, height - 10)

    # 生成4位验证码
    text = ''.join([choice(printable[:62]) for i in range(4)])
    # 把验证码写到画布上
    draw.text((10, 10), text, font=font, fill=font_color)
    # 绘制线条
    for i in range(0, 5):
        draw.line(((randint(0, width), randint(0, height)),
                   (randint(0, width), randint(0, height))),
                  fill=line_color, width=2)
    # 绘制点
    for i in range(randint(100, 1000)):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)
    # 输出
    # image不是一个HttpResponse可以识别的对象
    # 因此我们需要将image变成一个数据流才能放到HttpResponse上
    out = BytesIO() #BytesIO：相当于一个管道，可以用来存储字节流的
    image.save(out, format='jpeg')
    content = out.getvalue()
    out.close()

    print('图型验证码', text)
    return text, content
