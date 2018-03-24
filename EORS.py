# encoding:utf-8

from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
# from tkinter.ttk import * # 这行去掉注释会引入windows最新的特性，不过下面的程序涉及relief就会报错
import os
import sys
import datetime
import linecache
import json
import codecs
import hashlib
import requests
import webbrowser
import threading
from bs4 import BeautifulSoup
from Mypackage import get
from Mypackage import back_to_yesterday
from Mypackage import mail
from Mypackage import backup
from Mypackage import spvoice

now = datetime.datetime.now()
nowdate = now.strftime('%Y-%m-%d')
nowyear = str(int(now.strftime('%Y')))
nowmonth = str(int(now.strftime('%m')))
nowday = str(int(now.strftime('%d')))
print(nowdate)
# 获取当前年月日

where_script = os.path.split(os.path.realpath(__file__))[0]
print(where_script)

f = open(where_script+'/data/setting.json', 'r')
setting_json = json.load(f)
f.close()

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    print(size)
    root.geometry(size)

# 检查更新
def check_update():
    try:
        url = 'https://github.com/Foldblade/EORS/releases'
        postdata = {
            "headers": {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
        }
        s = requests.session()
        try:
            r = requests.get(url, data=postdata, timeout=2)
            response.encoding = 'utf-8'  # 修改编码为utf-8
        except:
            pass
        r = r.text
        webdata = BeautifulSoup(r, 'html.parser')
        find_v = webdata.find_all(class_='css-truncate-target')
        latest_version = str(find_v[0].get_text())
        latest_version = latest_version.replace('\r', '')
        latest_version = latest_version.replace('\n', '')
        latest_version = latest_version[1:]
    except:
        pass
    return latest_version

# 按钮 输出目录 被单击
def button_opendir_click():
    try:
        os.startfile(where_script + '/output/' + nowyear)
    except:
        os.startfile(where_script + '/output')

    return

# 按钮 退出 被单击
def button_exit_click():
    root.quit()
    sys.exit(0)
    return

# 按钮 关于 被单击
def button_about_click():

    # 按钮 返回 被单击，下同，不注释
    def button_back_click():
        about_window.destroy()
        root.deiconify()
        root.update()
        return
    about_window = Toplevel()
    center_window(about_window, 640, 400)
    about_window.overrideredirect(1)

    topbar = Frame(about_window, width=640, height=72)
    backpng = PhotoImage(file=where_script + '/UI/back2.png')
    button_back = Button(topbar, image=backpng, relief=FLAT, cursor='hand2', command=button_back_click)
    button_back.grid(row=1, column=1, sticky=W)
    label = Label(topbar, text='关于', font=('思源黑体 CN Light', 28), justify='center', anchor='center')
    label.grid(row=1, column=2, sticky=W)
    topbar.pack(side=TOP, expand=NO, fill=X)
    # 顶部条，一个返回按钮和当前栏目名称/功能。下文所有topbar功能一致，故不加注释。


    readmearea = Frame(about_window, width=600, height=250)
    scroll = Scrollbar(readmearea)
    scroll.pack(side=RIGHT, anchor=W, fill=Y)
    readmetext = Text(readmearea, relief=FLAT, font=('思源黑体 CN Regular', 10), padx=10, pady=10, bd=0,
                      bg='#f0f0f0', yscrollcommand=scroll.set)
    readmetext.pack(side=LEFT, expand=NO, fill=NONE, anchor=CENTER)
    readme = linecache.getlines('ReadMe.md')
    for linenum in range(0, len(readme)):
        readmetext.insert(END, readme[linenum])
    readmearea.pack(side=TOP, expand=NO, fill=NONE)
    scroll.config(command=readmetext.yview)
    about_window.mainloop()
    root.withdraw()
    # 添加Text区，显示ReadMe.md 的内容

    return


# 按钮 发送邮件 被单击
def button_mail_click():
    # 用的是两个messagebox弹窗。画风就不一致了……也许日后再修复吧。
    try:
        mail.mail()
        tkinter.messagebox.showinfo('邮件模组', '邮件发送成功！\n(ㅅ´ ˘ `)♡~')
    except:
        tkinter.messagebox.showerror('邮件模组', '出……出错啦 TAT\n请检查配置/网络再试一次？\n(ㅅ´ ˘ `)♡~')
    return

# 按钮 设置 被单击
def button_setting_click():

    def button_back_click():
        setting_window.destroy()
        root.deiconify()
        root.update_idletasks()
        root.update()
        return

    def listbox_mode_show_msg(event):
        global listbox_mode_newchosen
        print(listbox_mode.get(listbox_mode.curselection()))
        mode_chosen.set('当前：' + listbox_mode.get(listbox_mode.curselection()))
        listbox_mode_newchosen = listbox_mode.get(listbox_mode.curselection())
        return listbox_mode_newchosen

    def listbox_once_show_msg(event):
        global listbox_once_newchosen
        print(listbox_once.get(listbox_once.curselection()))
        once_chosen.set('当前：' + listbox_once.get(listbox_once.curselection()))
        listbox_once_newchosen = listbox_once.get(listbox_once.curselection())
        return listbox_once_newchosen

    def listbox_speech_show_msg(event):
        global listbox_speech_newchosen
        print(listbox_speech.get(listbox_speech.curselection()))
        speech_chosen.set('当前：' + listbox_speech.get(listbox_speech.curselection()))
        listbox_speech_newchosen = listbox_speech.get(listbox_speech.curselection())
        return listbox_speech_newchosen

    def listbox_countdown_show_msg(event):
        global listbox_countdown_newchosen
        print(listbox_countdown.get(listbox_countdown.curselection()))
        countdown_chosen.set('当前：' + listbox_countdown.get(listbox_countdown.curselection()))
        listbox_countdown_newchosen = listbox_countdown.get(listbox_countdown.curselection())
        return listbox_countdown_newchosen

    def back_to_ysd32_click():
        def button_back2_click():
            back_to_ysd_window.destroy()
            return

        def back_to_ysd_click():
            # print(passwd.get())
            # 特别注释：上一行的注释去掉，点击back_to_ysd按钮，就会print输入的密码！！
            inputpasswd = passwd.get()
            try:
                str = inputpasswd.encode('utf-8')
                sha = hashlib.sha256(str)
                encrypts = sha.hexdigest()
                f = codecs.open(where_script+'/safety/password', 'rb', 'utf-8')
                existpassword = f.read()
                f.close()
                if encrypts == existpassword:
                    back_to_ysd_change.set('时光机穿越中……')
                    print('Correct! PASS!')
                    back_to_ysd_window.update_idletasks()
                    back_to_ysd_window.update()
                    back_to_yesterday.back_to_yesterday()
                    back_to_ysd_change.set('已经回到昨日！')
                else:
                    print('Wrong passwd!')
                    back_to_ysd_change.set('密码错误！')
                    # 对输入密码进行Sha256加密，并对照
            except:
                print('Something Wrong.')
                back_to_ysd_change.set('伦家被绕晕了啦')

            back_to_ysd_window.update_idletasks()
            back_to_ysd_window.update()
            return

        back_to_ysd_window = Toplevel()
        center_window(back_to_ysd_window, 300, 180)
        back_to_ysd_window.overrideredirect(1)
        back_to_ysd_window.iconbitmap(where_script + '/UI/MRMJ_32.ico')
        back_to_ysd_window.wm_title('回到昨日')

        back_to_ysd_frame = Frame(back_to_ysd_window, relief=SOLID)

        back32png = PhotoImage(file=where_script + '/UI/back2_32.png')
        button_back2 = Button(back_to_ysd_frame, image=back32png, relief=FLAT, cursor='hand2', command=button_back2_click)
        button_back2.grid(row=1, column=1, sticky=W)

        back_to_ysd_change = StringVar()
        back_to_ysd_change.set('请输入管理员密码：')
        Label1 = Label(back_to_ysd_frame, text='确定回到昨日吗？', font=('思源黑体 CN Light', 16), justify='center', anchor='center')
        Label1.grid(row=1, column=2, sticky=W)
        Label2 = Label(back_to_ysd_frame, textvariable=back_to_ysd_change, font=('思源黑体 CN Regular', 12), justify='center',anchor='center')
        Label2.grid(row=2, column=1, columnspan=2, sticky='nsew')

        passwd = StringVar()
        passwdentry = Entry(back_to_ysd_frame, textvariable=passwd,width=5, show="*")
        passwdentry.grid(row=3, column=1, columnspan=2, sticky='nsew')

        back_to_ysd_frame.pack()

        back_to_ysdpng = PhotoImage(file=where_script + '/UI/backtoyes.png')
        button_back_to_ysd = Button(back_to_ysd_window, image=back_to_ysdpng, relief=FLAT, cursor='hand2', command=back_to_ysd_click)
        button_back_to_ysd.pack()

        back_to_ysd_window.update_idletasks()
        back_to_ysd_window.mainloop()
        return


    def button_save_click():

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()
        try:
            try:
                if listbox_mode_newchosen == '句子迷':
                    setting_json["mode"] = "juzimi"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                elif listbox_mode_newchosen == '作文纸条':
                    setting_json["mode"] = "zuowennote"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                savemessage.set('保存啦 QwQ')
            except:
                savemessage.set('出了点问题orz')

            try:
                if listbox_once_newchosen == 'ON':
                    setting_json["once"] = "on"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                elif listbox_once_newchosen == 'OFF':
                    setting_json["once"] = "off"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                savemessage.set('保存啦 QwQ')
            except:
                savemessage.set('出了点问题orz')

            try:
                if listbox_speech_newchosen == 'ON':
                    setting_json["speech"] = "on"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                elif listbox_speech_newchosen == 'OFF':
                    setting_json["speech"] = "off"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                savemessage.set('保存啦 QwQ')
            except:
                savemessage.set('出了点问题orz')

            try:
                if listbox_countdown_newchosen == 'ON':
                    setting_json["countdown"] = "on"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                elif listbox_countdown_newchosen == 'OFF':
                    setting_json["countdown"] = "off"
                    f = open(where_script+'/data/setting.json', 'w')
                    json.dump(setting_json, f, indent=4, ensure_ascii=False)
                    f.close()
                savemessage.set('保存啦 QwQ')
            except:
                savemessage.set('出了点问题orz')
        except:
            savemessage.set('操作错误，未记录。')


        setting_window.update_idletasks()
        setting_window.update()
        return

    setting_window = Toplevel()
    center_window(setting_window, 640, 400)
    setting_window.overrideredirect(1)
    setting_window.iconbitmap(where_script+'/UI/MRMJ_32.ico')

    topbar = Frame(setting_window, width=640, height=72)
    backpng = PhotoImage(file=where_script+'/UI/back2.png')
    button_back = Button(topbar, image=backpng, relief=FLAT, cursor='hand2', command=button_back_click)
    button_back.grid(row=1, column=1, sticky=W)
    label_setting = Label(topbar, text='设置', font=('思源黑体 CN Light', 28), justify='center', anchor='center')
    label_setting.grid(row=1, column=2, sticky=W)
    topbar.pack(side=TOP, expand=NO, fill=X)

    setting_area = Frame(setting_window,width=500, height=200)
    f = open(where_script+'/data/setting.json','r')
    setting_json = json.load(f)
    f.close()
    Label_mode = Label(setting_area, text='模式选择', font=('思源黑体 CN Regular', 14))
    Label_mode.grid(row=1, column=1, sticky=W)
    selection = ['句子迷', '作文纸条']
    mode = StringVar(value=selection)
    listbox_mode = Listbox(setting_area, height=2, width=7, selectmode=BROWSE, listvariable=mode, bd=1, bg='#f0f0f0')
    listbox_mode.grid(row=1, column=2, sticky=W)
    listbox_mode.bind("<<ListboxSelect>>", listbox_mode_show_msg)

    mode_chosen = StringVar()
    if setting_json["mode"] == 'juzimi':
        mode_chosen.set('当前：句子迷')
    elif setting_json["mode"] == 'zuowennote':
        mode_chosen.set('当前：作文纸条')
    Label_mode_follow = Label(setting_area, textvariable=mode_chosen, font=('思源黑体 CN Light', 12))
    Label_mode_follow.grid(row=1, column=3, sticky=W)

    Label_once = Label(setting_area, text='每日一次', font=('思源黑体 CN Regular', 14))
    Label_once.grid(row=1, column=4, sticky=W)
    selection = ['ON', 'OFF']
    once = StringVar(value=selection)
    listbox_once = Listbox(setting_area, height=2, width=7, selectmode=BROWSE, listvariable=once, bd=1, bg='#f0f0f0')
    listbox_once.grid(row=1, column=5, sticky=W)
    listbox_once.bind("<<ListboxSelect>>", listbox_once_show_msg)

    once_chosen = StringVar()
    if setting_json["once"] == 'on':
        once_chosen.set('当前：ON')
    elif setting_json["once"] == 'off':
        once_chosen.set('当前：OFF')
    Label_once_follow = Label(setting_area, textvariable=once_chosen, font=('思源黑体 CN Light', 12))
    Label_once_follow.grid(row=1, column=6, sticky=W)

    Label_speech = Label(setting_area, text='朗读句子', font=('思源黑体 CN Regular', 14))
    Label_speech.grid(row=2, column=1, sticky=W)
    selection = ['ON', 'OFF']
    speech = StringVar(value=selection)
    listbox_speech = Listbox(setting_area, height=2, width=7,
                             selectmode=BROWSE, listvariable=speech, bd=1, bg='#f0f0f0')
    listbox_speech.grid(row=2, column=2, sticky=W)
    listbox_speech.bind("<<ListboxSelect>>", listbox_speech_show_msg)

    speech_chosen = StringVar()
    if setting_json["speech"] == 'on':
        speech_chosen.set('当前：ON')
    elif setting_json["speech"] == 'off':
        speech_chosen.set('当前：OFF')
    Label_speech_follow = Label(setting_area, textvariable=speech_chosen, font=('思源黑体 CN Light', 12))
    Label_speech_follow.grid(row=2, column=3, sticky=W)

    Label_countdown = Label(setting_area, text='高考计时', font=('思源黑体 CN Regular', 14))
    Label_countdown.grid(row=2, column=4, sticky=W)
    selection = ['ON', 'OFF']
    countdown = StringVar(value=selection)
    listbox_countdown = Listbox(setting_area, height=2, width=7,
                             selectmode=BROWSE, listvariable=speech, bd=1, bg='#f0f0f0')
    listbox_countdown.grid(row=2, column=5, sticky=W)
    listbox_countdown.bind("<<ListboxSelect>>", listbox_countdown_show_msg)

    countdown_chosen = StringVar()
    if setting_json["speech"] == 'on':
        countdown_chosen.set('当前：ON')
    elif setting_json["speech"] == 'off':
        countdown_chosen.set('当前：OFF')
    Label_countdown_follow = Label(setting_area, textvariable=speech_chosen, font=('思源黑体 CN Light', 12))
    Label_countdown_follow.grid(row=2, column=6, sticky=W)

    Label_back_to = Label(setting_area, text='回到昨日', font=('思源黑体 CN Regular', 14))
    Label_back_to.grid(row=3, column=3, sticky=W)
    back_to_ysd32png = PhotoImage(file=where_script+'/UI/backtoyes_32.png')
    button_back_to_ysd32 = Button(setting_area, image=back_to_ysd32png, relief=FLAT, cursor='hand2', command=back_to_ysd32_click)
    button_back_to_ysd32.grid(row=3, column=4, sticky=W)

    setting_area.pack(side=TOP, expand=NO, fill=Y)

    bottombar = Frame(setting_window, width=640, height=120)
    savemessage = StringVar()
    savemessage.set('记得保存更改哦↓')
    labelsave = Label(bottombar, textvariable=savemessage, font=('思源黑体 CN Light', 20))
    labelsave.pack(side=TOP, expand=NO, fill=NONE, anchor=CENTER)
    savepng = PhotoImage(file=where_script+'/UI/save.png')
    button_save = Button(bottombar, image=savepng, relief=FLAT, cursor='hand2', command=button_save_click)
    button_save.pack(side=BOTTOM, expand=NO, fill=NONE, anchor=CENTER)

    bottombar.pack(side=BOTTOM, expand=NO, fill=X)

    setting_window.update_idletasks()
    setting_window.mainloop()
    root.withdraw()
    return


# 按钮 离线模式 被单击， 注释参照下一个函数button_write_click()，两者基本一致
def button_offline_click():
    def button_back_click():
        offline_window.destroy()
        root.deiconify()
        root.update_idletasks()
        root.update()
        return

    def chose_listbox_show_msg(event):
        print(chose_listbox.get(chose_listbox.curselection()))
        chose_sentence = chose_listbox.get(chose_listbox.curselection())
        return chose_sentence

    def button_next_click():
        backup.backup()
        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()

        if setting_json["mode"] == 'juzimi':
            f = codecs.open(where_script+'/data/today.txt', 'wb', 'utf-8')
            f.write(chose_listbox_show_msg('event')[:-2])  # 为什么是截取-2? 答:去掉原来的换行符
            f.close()
        elif setting_json["mode"] == 'zuowennote':
            f = codecs.open(where_script+'/data/today.txt', 'wb', 'utf-8')
            f.write(chose_listbox_show_msg('event'))
            f.close()

        final_window = Toplevel()
        center_window(final_window, 900, 500)
        final_window.overrideredirect(1)

        def button_back_click():
            final_window.destroy()
            offline_window.deiconify()
            offline_window.update_idletasks()
            offline_window.update()
            return

        def button_finish_click():
            f = open(where_script+'/data/setting.json', 'r')
            setting_json = json.load(f)
            f.close()

            if not os.path.exists(where_script + '/output/%(year)s' % {'year': nowyear}):
                os.makedirs(where_script + '/output/%(year)s' % {'year': nowyear})
            if not os.path.exists(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}):
                f = codecs.open(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}
                                , 'wb', 'utf-8')
                f.close()
            # 判断当月文件是否存在，不存在则创建

            if setting_json["mode"] == 'juzimi':

                f = codecs.open(where_script+'/data/today.txt', 'r', 'utf-8')
                sentence_output = f.read()
                f.close()

                output = codecs.open(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}, 'ab', 'utf-8')
                output.write(nowyear + '年' + nowmonth + '月' + nowday + '日' + '\r\n')
                output.write(sentence_output + '\r\n')
                output.write('\r\n')
                output.close()

                allhistory = codecs.open(where_script + '/data/allhistory.txt', 'ab', 'utf-8')
                allhistory.write(sentence_output + '\r\n')
                allhistory.close()

                cache_former = codecs.open(where_script + '/cache/sentence.txt', 'r', 'utf-8')

                allhistoryfile = codecs.open(where_script + '/data/allhistory.txt', 'r', 'utf-8')
                allhistory = []
                for line in allhistoryfile:
                    line = line.replace('\n','')
                    line = line.replace('\r','')
                    line = line.replace('\r\n','')
                    line = line.replace('\ufeff', '')
                    allhistory.append(line)
                allhistoryfile.close()

                cache = []

                for line in cache_former:
                    line = line.replace('\r', '')
                    line = line.replace('\n', '')
                    line = line.replace('\r\n', '')
                    line = line.replace('\ufeff', '')

                    if line not in allhistory:
                        if (line + '\r\n') not in cache:
                            cache.append(line + '\r\n')

                cache_file = codecs.open(where_script+'/cache/sentence.txt', 'wb', 'utf-8')
                for line in cache:
                    cache_file.write(line)
                cache_file.close()

                cache_former.close()

                f = open(where_script+'/data/setting.json', 'r')
                setting_json = json.load(f)
                f.close()
                if setting_json["once"] == "on":
                    f = open(where_script+'/data/uselog', 'w')
                    f.write(nowdate)
                    f.close()
                    # 使用记录。免得有人手贱，不回档还一天跑两回。

                print('存储完成，感谢使用。')
                root.quit()
                sys.exit(0)

            elif setting_json["mode"] == 'zuowennote':
                f = codecs.open(where_script+'/data/today.txt', 'r', 'utf-8')
                sentence_output = f.read()
                f.close()

                guidance_output = guidance_str

                output = codecs.open(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}, 'ab', 'utf-8')
                output.write(nowyear + '年' + nowmonth + '月' + nowday + '日' + '\r\n')
                output.write(sentence_output + '\r\n')
                output.write('（' + guidance_output + '）\r\n')
                output.write('\r\n')
                output.close()

                allhistory = codecs.open(where_script+'/data/zuowennote_allhistory.json', 'r', 'utf-8')
                allhistory_json = json.load(allhistory)
                # print(allhistory_json)
                allhistory.close()

                f = codecs.open(where_script+'/cache/zuowennote.json', 'r', 'utf-8')
                zuowennote_json = json.load(f)
                f.close()

                for sentencejson in zuowennote_json:
                    zuowennote_sentence = sentencejson["title"]
                    # print(zuowennote_sentence)
                    # print(sentencejson)
                    if zuowennote_sentence == sentence_str:
                        allhistory_json.append(sentencejson)
                        # print(allhistory_json)
                        allhistory = codecs.open(where_script+'/data/zuowennote_allhistory.json', 'wb', 'utf-8')
                        json.dump(allhistory_json, allhistory, indent=4, ensure_ascii=False)
                        allhistory.close()
                        break
                    else:
                        pass

                f = open(where_script+'/data/setting.json', 'r')
                setting_json = json.load(f)
                f.close()
                if setting_json["once"] == "on":
                    f = open(where_script+'/data/uselog', 'w')
                    f.write(nowdate)
                    f.close()
                    # 使用记录。免得有人手贱，不回档还一天跑两回。

                print('存储完成，感谢使用。')
                root.quit()
                sys.exit(0)

            return

        topbar = Frame(final_window)
        backpng = PhotoImage(file=where_script+'/UI/back2.png')
        button_back = Button(topbar, image=backpng, relief=FLAT, cursor='hand2', command=button_back_click)
        button_back.grid(row=1, column=1, sticky=W)

        f = codecs.open(where_script+'/data/today.txt', 'r', 'utf-8')
        sentencedata = f.read()
        f.close()

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()

        if setting_json["mode"] == 'juzimi':
            sentence_str = sentencedata[:sentencedata.find('——')]
            if sentencedata.find('《') == -1:
                writer_str = sentencedata[sentencedata.rfind('——') + 2:]
                book_str = ''
            else:
                writer_str = sentencedata[sentencedata.rfind('——') + 2:sentencedata.rfind('《')]
                book_str = sentencedata[sentencedata.rfind('《'):sentencedata.rfind('》') + 1]
        elif setting_json["mode"] == 'zuowennote':
            book_str = ''
            sentence_str = sentencedata[:sentencedata.find('——')]
            # print('sentence_str=' + sentence_str)
            writer_str = sentencedata[sentencedata.rfind('——') + 2:]
            if writer_str.find('『') != -1:
                book_str = writer_str
                writer_str = ''
            f = codecs.open(where_script+'/cache/zuowennote.json', 'r', 'utf-8')
            zuowennote_json = json.load(f)
            f.close()
            for sentencejson in zuowennote_json:
                zuowennote_sentence = sentencejson["title"]
                # print('zuowennote_sentence=' + zuowennote_sentence)
                if zuowennote_sentence == sentence_str:
                    guidance_str = sentencejson["content"]
                else:
                    pass


        if book_str == '':
            writer = StringVar()
            writer.set(writer_str)
            writer_label = Label(topbar, textvariable=writer, font=('思源宋体 CN SemiBold', 28), justify=LEFT, anchor=S)
            writer_label.grid(row=1, column=2, sticky=W)

            said = StringVar()
            said.set('曾经说过：')
            said_label = Label(topbar, textvariable=said, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
            said_label.grid(row=1, column=3, sticky=W)

            topbar.pack(side=TOP, expand=YES, fill=X)

        else:
            if len(writer_str + book_str) < 17:
                writer = StringVar()
                writer.set(writer_str)
                writer_label = Label(topbar, textvariable=writer, font=('思源宋体 CN SemiBold', 28), justify=LEFT, anchor=S)
                writer_label.grid(row=1, column=2, sticky=W)

                zai = StringVar()
                zai.set('在')
                zai_label = Label(topbar, textvariable=zai, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                zai_label.grid(row=1, column=3, sticky=W)

                book = StringVar()
                book.set(book_str)
                book_label = Label(topbar, textvariable=book, font=('思源宋体 CN Medium', 24), justify=LEFT, anchor=S)
                book_label.grid(row=1, column=4, sticky=W)

                said = StringVar()
                said.set('中曾经有过：')
                said_label = Label(topbar, textvariable=said, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                said_label.grid(row=1, column=5, sticky=W)
                topbar.pack(side=TOP, expand=YES, fill=X)
            else:
                writerbar = Frame(topbar)
                writer = StringVar()
                writer.set(writer_str)
                writer_label = Label(writerbar, textvariable=writer, font=('思源宋体 CN SemiBold', 28), justify=LEFT,
                                     anchor=S)
                writer_label.grid(row=1, column=1, sticky=W)
                zai = StringVar()
                zai.set('在')
                zai_label = Label(writerbar, textvariable=zai, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                zai_label.grid(row=1, column=2, sticky=W)
                writerbar.grid(row=1, column=2, sticky=W)

                bookbar = Frame(topbar)
                book = StringVar()
                book.set(book_str)
                book_label = Label(bookbar, textvariable=book, font=('思源宋体 CN Medium', 24), justify=LEFT, anchor=S)
                book_label.grid(row=1, column=1, sticky=W)
                said = StringVar()
                said.set('中曾经有过：')
                said_label = Label(bookbar, textvariable=said, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                said_label.grid(row=1, column=2, sticky=W)
                bookbar.grid(row=2, column=2, sticky=W)

                topbar.pack(side=TOP, expand=YES, fill=X)

        bottombar = Frame(final_window, width=640, height=72)
        finishpng = PhotoImage(file=where_script+'/UI/finish.png')
        button_finish = Button(bottombar, image=finishpng, relief=FLAT, cursor='hand2', command=button_finish_click)
        button_finish.pack(side=BOTTOM, expand=NO, fill=NONE, anchor=CENTER)

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()
        if setting_json["mode"] == 'juzimi':
            label_comefrom = Label(bottombar, text='内容来源：句子迷', font=('思源黑体 CN Regular', 8),
                                   justify=CENTER, anchor=CENTER)
            label_comefrom.pack(side=TOP, expand=NO, fill=NONE, anchor=CENTER)
        elif setting_json["mode"] == 'zuowennote':
            label_comefrom = Label(bottombar, text='内容来源：作文纸条', font=('思源黑体 CN Regular', 8),
                                   justify=CENTER, anchor=CENTER)
            label_comefrom.pack(side=TOP, expand=NO, fill=NONE, anchor=CENTER)
        else:
            pass

        bottombar.pack(side=BOTTOM, expand=YES, fill=BOTH)

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()

        if setting_json["mode"] == 'juzimi':
            juzimibar = Frame(final_window, width=756)
            sentence_text = ScrolledText(juzimibar, relief=FLAT, font=('思源宋体 CN Heavy', 28), width=35, bd=0,
                                 bg='#f0f0f0')
            sentence_text.insert(END, sentence_str)
            sentence_text.pack(side=LEFT, expand=NO, fill=NONE, anchor=CENTER)
            juzimibar.pack(side=TOP, expand=NO, fill=NONE)



        elif setting_json["mode"] == 'zuowennote':
            zuowennotebar = Frame(final_window)

            zuowennote_sentencebar = Frame(zuowennotebar)
            sentence_text = Text(zuowennote_sentencebar, relief=FLAT, font=('思源宋体 CN Heavy', 28), height=3,
                                 width=38, bd=0, bg='#f0f0f0')
            sentence_text.insert(END, sentence_str)
            sentence_text.pack(side=TOP, expand=YES, fill=X, anchor=CENTER, padx=20)
            zuowennote_sentencebar.grid(row=1, column=1, sticky=W)

            zuowennote_guidebar = Frame(zuowennotebar)
            guidance_text = ScrolledText(zuowennote_guidebar, relief=FLAT, font=('思源黑体 CN Regular', 16), #height=6,
                                 width=70, bd=0, bg='#f0f0f0')
            guidance_text.insert(END, guidance_str)
            guidance_text.pack(side=TOP, expand=YES, fill=Y, anchor=CENTER, padx=20)

            zuowennote_guidebar.grid(row=2, column=1, sticky=W)

            zuowennotebar.pack(side=TOP, expand=YES, fill=Y)

        # 朗读功能
        f = open(where_script + '/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()
        if setting_json["speech"] == 'on':
            if writer_str == '':
                speak_sentence = '在' + book_str + '中曾经有过：' + sentence_str
            elif writer_str != '':
                if book_str == '':
                    speak_sentence = writer_str + '曾经说过：' + sentence_str
                else:
                    speak_sentence = writer_str + '在' + book_str + '中曾经有过：' + sentence_str
            else:
                speak_sentence = sentence_str
            threads = []
            t1 = threading.Thread(target=spvoice.say, args=(speak_sentence,))
            threads.append(t1)
            if __name__ == '__main__':
                for t in threads:
                    t.setDaemon(True)
                    t.start()

        final_window.mainloop()
        offline_window.withdraw()
        return

    offline_window = Toplevel()
    center_window(offline_window, 640, 400)
    offline_window.overrideredirect(1)
    topbar = Frame(offline_window, width=640, height=72)
    backpng = PhotoImage(file=where_script+'/UI/back2.png')
    button_back = Button(topbar, image=backpng, relief=FLAT, cursor='hand2', command=button_back_click)
    button_back.grid(row=1, column=1, sticky=W)
    label = Label(topbar, text='选择你想发布的句子', font=('思源黑体 CN Light', 28), justify='center', anchor='center')
    label.grid(row=1, column=2, sticky=W)
    topbar.pack(side=TOP, expand=NO, fill=X)


    chosearea = Frame(offline_window, width=500,height=100)
    yscroll = Scrollbar(chosearea)
    yscroll.pack(side=RIGHT, anchor=CENTER, fill=Y)
    xscroll = Scrollbar(chosearea, orient=HORIZONTAL)
    xscroll.pack(side=BOTTOM, anchor=CENTER, fill=X)
    chose_listbox = Listbox(chosearea, font=('思源黑体 CN Regular', 12),width=50 , bg='#f0f0f0', bd=0,
                            yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

    f = open(where_script+'/data/setting.json', 'r')
    setting_json = json.load(f)
    f.close()

    if setting_json["mode"] == 'juzimi':
        f = codecs.open(where_script+'/cache/sentence.txt', 'r', 'utf-8')
        for line in f:
            chose_listbox.insert(END, line)
        f.close()

    elif setting_json["mode"] == 'zuowennote':
        f = codecs.open(where_script+'/cache/zuowennote.json', 'r', 'utf-8')
        zuowennote_json = json.load(f)
        f.close()
        f = codecs.open(where_script+'/data/zuowennote_allhistory.json', 'r', 'utf-8')
        zuowennote_allhistory_json = json.load(f)
        f.close()

        for sentencejson in zuowennote_json:
            if sentencejson not in zuowennote_allhistory_json:
                # print(sentencejson)
                zuowennote_sentence = sentencejson["title"]
                zuowennote_writer = sentencejson["author"]
                if sentencejson["content"] == '':
                    pass
                elif zuowennote_writer.find('纸条') != -1 or zuowennote_writer.find('迢遥旧梦') != -1 or \
                                zuowennote_writer.find('小胖纸') != -1 or zuowennote_writer.find('铝汉纸') != -1:
                    pass
                else:
                    chose_listbox.insert(END, zuowennote_sentence + '——' + zuowennote_writer)




    yscroll.config(command=chose_listbox.yview)
    xscroll.config(command=chose_listbox.xview)

    chose_listbox.bind("<<ListboxSelect>>", chose_listbox_show_msg)

    chose_listbox.pack(side=TOP, expand=YES, fill=X, anchor=CENTER)
    chosearea.pack(side=TOP, expand=NO, fill=Y, anchor=CENTER)

    bottombar = Frame(offline_window, width=640, height=72)
    gotopng = PhotoImage(file=where_script+'/UI/goto.png')
    button_next = Button(bottombar, image=gotopng, relief=FLAT, cursor='hand2', command=button_next_click)
    button_next.pack(side=BOTTOM, expand=NO, fill=NONE, anchor=CENTER)

    bottombar.pack(side=BOTTOM, expand=YES, fill=BOTH)
    offline_window.mainloop()
    root.withdraw()


# 按钮 发布句子 被单击
def button_write_click():
    try:
        get.get()
    except:
        tkinter.messagebox.showerror('获取模组', '出……出错啦 TAT\n请检查配置/网络再试一次？\n(ㅅ´ ˘ `)♡~')
        # 此处可能有一bug：即使无网络仍然显示发布句子窗口——也许编译运行时不会出现？待查。2017/7/18
    # 进行抓取操作，执行/Mypackage/get.py

    def button_back_click():
        write_window.destroy()
        root.deiconify()
        root.update()
        return

    # 获取listbox里的内容
    def chose_listbox_show_msg(event):
        print(chose_listbox.get(chose_listbox.curselection()))
        chose_sentence = chose_listbox.get(chose_listbox.curselection())
        return chose_sentence

    # 按钮 下一步 被单击
    def button_next_click():
        backup.backup()
        # 执行/Mypackage/backup.py ，进行备份操作
        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()
        # 获取设置内容

        if setting_json["mode"] == 'juzimi':
            f = codecs.open(where_script+'/data/today.txt', 'wb', 'utf-8')
            f.write(chose_listbox_show_msg('event')[:-2])  # 为什么是截取-2? 答:去掉原来的换行符
            f.close()
        elif setting_json["mode"] == 'zuowennote':
            f = codecs.open(where_script+'/data/today.txt', 'wb', 'utf-8')
            f.write(chose_listbox_show_msg('event'))
            f.close()

        final_window = Toplevel()
        center_window(final_window, 900, 500)
        final_window.overrideredirect(1)
        # 终焉窗口，即最后的展示窗口

        def button_back_click():
            final_window.destroy()
            write_window.deiconify()
            write_window.update_idletasks()
            write_window.update()
            return

        def button_finish_click():
            f = open(where_script+'/data/setting.json', 'r')
            setting_json = json.load(f)
            f.close()

            if not os.path.exists(where_script + '/output/%(year)s' % {'year': nowyear}):
                os.makedirs(where_script + '/output/%(year)s' % {'year': nowyear})
            if not os.path.exists(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}):
                f = codecs.open(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}, 'wb', 'utf-8')
                f.close()
            # 判断当月文件是否存在，不存在则创建

            if setting_json["mode"] == 'juzimi':

                f = codecs.open(where_script + '/data/today.txt', 'r', 'utf-8')
                sentence_output = f.read()
                f.close()

                output = codecs.open(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}, 'ab', 'utf-8')
                output.write(nowyear + '年' + nowmonth + '月' + nowday + '日' + '\r\n')
                output.write(sentence_output + '\r\n')
                output.write('\r\n')
                output.close()

                allhistory = codecs.open(where_script+'/data/allhistory.txt', 'ab', 'utf-8')
                allhistory.write(sentence_output + '\r\n')
                allhistory.close()

                cache_former = codecs.open(where_script+'/cache/sentence.txt', 'r', 'utf-8')
                sentence_get_file = codecs.open(where_script+'/data/sentenceget.txt', 'r', 'utf-8')

                allhistoryfile = codecs.open(where_script+'/data/allhistory.txt', 'r', 'utf-8')
                allhistory = []
                for line in allhistoryfile:
                    line = line.replace('\n','')
                    line = line.replace('\r','')
                    line = line.replace('\r\n','')
                    line = line.replace('\ufeff', '')
                    allhistory.append(line)
                allhistoryfile.close()

                cache = []
                for line in sentence_get_file:
                    line = line.replace('\r', '')
                    line = line.replace('\n', '')
                    line = line.replace('\r\n', '')
                    line = line.replace('\ufeff', '')
                    if line != sentence_output:
                        if line not in allhistory:
                            cache.append(line + '\r\n')


                for line in cache_former :
                    line = line.replace('\r', '')
                    line = line.replace('\n', '')
                    line = line.replace('\r\n', '')
                    line = line.replace('\ufeff', '')

                    if line not in allhistory:
                        if (line + '\r\n') not in cache:
                            cache.append(line + '\r\n')


                cache_file = codecs.open(where_script+'/cache/sentence.txt', 'wb', 'utf-8')
                for line in cache:
                    cache_file.write(line)
                cache_file.close()

                cache_former.close()
                sentence_get_file.close()

                f = open(where_script+'/data/setting.json', 'r')
                setting_json = json.load(f)
                f.close()
                if setting_json["once"] == "on":
                    f = open(where_script+'/data/uselog', 'w')
                    f.write(nowdate)
                    f.close()
                    # 使用记录。免得有人手贱，不回档还一天跑两回。

                print('存储完成，感谢使用。')
                root.quit()
                sys.exit(0)

            elif setting_json["mode"] == 'zuowennote':
                f = codecs.open(where_script+'/data/today.txt', 'r', 'utf-8')
                sentence_output = f.read()
                f.close()

                guidance_output = guidance_str

                output = codecs.open(where_script + '/output/%(year)s/%(month)s月.txt' % {'year': nowyear, 'month': nowmonth}, 'ab', 'utf-8')
                output.write(nowyear + '年' + nowmonth + '月' + nowday + '日' + '\r\n')
                output.write(sentence_output + '\r\n')
                output.write('（' + guidance_output + '）\r\n')
                output.write('\r\n')
                output.close()

                allhistory = codecs.open(where_script+'/data/zuowennote_allhistory.json', 'r', 'utf-8')
                allhistory_json = json.load(allhistory)
                print(allhistory_json)
                allhistory.close()

                f = codecs.open(where_script+'/data/zuowennote_get.json', 'r', 'utf-8')
                zuowennote_json = json.load(f)
                f.close()

                for sentencejson in zuowennote_json:
                    zuowennote_sentence = sentencejson["title"]
                    print(zuowennote_sentence)
                    print(sentencejson)
                    if zuowennote_sentence == sentence_str:
                        allhistory_json.append(sentencejson)
                        print(allhistory_json)
                        allhistory = codecs.open(where_script+'/data/zuowennote_allhistory.json', 'wb', 'utf-8')
                        json.dump(allhistory_json, allhistory, indent=4, ensure_ascii=False)
                        allhistory.close()
                        break
                    else:
                        pass

                f = open(where_script+'/data/setting.json', 'r')
                setting_json = json.load(f)
                f.close()
                if setting_json["once"] == "on":
                    f = open(where_script+'/data/uselog', 'w')
                    f.write(nowdate)
                    f.close()
                # 使用记录。免得有人手贱，不回档还一天跑两回。
                print('存储完成，感谢使用。')
                root.quit()
                sys.exit(0)

            return

        topbar = Frame(final_window)
        backpng = PhotoImage(file=where_script+'/UI/back2.png')
        button_back = Button(topbar, image=backpng, relief=FLAT, cursor='hand2', command=button_back_click)
        button_back.grid(row=1, column=1, sticky=W)

        f = codecs.open(where_script+'/data/today.txt', 'r', 'utf-8')
        sentencedata = f.read()
        f.close()

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()

        if setting_json["mode"] == 'juzimi':
            sentence_str = sentencedata[:sentencedata.find('——')]
            if sentencedata.find('《') == -1:
                writer_str = sentencedata[sentencedata.rfind('——') + 2:]
                book_str = ''
            else:
                writer_str = sentencedata[sentencedata.rfind('——') + 2:sentencedata.rfind('《')]
                book_str = sentencedata[sentencedata.rfind('《'):sentencedata.rfind('》') + 1]
        elif setting_json["mode"] == 'zuowennote':
            book_str = ''
            sentence_str = sentencedata[:sentencedata.find('——')]
            # print('sentence_str=' + sentence_str)
            writer_str = sentencedata[sentencedata.rfind('——') + 2:]
            if writer_str.find('『') != -1:
                book_str = writer_str
                writer_str = ''
            f = codecs.open(where_script+'/data/zuowennote_get.json', 'r', 'utf-8')
            zuowennote_json = json.load(f)
            f.close()
            for sentencejson in zuowennote_json:
                zuowennote_sentence = sentencejson["title"]
                # print('zuowennote_sentence=' + zuowennote_sentence)
                if zuowennote_sentence == sentence_str:
                    guidance_str = sentencejson["content"]
                else:
                    pass


        if book_str == '':
            writer = StringVar()
            writer.set(writer_str)
            writer_label = Label(topbar, textvariable=writer, font=('思源宋体 CN SemiBold', 28), justify=LEFT, anchor=S)
            writer_label.grid(row=1, column=2, sticky=W)

            said = StringVar()
            said.set('曾经说过：')
            said_label = Label(topbar, textvariable=said, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
            said_label.grid(row=1, column=3, sticky=W)

            topbar.pack(side=TOP, expand=YES, fill=X)

        else:
            if len(writer_str + book_str) < 17:
                writer = StringVar()
                writer.set(writer_str)
                writer_label = Label(topbar, textvariable=writer, font=('思源宋体 CN SemiBold', 28), justify=LEFT, anchor=S)
                writer_label.grid(row=1, column=2, sticky=W)

                zai = StringVar()
                zai.set('在')
                zai_label = Label(topbar, textvariable=zai, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                zai_label.grid(row=1, column=3, sticky=W)

                book = StringVar()
                book.set(book_str)
                book_label = Label(topbar, textvariable=book, font=('思源宋体 CN Medium', 24), justify=LEFT, anchor=S)
                book_label.grid(row=1, column=4, sticky=W)

                said = StringVar()
                said.set('中曾经有过：')
                said_label = Label(topbar, textvariable=said, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                said_label.grid(row=1, column=5, sticky=W)
                topbar.pack(side=TOP, expand=YES, fill=X)
            else:
                writerbar = Frame(topbar)
                writer = StringVar()
                writer.set(writer_str)
                writer_label = Label(writerbar, textvariable=writer, font=('思源宋体 CN SemiBold', 28), justify=LEFT,
                                     anchor=S)
                writer_label.grid(row=1, column=1, sticky=W)
                zai = StringVar()
                zai.set('在')
                zai_label = Label(writerbar, textvariable=zai, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                zai_label.grid(row=1, column=2, sticky=W)
                writerbar.grid(row=1, column=2, sticky=W)

                bookbar = Frame(topbar)
                book = StringVar()
                book.set(book_str)
                book_label = Label(bookbar, textvariable=book, font=('思源宋体 CN Medium', 24), justify=LEFT, anchor=S)
                book_label.grid(row=1, column=1, sticky=W)
                said = StringVar()
                said.set('中曾经有过：')
                said_label = Label(bookbar, textvariable=said, font=('思源黑体 CN ExtraLight', 18), justify=LEFT, anchor=S)
                said_label.grid(row=1, column=2, sticky=W)
                bookbar.grid(row=2, column=2, sticky=W)

                topbar.pack(side=TOP, expand=YES, fill=X)

        bottombar = Frame(final_window, width=640, height=72)
        finishpng = PhotoImage(file=where_script+'/UI/finish.png')
        button_finish = Button(bottombar, image=finishpng, relief=FLAT, cursor='hand2', command=button_finish_click)
        button_finish.pack(side=BOTTOM, expand=NO, fill=NONE, anchor=CENTER)

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()
        if setting_json["mode"] == 'juzimi':
            label_comefrom = Label(bottombar, text='内容来源：句子迷', font=('思源黑体 CN Regular', 8),
                                   justify=CENTER, anchor=CENTER)
            label_comefrom.pack(side=TOP, expand=NO, fill=NONE, anchor=CENTER)
        elif setting_json["mode"] == 'zuowennote':
            label_comefrom = Label(bottombar, text='内容来源：作文纸条', font=('思源黑体 CN Regular', 8),
                                   justify=CENTER, anchor=CENTER)
            label_comefrom.pack(side=TOP, expand=NO, fill=NONE, anchor=CENTER)
        else:
            pass

        bottombar.pack(side=BOTTOM, expand=YES, fill=BOTH)

        f = open(where_script+'/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()

        if setting_json["mode"] == 'juzimi':
            juzimibar = Frame(final_window, width=756)
            sentence_text = ScrolledText(juzimibar, relief=FLAT, font=('思源宋体 CN Heavy', 28), width=35, bd=0,
                                 bg='#f0f0f0')
            sentence_text.insert(END, sentence_str)
            sentence_text.pack(side=LEFT, expand=NO, fill=NONE, anchor=CENTER)
            juzimibar.pack(side=TOP, expand=NO, fill=NONE)



        elif setting_json["mode"] == 'zuowennote':
            zuowennotebar = Frame(final_window)

            zuowennote_sentencebar = Frame(zuowennotebar)
            sentence_text = Text(zuowennote_sentencebar, relief=FLAT, font=('思源宋体 CN Heavy', 28), height=3,
                                 width=38, bd=0, bg='#f0f0f0')
            sentence_text.insert(END, sentence_str)
            sentence_text.pack(side=TOP, expand=YES, fill=X, anchor=CENTER, padx=20)
            zuowennote_sentencebar.grid(row=1, column=1, sticky=W)

            zuowennote_guidebar = Frame(zuowennotebar)
            guidance_text = ScrolledText(zuowennote_guidebar, relief=FLAT, font=('思源黑体 CN Regular', 16),  # height=6,
                                         width=70, bd=0, bg='#f0f0f0')
            guidance_text.insert(END, guidance_str)
            guidance_text.pack(side=TOP, expand=YES, fill=Y, anchor=CENTER, padx=20)

            zuowennote_guidebar.grid(row=2, column=1, sticky=W)

            zuowennotebar.pack(side=TOP, expand=YES, fill=Y)

        # 朗读功能
        f = open(where_script + '/data/setting.json', 'r')
        setting_json = json.load(f)
        f.close()
        if setting_json["speech"] == 'on':
            if writer_str == '':
                speak_sentence = '在' + book_str + '中曾经有过：' + sentence_str
            elif writer_str != '':
                if book_str == '':
                    speak_sentence = writer_str + '曾经说过：' + sentence_str
                else:
                    speak_sentence = writer_str + '在' + book_str + '中曾经有过：' + sentence_str
            else:
                speak_sentence = sentence_str
            threads = []
            t1 = threading.Thread(target=spvoice.say, args=(speak_sentence,))
            threads.append(t1)
            if __name__ == '__main__':
                for t in threads:
                    t.setDaemon(True)
                    t.start()

        final_window.mainloop()
        write_window.withdraw()
        return

    write_window = Toplevel()
    center_window(write_window, 640, 400)
    write_window.overrideredirect(1)
    topbar = Frame(write_window, width=640, height=72)
    backpng = PhotoImage(file=where_script+'/UI/back2.png')
    button_back = Button(topbar, image=backpng, relief=FLAT, cursor='hand2', command=button_back_click)
    button_back.grid(row=1, column=1, sticky=W)

    writemessage = StringVar()
    writemessage.set('选择你想发布的新鲜句子')
    label = Label(topbar, textvariable=writemessage, font=('思源黑体 CN Light', 28), justify='center', anchor='center')
    label.grid(row=1, column=2, sticky=W)
    topbar.pack(side=TOP, expand=NO, fill=X)

    chosearea = Frame(write_window, width=500, height=100)
    yscroll = Scrollbar(chosearea)
    yscroll.pack(side=RIGHT, anchor=CENTER, fill=Y)
    xscroll = Scrollbar(chosearea, orient=HORIZONTAL)
    xscroll.pack(side=BOTTOM, anchor=CENTER, fill=X)
    chose_listbox = Listbox(chosearea, font=('思源黑体 CN Regular', 12), width=50, bg='#f0f0f0', bd=0,
                            yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

    f = open(where_script+'/data/setting.json', 'r')
    setting_json = json.load(f)
    f.close()

    if setting_json["mode"] == 'juzimi':
        f = codecs.open(where_script+'/data/sentenceget.txt', 'r', 'utf-8')
        for line in f:
            chose_listbox.insert(END, line)
        f.close()

    elif setting_json["mode"] == 'zuowennote':
        f = codecs.open(where_script+'/data/zuowennote_get.json', 'r', 'utf-8')
        zuowennote_json = json.load(f)
        f.close()
        for sentencejson in zuowennote_json:
            # print(sentencejson)
            zuowennote_sentence = sentencejson["title"]
            zuowennote_writer = sentencejson["author"]
            if sentencejson["content"] == '':
                pass
            elif zuowennote_writer.find('纸条') != -1 or zuowennote_writer.find('迢遥旧梦') != -1 or \
                            zuowennote_writer.find('小胖纸') != -1 or zuowennote_writer.find('铝汉纸') != -1:
                pass
            else:
                chose_listbox.insert(END, zuowennote_sentence + '——' + zuowennote_writer)


    yscroll.config(command=chose_listbox.yview)
    xscroll.config(command=chose_listbox.xview)

    chose_listbox.bind("<<ListboxSelect>>", chose_listbox_show_msg)

    chose_listbox.pack(side=TOP, expand=YES, fill=X, anchor=CENTER)
    chosearea.pack(side=TOP, expand=NO, fill=Y, anchor=CENTER)

    bottombar= Frame(write_window, width=640, height=72)
    gotopng = PhotoImage(file=where_script+'/UI/goto.png')
    button_next = Button(bottombar, image=gotopng, relief=FLAT, cursor='hand2', command=button_next_click)
    button_next.pack(side=BOTTOM, expand=NO, fill=NONE, anchor=CENTER)

    bottombar.pack(side=BOTTOM, expand=NO, fill=X)

    write_window.mainloop()
    root.withdraw()

    return


# 以下是root窗口，即初始界面
root = Tk()
center_window(root, 640, 400)
root.overrideredirect(1)
root.wm_title('每日名句获取器')

topbar = Frame(root, width=640, height=72)
exitpng = PhotoImage(file=where_script+'/UI/exit.png')
button_exit = Button(topbar, image=exitpng, relief=FLAT, cursor='hand2',command=button_exit_click)
button_exit.pack(side=TOP, expand=NO, fill=NONE, anchor=E)
topbar.pack(side=TOP, expand=NO, fill=X)

top = Frame(root, width=640, height=100)
label = Label(top, text='每日名句获取器', font=('思源黑体 CN ExtraLight', 48),justify='center', anchor='center')
label.pack(side=TOP, expand=NO, fill=Y)
dateinfo = StringVar()
label2 = Label(top, textvariable=dateinfo, font=('思源黑体 CN Regular', 14), justify='center', anchor='center')
if setting_json["countdown"] == "on":
    countdown_days = (datetime.date(int(nowyear), 6, 7) - datetime.date(int(nowyear), int(nowmonth), int(nowday))).days
    if countdown_days < 0:
        countdown_days = (
        datetime.date(int(nowyear) + 1, 6, 7) - datetime.date(int(nowyear), int(nowmonth), int(nowday))).days
    dateinfo.set(nowdate + '\r' + '距离高考还有%s天' % countdown_days)
    label2['font'] = ('思源黑体 CN Regular', 12)
    label2['foreground'] = '#001A43'
else:
    dateinfo.set(nowdate)

label2.pack(side=BOTTOM, expand=YES, fill=BOTH)
top.pack(side=TOP, expand=YES, fill=BOTH)

# 六个按钮
buttons = Frame(root, width=180, height=180)
opendirpng = PhotoImage(file=where_script+'/UI/opendir.png')
button_opendir = Button(buttons, image=opendirpng, relief=FLAT, cursor='hand2', command=button_opendir_click)
button_opendir.grid(row=0, column=1, sticky="nsew")
quepng = PhotoImage(file=where_script+'/UI/que.png')
button_about = Button(buttons, image=quepng, relief=FLAT, cursor='hand2', command=button_about_click)
button_about.grid(row=0, column=2, sticky="nsew")
settingpng = PhotoImage(file=where_script+'/UI/setting.png')
button_setting = Button(buttons, image=settingpng, relief=FLAT, cursor='hand2', command=button_setting_click)
button_setting.grid(row=0, column=3, sticky="nsew")
mailpng = PhotoImage(file=where_script+'/UI/mail.png')
button_mail = Button(buttons, image=mailpng, relief=FLAT, cursor='hand2', command=button_mail_click)
button_mail.grid(row=0, column=4, sticky="nsew")
neterrorpng = PhotoImage(file=where_script+'/UI/neterror.png')
button_offline = Button(buttons, image=neterrorpng, relief=FLAT, cursor='hand2', command=button_offline_click)
button_offline.grid(row=0, column=5, sticky="nsew")
writepng = PhotoImage(file=where_script+'/UI/write.png')
button_write = Button(buttons, image=writepng, relief=FLAT, cursor='hand2', command=button_write_click)
button_write.grid(row=0, column=6, sticky="nsew")


# 六个标签
label_opendir = Label(buttons, text='输出目录', font=('思源黑体 CN Regular', 12), justify='center', anchor='center')
label_opendir.grid(row=1, column=1)
label_about = Label(buttons, text='关于', font=('思源黑体 CN Regular', 12), justify='center', anchor='center')
label_about.grid(row=1, column=2)
label_setting = Label(buttons, text='设置', font=('思源黑体 CN Regular', 12), justify='center', anchor='center')
label_setting.grid(row=1, column=3)
label_mail = Label(buttons, text='发送邮件', font=('思源黑体 CN Regular', 12), justify='center', anchor='center')
label_mail.grid(row=1, column=4)
label_offline = Label(buttons, text='离线模式', font=('思源黑体 CN Regular', 12), justify='center' ,anchor='center')
label_offline.grid(row=1, column=5)
label_write = Label(buttons, text='发布句子', font=('思源黑体 CN Regular', 12), justify='center', anchor='center')
label_write.grid(row=1, column=6)
buttons.pack(side=TOP, expand=YES, fill=Y)


if setting_json["once"] == "on":
    f = open(where_script+'/data/uselog', 'r')
    uselog = f.read()
    f.close()
    if uselog == nowdate:
        button_offline['state'] = DISABLED
        button_write['state'] = DISABLED
        dateinfo.set('今日已运行过！')
        label2['font'] = ('思源黑体 CN Regular', 14)
        label2['foreground'] = '#EB6159'
    else:
        pass
# 每日一次模式。

bottom = Frame(root, width=640, height=50, cursor='heart')
label3 = Label(bottom, text='F.B. Made With ♥  2017-8  V' + setting_json['version']
               , font=('思源黑体 CN Light', 10), justify='center', anchor='center')
label3.pack(side=TOP, expand=NO, fill=Y)
label4 = Label(bottom,text='Powered by Python3 & Tkinter. 内容取自互联网，不代表程序编写者的立场。'
               , font=('思源黑体 CN Light', 8), justify='center', anchor='center')
label4.pack(side=TOP, expand=YES, fill=Y)
bottom.pack(side=BOTTOM, expand=YES, fill=Y)

try:
    latest_version = check_update()
    if setting_json['version'] != latest_version:
        nv = setting_json['version'].split('.')  # nv:now_version
        lv = latest_version.split('.')  # lv:latest_version
        nvX = int(nv[0])  # nvX:now_version's MAJOR version
        nvY = int(nv[1])  # nvY:now_version's MINOR version
        nvZ = int(nv[2])  # nvZ:now_version's PATCH version
        lvX = int(lv[0])
        lvY = int(lv[1])
        lvZ = int(lv[2])
        # print(nvX,nvY,nvZ)
        # print(lvX,lvY,lvZ)
        def update_messagebox():
            if tkinter.messagebox.askyesno("版本更新",
                                           "当前版本是%(nowversion)s\n最新版本是%(newversion)s\n要不要更新一下试试呢？"
                                                   % {'nowversion': setting_json['version'],
                                                      'newversion': latest_version}) is True:
                webbrowser.open('https://github.com/Foldblade/EORS/releases')
            return
        if nvX <= lvX:
            if nvX == lvX:
                if nvY > lvY:
                    pass
                elif nvY == lvY:
                    if nvZ >= lvZ:
                        pass
                    else:
                        update_messagebox()
                else:
                    update_messagebox()
            else:
                update_messagebox()
# 总觉得这检查更新的写法好不简洁……啊啊啊啊啊啊orz
except:
    pass


root.mainloop()
