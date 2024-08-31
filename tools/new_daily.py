import os

year = '2024'
months = '08'
data = input('输入日期')
if int(data) < 10:
    data = '0' + data
file_path = "{year}-{months}-{data}.md".format(year=year, months=months, data=data)
if not os.path.exists(file_path):
    open(file_path, "w").close()
    print(f"文件 {file_path} 创建成功")
else:
    print(f"文件 {file_path} 已存在")