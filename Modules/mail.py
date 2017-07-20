# encoding:utf-8

import os
import datetime
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
import json

now = datetime.datetime.now()
nowdate = now.strftime('%Y-%m-%d')
nowyear = now.strftime('%Y')
nowmonth = str(int(now.strftime('%m')))
nowday = str(int(now.strftime('%d')))
print(nowdate)

where_script = os.path.split(os.path.realpath(__file__))[0]
print(where_script)
where_rootmenu = where_script[:where_script.rfind('\\')]
print(where_rootmenu)


f = open(where_script + '/mailsetting.json', 'r')
mailjson = json.load(f)
f.close()


def mailto(receivers):
    for people in receivers:
        print(people)
        message = MIMEMultipart()

        # 第三方 SMTP 服务
        smtp_host = mailjson["smtp_host"]  # SMTP服务器
        smtp_port = int(mailjson["smtp_port"])
        smtp_user = mailjson["smtp_user"]  # 用户名
        smtp_passwd = mailjson["smtp_passwd"]  # 密码

        sender = mailjson["sender"]  # 发件人邮箱(最好写全, 不然会失败)
        receiver = [people]
        print(receiver)

        content = '发送时间：' + nowdate
        title = '本周名句(' + nowdate + ')'  # 邮件主题
        message.attach(MIMEText(content, 'plain', 'utf-8'))  # 内容, 格式, 编码

        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receiver)
        message['Subject'] = title

        file_names = []
        file_names.append(where_rootmenu + '/output/'+ nowmonth + '月.txt')
        if int(nowday) < 7:
            try:
                if nowmonth == 1:
                    file_names.append(where_rootmenu + '/output/12月.txt')
                else:
                    file_names.append(where_rootmenu + '/output/' + str(int(nowmonth) - 1) + '月.txt')
            except:
                pass

        
        for file_name in file_names:
            data = open(file_name, 'rb')
            ctype, encoding = mimetypes.guess_type(file_name)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            file_msg = MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read())
            data.close()
            encoders.encode_base64(file_msg)  # 把附件编码
            basename = os.path.basename(file_name)
            file_msg.add_header('Content-Disposition', 'attachment', filename=basename)# 修改邮件头
            message.attach(file_msg)  # 设置根容器属性

        try:
            smtpObj = smtplib.SMTP_SSL(smtp_host, smtp_port)  # 启用SSL发信, 端口一般是465
            smtpObj.login(smtp_user, smtp_passwd)  # 登录验证
            smtpObj.sendmail(sender, receiver, message.as_string())  # 发送
            print(people + "'s mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)
    return()


print(mailjson["receivers"])
mailto(mailjson["receivers"])
