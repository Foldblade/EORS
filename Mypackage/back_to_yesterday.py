# encoding:utf-8

'''
————————————————————————————————
back_to_yesterday.py
对备份文件的回档，所谓‘回到昨天’功能。
实现原理：删除源文件。解压备份的zip，自动覆盖。
————————————————————————————————
'''

import os
import zipfile
import shutil
import time

def back_to_yesterday():
    where_script = os.path.split(os.path.realpath(__file__))[0]
    # print(where_script)
    where_rootmenu = where_script[:where_script.rfind('\\')]
    # print(where_rootmenu)

    def unzip(zipfilepath, unzippath):
        # zipfilepath 为需要解压的文件路径，unzippath为解压的目标目录
        # e.g.  unzip(where_rootmenu + '/cache/cache.zip', where_rootmenu + '/cache')
        f = zipfile.ZipFile(zipfilepath, 'r')
        for file in f.infolist():
            d = file.date_time
            gettime = "%s/%s/%s %s:%s" % (d[0], d[1], d[2], d[3], d[4])  # 获取文件原修改时间
            f.extract(file, unzippath)
            filep = os.path.join(unzippath, file.filename)
            timearry = time.mktime(time.strptime(gettime, '%Y/%m/%d %H:%M'))
            os.utime(filep, (timearry, timearry))  # 重写文件原修改时间
        return

    def clear_unexist(dirname, zipfilename):
        zipfilepath = (where_rootmenu + '/backup/' + zipfilename)
        fileinzip = []
        f = zipfile.ZipFile(zipfilepath, 'r')
        for filename in f.namelist():
            # print(filename)
            fileinzip.append(filename)

        for parent, dirnames, filenames in os.walk(dirname):
            for filename in filenames:
                # print ("parent is:" + parent)
                # print("filename is:" + filename)
                # print ("the full name of the file is:" + os.path.join(parent,filename))
                if filename not in fileinzip:
                    os.remove(os.path.join(parent, filename))  # 删除压缩包内不存在的文件
        return

    clear_unexist(where_rootmenu + '/cache', 'cache.zip')
    clear_unexist(where_rootmenu + '/data', 'data.zip')
    clear_unexist(where_rootmenu + '/output', 'output.zip')
    # 删除压缩包内不存在的文件

    shutil.copyfile(where_rootmenu + '/backup/cache.zip', where_rootmenu + '/cache/cache.zip')
    shutil.copyfile(where_rootmenu + '/backup/output.zip', where_rootmenu + '/output/output.zip')
    shutil.copyfile(where_rootmenu + '/backup/data.zip', where_rootmenu + '/data/data.zip')
    # 拷贝备份zip到各自目录下

    unzip(where_rootmenu + '/cache/cache.zip', where_rootmenu + '/cache')
    unzip(where_rootmenu + '/output/output.zip', where_rootmenu + '/output')
    unzip(where_rootmenu + '/data/data.zip', where_rootmenu + '/data')
    # 解压文件

    os.remove(where_rootmenu + '/cache/cache.zip')
    os.remove(where_rootmenu + '/output/output.zip')
    os.remove(where_rootmenu + '/data/data.zip')
    # 删除拷贝的zip文件

    print('成功穿越回昨日!!')
    return

