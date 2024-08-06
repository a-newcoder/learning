# 文件名称:E:\python Project\Performance test and other test documents\Source code query.py
# 注释添加日期:2022-07-23 23:07:24.589843
# 编写工具:PyChame
# 编写目的:查询某函数的源代码
# -*- coding: utf-8 -*-
from inspect import getsource

#程序入口
if __name__ == "__main__":
    print(getsource())
