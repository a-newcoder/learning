# 文件名称:E:\python Project\py skill files\Function passing reference.py
# 注释添加日期:2022.7.23
# 编写工具:PyChame
# 编写目的:装饰器技巧训练
# -*- coding: utf-8 -*-
import datetime
from time import time
def timer(func):
    def f(*args,**kwargs):
        before = time()
        rv = func(*args,**kwargs)
        after = time()
        print('time taken:', after - before)

        return rv

    return f


@timer
def add(x, y=10):
    return x + y


@timer
def sub(x, y=10):
    return x - y

print('add(10)', add(10))
print('add(20.30)', add(20, 30))
print('add("a","b")', add("a", "b"))
print('sub(10)', sub(10))
print('sub(20,30)', sub(20, 30))
now=datetime.datetime.now()
print(now)

