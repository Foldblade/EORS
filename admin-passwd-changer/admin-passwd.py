# encoding:utf-8

import hashlib
import codecs
import time
import os
import shutil

print(
'''
***********************************
  每日名句获取器-管理密码修改器   
***********************************
运行后，会在此程序运行目录下创建新的'password'文件。
本程序将自动把'password'文件自动复制到程序主体目录的'/safety'文件夹下，覆盖原有'password'文件完成配置。
（如果您是在使用安装程序，请无视以上内容——一切都是自动的，不用您操心）
您的密码将不会以明文形式存储在您的计算机上。
如果您遗忘了密码，您还可以在安装目录下找到本“管理密码修改器”再度进行设置。
当然，安全起见，我建议您配置完密码后手动删除本程序。

请务必阅读以上说明后再开始设置。

''')

time.sleep(3)

where_script = os.path.split(os.path.realpath(__file__))[0]
# print(where_script)
where_rootmenu = where_script[:where_script.rfind('\\')]
# print(where_rootmenu)

input('按下回车开始设置密码。')
passwd = input('请输入管理密码：')

str = passwd.encode('utf-8')
sha = hashlib.sha256(str)
encrypts = sha.hexdigest()
f = codecs.open('password', 'w', 'utf-8')
f.write(encrypts)
f.close()

print('密码文件已经生成。')
print('配置中……')
shutil.copyfile(where_script + '/password', where_rootmenu + '/safety/password')

if os.path.exists(where_rootmenu + '/safety/password'):
    print('配置完毕。3秒后自动退出。')
else :
    print('配置错误。请在Github向我发送ISSUE，或尝试以管理员身份再次运行此程序。')

time.sleep(3)


