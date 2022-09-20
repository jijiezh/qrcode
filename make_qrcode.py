# coding:utf-8
import qrcode
import hashlib
import json
import math

debug_mode = False
qr = qrcode.QRCode(version=10,
                   # 二维码的纠错功能
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   # 二维码中每个小格子包含的像素
                   box_size=10,
                   # 边框包含的格子数，默认为4
                   border=4)


def make_qrcode_img_no_section(qr_data):
    hexdigits = hashlib.md5(qr_data.encode(encoding='UTF-8')).hexdigest()
    section = '1@1'
    generate_data = {'s': hexdigits, 'v': {
        'section': section, 'content': qr_data
    }, 'e': '0'}
    qr.clear()
    generate_result = json.dumps(generate_data, ensure_ascii=False)
    qr.add_data(generate_result)
    qr.make(fit=True)
    # 二维码的背景色和格子色
    img = qr.make_image(fill_color='black', back_color='white')
    file_name = hexdigits + '_' + section + '.png'
    img.save(file_name)
    if debug_mode:
        img.show()
    return [{"img_url": file_name, 'img_digits': hexdigits, 'img_content': generate_result}]


def make_qrcode_img(qr_data):
    default_max = len(qr_data) if (len(qr_data) < 500) else 500
    imgs = []
    msg_count = math.ceil(len(qr_data) / default_max)
    print("Messge count====>" + str(msg_count) + ";real length==" + str(default_max))
    if msg_count >= 1:
        for i in range(msg_count):
            section = str(i + 1) + '@' + str(msg_count)
            section_msg = qr_data[i * default_max:(i + 1) * default_max]

            print(section + "====" + section_msg)

            hexdigits = hashlib.md5(qr_data.encode(encoding='UTF-8')).hexdigest()
            generate_data = {'s': hexdigits, 'v': {
                'section': section, 'content': section_msg
            }, 'e': '0'}
            qr.clear()
            generate_result = json.dumps(generate_data, ensure_ascii=False)
            qr.add_data(generate_result)
            qr.make(fit=True)
            # 二维码的背景色和格子色
            img = qr.make_image(fill_color='black', back_color='white')
            file_name = hexdigits + '_' + section + '.png'
            img.save(file_name)
            if debug_mode:
                img.show()
            imgs.append({"img_url": file_name, 'img_digits': hexdigits, 'img_content': generate_result})
    return imgs


if __name__ == '__main__':
    data = 'Python中的条件表达式在其他编程语言中也称之为三元运算符，在C#和JAVA中都有三元运算符，Python中的条件表达式是基于真（true）假（false）的条件进行判断的，或者说三元运算符在操作的过程中使用了三个元素如：分析：首先判断if后面的10是否大于20，如果大于则返回前面条件为True的结果为10，如果判断的结果为False则返回后面else条件为假的结果20，所以这段伪代码的结果如图：num01 = 10 if10 > 20 else20print(num01)实例01通过Python的条件表达式判断用户输入的用户名和密码是否正确，如果正确返回“欢迎登录！”如果用户名或者密码有一个输入错误就显示“用户名或密码输入错误！”print("num01大于num02"ifnum01 > num02 else"num01小于num02")首先使用的eval函数来输入两个不相等的数字，eval 只能一次输入多个数字（其实是字符串），然后把输入的数字自动转换为int类型；然后判断num01是否大于num02，如果大于，判断的结果为True就返回"num01大于num02"，如果num01小于num02，判断结果为False就返回"num01小于num02"'
    make_qrcode_img(data)
