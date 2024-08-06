# 文件名称:E:\python Project\some thing no important\setup_python_library.py(中文意思为:源代码查询)
# 注释添加日期:2022-07-24 09:28:37.874742
# 编写工具:PyChame
# 编写目的:安装或者更新库
# -*- coding: utf-8 -*-

import os


def set_up():

    library = input("输入你要安装的库")
    os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple" + " " + library)


def up_date():
    library = input("输入你要更新的库")
    os.system("python -m pip install --upgrade" + " " + library)


a = input('请输入数字，下载请输入1，更新请输入2\n')

if a == '1':
    set_up()
elif a == '2':
    up_date()
