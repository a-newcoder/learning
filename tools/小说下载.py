import re
import requests
from lxml import etree
import time
from os import remove
import aiofiles
from aiohttp import ClientSession, ClientTimeout
import asyncio
from colorama import init
from json import loads


def len_str(string):
    count = 0
    for ch in string:
        if ch >= '\u007f':
            count += 1
    return count


def width(string, length):
    return length - len_str(string)


cookies = {}

headers = {
    'authority': 'www.bige3.cc',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'cache-control': 'no-cache', # Requests sorts cookies= alphabetically
    'pragma': 'no-cache', 'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"', 'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
}
headers1 = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; TAS-AN00 Build/HUAWEITAS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.61 Mobile Safari/537.36 Super 4.6.5"
}

# 获取小说书名、目录、章节链接
def get_title(url):
    try:
        response1 = requests.get(url, cookies = cookies, headers = headers)
        html1 = etree.HTML(response1.text, parser = etree.HTMLParser(encoding = 'utf-8'))
        chapter_name1 = html1.xpath('/html/body/div[5]/dl/dd/a/text()')
        chapter_name2 = html1.xpath('/html/body/div[5]/dl/span/dd/a/text()')
        chapter_url1 = html1.xpath('/html/body/div[5]/dl/dd/a/@href')
        chapter_url2 = html1.xpath('/html/body/div[5]/dl/span/dd/a/@href')
        chapter_names = chapter_name1[0:10] + chapter_name2 + chapter_name1[-10:]
        chapter_urls = chapter_url1[0:10] + chapter_url2 + chapter_url1[-10:]  # 拼接完整章节目录和链接
        novel = html1.xpath('/html/body/div[4]/div[2]/h1/text()')  # 获取小说书名
        return chapter_names, chapter_urls, novel
    except Exception as e:
        print(f'\033[31m获取小说书名出错，出错原因\033[0m：{e}')
        return [], [], ['error']


# 单章小说内容下载
async def singe_chapter(url1, name1, sem):
    new_url = f"https://www.bige3.cc{url1}"  # 拼接章节网址
    i = 0
    async with sem:
        while True:
            i += 1
            try:
                timeout = ClientTimeout(total = 10)
                async with ClientSession(headers = headers, cookies = cookies, timeout = timeout) as session:
                    async with session.get(new_url) as resp:
                        html2 = etree.HTML(await resp.text(), parser = etree.HTMLParser(encoding = 'utf-8'))
                        singe_content = html2.xpath('//*[@id="chaptercontent"]/text()')  # 获取小说章节内容
                        result = re.findall(r'第(.*?)章', singe_content[0])
                        if len(result):
                            del singe_content[0]  # 去除可能出现的重复标题
                        content = singe_content[0:-2]  # 去除网站附带的广告链接
                        name2 = strinfo.sub('_', name1)  # 去除小说章节书名中的特殊字符，避免生成章节文件时出错
                        async with aiofiles.open(f"./小说/{name2}.txt", "w", encoding = "utf-8") as f:  # 在小说目录下创建临时的单章txt
                            await f.write(name2 + '\r\r\r')
                            for lists in content:
                                await f.write(lists + '\r\r')
                        name2_width = 60 - len_str(name2)
                        print(f'{name2:<{name2_width}}finish')
                        break  # await asyncio.sleep(random.uniform(1, 1.5))                           # 想要更快可以直接注释
            except:
                print(f'{name1}                               false        {i}/5')
                if i >= 5:
                    break  # await asyncio.sleep(random.uniform(1, 1.5))


# 创建异步任务
async def create_tasks(name_chapter, url_chapter, lens):
    tasks = []
    if lens > 1000:
        sema = 1000
    else:
        sema = lens
    sem = asyncio.Semaphore(sema)  # 设置同时进行的异步数量，可以根据上面自行设定，数量越大，下载越快
    for url4, name3 in zip(url_chapter, name_chapter):
        tasks.append(asyncio.create_task(singe_chapter(url4, name3, sem)))  # 创建任务
    await asyncio.gather(*tasks)


