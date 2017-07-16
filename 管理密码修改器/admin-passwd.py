# encoding:utf-8

import hashlib
import codecs

print(
'''
***********************************
*   每日名句获取器-管理密码修改器   *
***********************************
运行后，会在此程序运行目录下创建'password'文件。
请手动复制到程序主体目录的'/safety'文件夹下，覆盖原有'passwd'文件。
您的密码将不会以明文形式存储在您的计算机上。
''')



input('按下回车开始设置密码。')
passwd = input('请输入管理密码：')

str = passwd.encode('utf-8')
sha = hashlib.sha256(str)
encrypts = sha.hexdigest()
f = codecs.open('password', 'w', 'utf-8')
f.write(encrypts)
f.close()
print('密码文件已经生成。')