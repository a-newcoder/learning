# 文件名称：try
# 注释添加日期：2022.11.29
# 编写工具：pycheme
# 编写目的：尝试学习bottle库
# -*- coding: utf-8 -*-


from bottle import route,run
@route('/')
def index():
    f="abc"
    return f
run(host = 'localhost', port = 80)