def start_download(url):
    chapter_name, chapter_url, novel_name = get_title(f'https://www.bige3.cc{url}')  # 获取小说目录，对应的网页链接，书名
    length = len(chapter_name)
    if length:
        print(f"\033[31m《{novel_name[0]}》共{length}章, 开始下载！！\033[0m\n\n")
        new_chapter_name = chapter_name[0: length]
        new_chapter_url = chapter_url[0: length]  # 该处可以更改想要下载的范围，可以在前面创建一个input修改这个范围
        time1 = time.time()
        loop.run_until_complete(create_tasks(new_chapter_name, new_chapter_url, length))  # 提交任务
        time2 = time.time()
        with open(f'./小说/{novel_name[0]}.txt', 'w', encoding = 'utf-8') as f1:  # 将分散的小说章节写入一个{书名}.txt中
            for chapter_names in new_chapter_name:
                chapter_name2 = strinfo.sub("_", chapter_names)
                try:
                    with open(f'./小说/{chapter_name2}.txt', 'r', encoding = 'utf-8') as f2:
                        text1 = f2.read()
                        f1.write(text1)
                    remove(f"./小说/{chapter_name2}.txt")  # 移除已写入{书名}.txt的临时章节
                except:
                    print(f'{chapter_names}  false')
            print('==============================下载完成==============================\n')
        print(f'共耗时：\033[33m{time2 - time1:.2f}s\033[0m\n\n')
        print(f'\033[32m《{novel_name[0]}》已下载！！！！\033[0m\n\n\n')
    else:
        print('error')


async def fanqie_singe_chapter(id, sem):
    if len(id):
        new_url = 'https://novel.snssdk.com/api/novel/book/reader/full/v1'# 拼接章节网址
        data = {
            'device_platform': 'android',
            'parent_enterfrom': 'novel_channel_search.tab.',
            'aid': '2329',
            'platform_id': '1',
            'group_id': str(id),
            'item_id': str(id)
        }
        i = 0
        async with sem:
            while True:
                i += 1
                try:
                    timeout = ClientTimeout(total = 5)
                    async with ClientSession(headers = headers1, timeout = timeout) as session:
                        async with session.get(new_url, params=data) as resp:
                            json = await resp.json()
                            data = json['data']['content']
                            html2 = etree.HTML(data, parser = etree.HTMLParser(encoding = 'utf-8'))
                            singe_content = html2.xpath('//article/p/text()')  # 获取小说章节内容
                            name2 = json['data']['novel_data']['chapter_title']
                            async with aiofiles.open(f"./小说/{id}.txt", "w", encoding = "utf-8") as f:  # 在小说目录下创建临时的单章txt
                                await f.write(name2 + '\r\r\r')
                                for lists in singe_content:
                                    await f.write('    ' + lists + '\r\r')
                            name2_width = 60 - len_str(name2)
                            print(f'{name2:<{name2_width}}finish')
                            break
                except Exception as e:
                    print(f'{id}     false      {i}/5')
                    if i >= 10:
                        break


# 创建异步任务
async def fanqie_create_tasks(ids, lens):
    tasks = []
    if lens > 1000:
        sema = 1000
    else:
        sema = lens
    sem = asyncio.Semaphore(sema)  # 设置同时进行的异步数量，可以根据上面自行设定，数量越大，下载越快
    for id in ids:
        tasks.append(asyncio.create_task(fanqie_singe_chapter(id, sem)))  # 创建任务
    await asyncio.gather(*tasks)


def fanqie_download(book_id):
    if book_id.isdigit():
        time1 = time.time()
        try:
            resp = requests.get(f'https://fanqienovel.com/page/{book_id}', headers = headers1)
        except Exception as e:
            print('章节页面请求错误！！')
            return 0
        json1 = loads(re.findall('window.__INITIAL_STATE__=(.*?);', resp.text)[0])['page']
        item_ids = json1['itemIds']
        novel_name = json1['bookName']
        novel_author = json1['author']
        if not novel_name:
            print('该书不是正常书籍状态，可能书籍更换了书籍号或者出现了其他原因，内容无法保证正确，请尽量检索完整的小说书名！！')
            novel_name = '异常书籍' + str(book_id)
        else:
            novel_name = novel_name + '-' + novel_author
        if len(item_ids):
            print(f"\033[31m《{novel_name}》({book_id})共{len(item_ids)}章, 开始下载！！\033[0m\n\n")
            item_ids.reverse()
            loop.run_until_complete(fanqie_create_tasks(item_ids, len(item_ids)))  # 提交任务
            time2 = time.time()
            with open(f'./小说/{novel_name}.txt', 'w', encoding = 'utf-8') as f1:  # 将分散的小说章节写入一个{书名}.txt中
                for id in item_ids:
                    try:
                        with open(f'./小说/{id}.txt', 'r', encoding = 'utf-8') as f2:
                            text1 = f2.read()
                            f1.write(text1)
                        remove(f"./小说/{id}.txt")  # 移除已写入{书名}.txt的临时章节
                    except:
                        print(f'{id}  false')
                print('==============================下载完成==============================\n')
            print(f'共耗时：\033[33m{time2 - time1:.2f}s\033[0m\n\n')
            print(f'\033[32m《{novel_name}》已下载！！！！\033[0m\n\n\n')
        else:
            print('\033[31m请输入有效的书籍ID\033[0m\n')
    else:
        print('\033[31m请输入纯数字的书籍ID！！！！\033[0m')


