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

where_script = os.path.split(os.path.realpath(__file__))[0]
# print(where_script)
where_rootmenu = where_script[:where_script.rfind('\\')]
# print(where_rootmenu)

'''
def backup(dirpath, zipfilename):
    
    z = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
    startdir = dirpath
    for dirpath, dirnames, filenames in os.walk(startdir):
        print(dirpath)
        print(filenames)
        for filename in filenames:
            #filefullpath = dirpath + '/' + filename
            print(filename)
            z.write(os.path.join(dirpath, filename))
            # z.write(filename)
    z.close()
    
    return
'''
# backup(where_rootmenu + '/cache',where_rootmenu + '/backup/cache.zip')


def backup(sourceFilePath, zipFilePath, zipfileName):
    sourceFiles = os.listdir(sourceFilePath)
    if sourceFiles == None or len(sourceFiles) < 1:
        print(">>>>>> 待压缩的文件目录：" + sourceFilePath + " 里面不存在文件,无需压缩. <<<<<<")
    else:
        zipFileFullDir = os.path.join(zipFilePath, zipfileName)
        z = zipfile.ZipFile(zipFileFullDir, 'w', zipfile.ZIP_DEFLATED)
        for sourceFile in sourceFiles:
            sourceFileFullDir = os.path.join(sourceFilePath, sourceFile)
            # sourceFileFullDir是文件的全路径，sourceFile是文件名，这样就能达到你要的目的了
            z.write(sourceFileFullDir, sourceFile)
        z.close()
    return

backup(where_rootmenu + '/cache',where_rootmenu + '/backup','cache.zip')
backup(where_rootmenu + '/output',where_rootmenu + '/backup','output.zip')
backup(where_rootmenu + '/data',where_rootmenu + '/backup','data.zip')

print('备份成功!')