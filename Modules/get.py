# encoding:utf-8

'''
————————————————————————————————
get.py
获取句子迷 的句子页，获取源码，解析，分析出句子。
对句子进行字数判断，多于120字不取。
取完句子后与 /data/allhistory.txt 比对，删除取过的句子。
保存今日新抓取句子为 /data/sentenceget.txt ，以备GUI引用。
————————————————————————————————
'''

import os
import random
import requests
import codecs
from bs4 import BeautifulSoup
import re
import json

where_script = os.path.split(os.path.realpath(__file__))[0]
# print(where_script)
where_rootmenu = where_script[:where_script.rfind('\\')]
# print(where_rootmenu)


def juzimi():

    user_agaents = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
        'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14']

    url = 'http://m.juzimi.com/hotfamsen/?mobver=1'
    headers= {"User-Agent": random.choice(user_agaents)}
      # 严肃：安全起见加了一段对user_agent的切换
    s = requests.session()
    response = s.post(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'  # 修改编码为utf-8
    r = response.text
    soup = BeautifulSoup(r, 'html.parser')
    alltext = soup.get_text()
    # alltext = "".join(alltext.split())
    alltext = alltext.strip()
    alltext = alltext.split('\n')
    # 此处的alltext并不是取得的句子，还包括没用的网页信息。

    allhistoryfile = codecs.open(where_rootmenu + '/data/allhistory.txt', 'r', 'utf-8')
    allhistory = []
    for line in allhistoryfile:
        line = line.replace('\r','')
        line = line.replace('\n','')
        line = line.replace('\r\n','')
        line = line.replace('\ufeff','')
        allhistory.append(line)
    allhistoryfile.close()
    #for line in allhistory:
    #    print(line)
    # print(allhistory)
    # 获取以前取过的句子

    sentences = []
    for line in alltext:
        line = line.replace('\r','')
        line = line.replace('\n', '')
        line = line.replace('\r\n', '')
        line = line.replace(' ', '') # 进一步消灭无用信息
        if line.find('喜欢(') != -1:  # 处理alltext，判断有无句子（自己看url的网页源码）
            line = line[:line.find('喜欢(')]
            # line = re.sub('[a-zA-Z]', '', line)
            pattern = re.compile('[a-zA-Z]')
            match = pattern.match(line)
            if not match :
                if line.find('（全文）') != -1:
                    line = line[:line.find('（全文）')]
                if len(line) <= 100:  # 判断长度
                    if line.find('——') != -1:
                        if line in allhistory:  # 删除已经取过的
                            pass
                        else:
                            sentences.append(line)
                            print(line)



    for sentence in sentences:
        print(sentence)

    if sentences == []:
        print('Errrr...We got nothing.')
        exit(1)
    else:
        pass
    # 检查。以免句子为空。

    f = codecs.open(where_rootmenu + '/data/sentenceget.txt', 'wb+','utf-8')
    f.close()
    # 清除上次历史记录

    f = codecs.open(where_rootmenu + '/data/sentenceget.txt', 'ab+', 'utf-8')
    for sentence in sentences:
        f.write(sentence + '\r\n')  # 此处是照顾windows换行符。所以在GUI最后发布时，要去掉两个字符，就是这俩。
    f.close()
    # 保存取得的句子，GUI界面好引用

    f = open(where_rootmenu + '/data/sentenceget.txt', 'r')
    if f == '':
        print('Save Wrong!')
        exit(1)
    else:
        pass
    # 检查。以免保存失败。'''
    print('句子迷getdone!')

    return

def zuowennote():


    user_agaents = [
        'CompositionNote/2.2 (iPhone;iOS 10.3.3; Scale/2.00)',
        'CompositionNote/2.2 (iPad;iOS 10.3.3; Scale/2.00)',
        'CompositionNote/2.2 (iPhone;iOS 10.3.2; Scale/2.00)',
        'CompositionNote/2.2 (iPhone;iOS 10.3.1; Scale/2.00)']

    url = 'http://zhitiao.gaokaowenwen.com/v_2_0/composition/article/list'
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-Hans-CN;q=1, en-CN;q=0.9, ja-JP;q=0.8",
        "Connection":"keep-alive",
        "Contene-Length":'2',
        "Conent-Type":"application/json",
        "Host":"zhitiao.gaokaowenwen.com",
        "Proxy-Connection":"keep-alive",
        "User-Agent": random.choice(user_agaents)}
    # 严肃：安全起见加了一段对user_agent的切换
    s = requests.session()
    response = s.post(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'  # 修改编码为utf-8
    r = response.text
    jsonall = json.loads(r)["data"]
    for sentence in jsonall:
        sentence["title"] = sentence["title"].replace('|','')
    todaysentence = jsonall[-3:]
    f = codecs.open(where_rootmenu + '/data/zuowennote_get.json', 'w', 'utf-8')
    json.dump(todaysentence, f, indent=4, ensure_ascii=False)
    f.close()
    f = codecs.open(where_rootmenu + '/cache/zuowennote.json', 'w', 'utf-8')
    json.dump(jsonall, f, indent=4, ensure_ascii=False)
    f.close()
    print('作文纸条保存完毕!')
    return


f = open(where_rootmenu + '/data/setting.json', 'r')
setting_json = json.load(f)
f.close()

if setting_json["mode"] == 'juzimi':
    juzimi()
elif setting_json["mode"] == 'zuowennote':
    zuowennote()
else:
    print('配置错误')
    exit(1)


