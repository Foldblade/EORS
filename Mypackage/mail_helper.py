# encoding:utf-8

import json
import codecs
import time
import os
import sys
import shutil

print(
'''
***********************************
  每日名句获取器-邮件配置助手  
***********************************
运行后，会帮您配置 /Mypackage 下的 `mailsetting.json`。
我需要您明白：
1. 什么是SMTP
2. 拥有支持SMTP的账户

如果您没有支持SMTP的邮箱，您可以考虑使用俄罗斯的Yandex提供的邮箱：Yandex Mail。

请务必阅读以上说明后再开始设置。

''')

where_script = os.path.split(os.path.realpath(__file__))[0]

time.sleep(3)

shutil.copyfile(where_script + '/mailsetting(origin).json', where_script + '/mailsetting.json')

chosen = input('按下回车进行配置。或输入大写N跳过。')

if chosen == 'N':
    print('您选择跳过。您将无法使用邮件服务。')
    time.sleep(2)
    sys.exit(0)
else:
    f = codecs.open(where_script + '/mailsetting.json', 'r+','utf-8')
    mailjson = json.load(f)
    f.close()
    pass
    

print('第一项配置：SMTP服务器（主机）')
smtp_host = input('输入您的SMTP服务器（主机）地址：')
mailjson["smtp_host"] = smtp_host

print('第二项配置：SMTP服务器（主机）端口')
smtp_port = input('输入您的SMTP服务器（主机）端口，一般是22或465：')
while smtp_port.isdigit() is False:
    print('端口输入错误！这不是数字吧？')
    smtp_port = input('输入您的SMTP服务器（主机）端口，一般是22或465：')
mailjson["smtp_port"] = int(smtp_port)

print('第三项配置：SMTP账户')
smtp_user = input('输入您的SMTP账户（发件邮箱）：')
mailjson["smtp_user"] = smtp_user

print('第四项配置：SMTP账户密码/授权码')
smtp_passwd = input('输入您的SMTP账户（发件邮箱）密码/授权码：')
mailjson["smtp_passwd"] = smtp_passwd

print('第五项配置：发件人')
sender = input('输入您希望的发件人。不知道写什么，就填写发件邮箱：')
mailjson["sender"] = sender

print('第六项配置：收件人')
print('此配置支持多人。多人请用英文逗号分隔开，中间不用加空格。例如：')
print('单人请输入：email@email.com')
print('多人请输入：email1@email.com,email2@email.com,email3@email.com')
receivers = input('输入您希望的收件人邮箱：')
mailjson["receivers"] = receivers.split(",")  

print('配置完成。开始保存。')

f = codecs.open(where_script + '/mailsetting.json', 'w', 'utf-8')
json.dump(mailjson, f, indent=4, ensure_ascii=False)
f.close()

if os.path.exists(where_script + '/mailsetting.json'):
    print('保存成功！3秒后自动退出。')
else :
    print('配置错误。请在Github向我发送ISSUE，或尝试安装结束后以管理员身份再次运行此程序。')

time.sleep(3)
