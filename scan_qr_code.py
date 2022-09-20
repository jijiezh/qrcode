from collections.abc import Iterable

import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np
import json
import send_wechat_corp_msg as sender


def img_resize(image):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架 640x369 1280×720 1920×1080
    width_new = 1280
    height_new = 720
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    return img_new


def video_cv2(path=0):
    capture = cv2.VideoCapture(path)

    while True:
        if capture.isOpened():
            is_opened, frame = capture.read()
            if not (is_opened):
                video_cv2(path)
            else:
                img = decode_zbar(frame)
                cv2.imshow("camera", img_resize(frame))
        else:
            video_cv2(path)

        if cv2.waitKey(30) & 0xff == 27:
            break
    capture.release()
    cv2.destroyAllWindows()

s_cache = []
def decode_zbar(frame):
    barcodes = pyzbar.decode(frame, symbols=[pyzbar.ZBarSymbol.QRCODE])
    target = ''
    if isinstance(barcodes, Iterable):
        for barcode in barcodes:
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # 条形码数据为字节对象，所以如果我们想在输出图像上画出来， v`需要先将它转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            if (isinstance(frame, np.ndarray)):  # 判断是否OpenCV图片类型
                frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            draw = ImageDraw.Draw(frame)
            # 字体的格式
            fontStyle = ImageFont.truetype("simsun.ttc", 12, encoding="utf-8")
            # 绘出图像上条形码的数据和条形码类型
            text = "{} ({})".format(barcodeData, barcodeType)
            draw.text((x, y - 15), text, (0, 0, 125), font=fontStyle)

            # cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            #             .5, (0, 0, 125), 2)
            barcode_json = json.loads(barcodeData)
            signature = barcode_json['s']
            if not (signature in s_cache):
                print()
                s_cache.insert(0, signature)
                if len(s_cache) > 100:
                    s_cache.pop(-1)
            # if not operator.contains(target, barcodeData):
            #     target += barcodeData
                sender.send_msg(barcode_json['v'])
            # 向终端打印条形码数据和条形码类型
            print("[INFO] Found {} Content: {}".format(
                barcodeType, barcodeData))
            frame = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)
    return frame


# 读取照片
def decode_zbar_img(img_path):
    if not os.path.exists(img_path):
        raise FileExistsError(img_path)
    return pyzbar.decode(Image.open(img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])


# 识别二维码照片-----广场项目
if __name__ == '__main__':
    print(decode_zbar_img(
        "d:/PreSearch/pyhikvision/example/camera/qrcode/test2.png")[0].data)
    vpath = 'rtsp://admin:a1234567@10.9.97.98:554/Streaming/Channels/101'
    video_cv2(vpath)