if __name__ == '__main__':
    # get_title('https://www.bige3.cc/book/66/')
    init(autoreset = True)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    strinfo = re.compile('[/:*?"<>|\\\\]')  # 匹配字符串中特殊的字符
    a = input('笔趣阁本地搜索：    1\n笔趣阁链接下载：    2\n番茄小说ID下载：    3 \n番茄小说搜索下载：  4 \n请选择：')
    if a == '1':
        with open('./小说/all_books.txt', 'r', encoding = 'utf-8') as f:
            books = f.read()
        books = eval(books)
        while True:
            k = 1
            target = []
            a = input('本地搜索已启动:')
            for dic in books:
                result = re.findall(f'{a}', dic[0] + dic[1])
                if len(result):
                    target.append(dic)
                    width1 = 60 - len_str(dic[0])
                    width2 = 40 - len_str(dic[1])
                    print(f'{k:<4}{dic[0]:^{width1}}{dic[1]:<{width2}}')
                    k = k + 1
                    if k > 100:
                        break
            if len(target) == 0:
                print('小说不存在，请重新输入')
                continue
            b = input('请输入序号(重新搜索请输入0, 全部下载请输入101)：')
            if b == '0':
                continue
            elif b == '101':
                for book in target:
                    start_download(book[2])
                    time.sleep(0.5)
            else:
                start_download(target[int(b) - 1][2])
    elif a == '2':
        print('\n请到 \033[32mhttps://www.bige3.cc\033[0m 网站搜索你想下的小说，并获取相应的的书籍链接\n链接格式为:/book/34454/\n')
        while True:
            book_url = input('请输入书籍链接(格式：/book/书籍id/):')
            start_download(book_url)
    elif a == '3':
        print('\n\033[31m注意\033[0m：下载番茄小说的小说，需要自行获取书籍的id，可以通过网页搜索的方式获取\n      就是书籍章节页面url后面那一串数字，输入那一串数字即可\n')
        while True:
            bookid = input('请输入番茄小说ID(批量下载请用空格分割)：')
            if bookid:
                for id in bookid.split(' '):
                    fanqie_download(id)
                    time.sleep(0.5)
    elif a == '4':
        print('\n\033[31m番茄小说搜索下载功能\033[0m：尽量检索完整小说书名，可能会出现正常网页检索不出的书籍，请注意甄别')
        while True:
            search_name = input('请输入书名或者作者名进行搜索：')
            book_id, num = [], 0
            for i in range(3):
                new_url = f'https://novel.snssdk.com/api/novel/channel/homepage/search/search/v1/?device_platform=android&parent_enterfrom=novel_channel_search.tab&aid=1967&offset={i * 10}&q={search_name}'  # 拼接章节网址
                resp = requests.get(url = new_url, headers = headers1).json()
                for index, book in enumerate(resp['data']['ret_data']):
                    book_id.append(book['book_id'])
                    title = book['title']
                    author = book['author']
                    num += 1
                    print(f'{num:<4}{title:^{width(title, 60)}}{author:<{width(author, 40)}}')
                if not resp['data']['has_more']:
                    break
            choose = input('请输入书籍序号，输入\033[32m0\033[0m重新搜索(批量下载请用空格分割序号)：')
            choose_list = choose.split(' ')
            for ids in choose_list:
                if ids.isdigit():
                    if int(ids) <= len(book_id):
                        if int(ids):
                            fanqie_download(book_id[int(ids)-1])
                            time.sleep(0.5)
                        else:
                            continue
                    else:
                        print('\033[31m序号超出范围，请重新搜索！！\033[0m')
                else:
                    print('\033[31m请输入正确格式的书籍序号！！！！\033[0m')

