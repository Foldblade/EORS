# encoding:utf-8

'''
————————————————————————————————
backup.py
备份三个重要文件夹的文件，所谓‘回到昨天’功能的第一步。
实现原理：压缩文件为zip，存储到 /backup 目录。
————————————————————————————————
'''

import os
import zipfile

def backup():
    where_script = os.path.split(os.path.realpath(__file__))[0]
    # print(where_script)
    where_rootmenu = where_script[:where_script.rfind('\\')]
    # print(where_rootmenu)

    def zipit(sourceFilePath, zipFilePath, zipfileName):
        z = zipfile.ZipFile(os.path.join(zipFilePath, zipfileName), 'w', zipfile.ZIP_DEFLATED)
        startdir = sourceFilePath
        for dirpath, dirnames, filenames in os.walk(startdir):
            # print('Dirpath:', dirpath)
            # print('Dirnames:', dirnames)
            # print('Filenames:', filenames)
            for filename in filenames:
                print('FILENAME：',filename)
                sourceFileFullDir = os.path.join(dirpath, filename)
                # sourceFileFullDir是文件的全路径
                sourceFileFullDir_inZIP = sourceFileFullDir.replace(startdir,'')
                # print(sourceFileFullDir_inZIP)
                z.write(sourceFileFullDir, sourceFileFullDir_inZIP)
                # 第一个参数：源文件全路径；第二个参数：ZIP中该文件路径。
                # 思路：源文件全路径 - 被打包文件夹的路径 = ZIP中该文件路径
                # 大概呢也就我才能这么有病的搞个这种文件目录吧，文件夹里套文件夹，还有几个散兵游勇。
        z.close()
        return

    zipit(where_rootmenu + '/cache', where_rootmenu + '/backup', 'cache.zip')
    zipit(where_rootmenu + '/output', where_rootmenu + '/backup', 'output.zip')
    zipit(where_rootmenu + '/data', where_rootmenu + '/backup', 'data.zip')

    print('备份成功!')
    return
