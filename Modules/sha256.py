# encoding:utf-8

import hashlib
import codecs
import os

where_script = os.path.split(os.path.realpath(__file__))[0]
print(where_script)
where_rootmenu = where_script[:where_script.rfind('\\')]
print(where_rootmenu)

def encrypt(passwd):
    global encrypts
    # 使用sha256加密算法，返回str加密后的字符串
    str = passwd.encode('utf-8')
    sha = hashlib.sha256(str)
    encrypts = sha.hexdigest()
    print(encrypts)
    return encrypts

def get_now_passwd():
    global existpassword
    f = codecs.open(where_rootmenu + '/safety/password', 'rb', 'utf-8')
    existpassword = f.read()
    f.close()
    print(existpassword)
    return existpassword

if encrypt('foldblade') == get_now_passwd():
    print('success!')

