# 文件名称:Function passing reference.py
# 注释添加日期:2022-07-23 23:08:35.194335
# 编写工具:PyChame
# 编写目的:添加程序信息
# -*- coding: utf-8 -*-
from datetime import datetime

if __name__ == "__main__":
    try:
        now = str(datetime.now())
        file = input("input the file name or input the file way")
        goal = input("input your goal")
        Target_file = open(file, "r", encoding='utf-8', errors='ignore')
        Intermediator = Target_file.read()
        Target_file.close()
        information = "# 文件名称:" + file + "(中文意思为:源代码查询)\n\
# 注释添加日期:" + now + "\n\
# 编写工具:PyChame\n\
# 编写目的:" + goal + "\n\
# -*- coding: utf-8 -*-\n"
        Intermediator = information + Intermediator
        Target_file = open(file, "w", encoding='utf-8', errors='ignore')
        Target_file.write(Intermediator)
        Target_file.close()
    except Exception as error:
        print("没有这个文件")
        print(error)
