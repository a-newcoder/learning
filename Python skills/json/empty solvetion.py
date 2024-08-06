import json

"""验证用户,若为新用户则储存新用户名"""


def greet_user():
    """问候"""
    try:
        with open('username.json') as f_obj:
            user_old = json.load(f_obj)

    except json.decoder.JSONDecodeError  or IOError:
        """文件如果空时会出错"""
        get_new_username()

    else:
        print("Your name is " + user_old)
        answer = input()

        if answer.lower() == 'y':
            print('Hello ' + user_old)
        else:
            get_new_username()


def get_new_username():
    """获取新的用户名"""
    with open('username.json', 'w') as f_obj:
        nam = input("Your name: ")
        json.dump(nam, f_obj)


greet_user()
