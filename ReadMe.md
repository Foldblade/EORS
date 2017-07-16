# EORS-Everyday One Rhesis System-每日名句获取器

1. 本程序[在Github开源](https://github.com/foldblade/EORS)。
2. 本程序所抓取内容来自[句子迷](http://www.juzimi.com)、[作文纸条](https://itunes.apple.com/cn/app/%E4%BD%9C%E6%96%87%E7%BA%B8%E6%9D%A1/id1207254643)，为满足每日名句的选择和数字化、日志化而编写，不代表程序编写者的立场。  

下载请移步release。
本程序版本：1.1 。感谢使用。

To English User：  
This programme was designed for Chinese users only.  
(But if you want to learn Chinese , you may try it ! )  
I won't add the support of any other languages.  
Thank you.  

F.B. 2017-7  

***

## 使用说明

为了显示效果，需要安装以下两款基于 SIL Open Font License 1.1 的开源字体，请查阅官网和Github了解更多。  
您可以选择不安装，这样程序将会默认以宋体显示。本人非常不建议用这种方式体验`EORS-每日名句获取器`。  

**[思源黑体 | Source Han Sans](http://adobe.ly/SourceHanSans)**  
官方网址：http://adobe.ly/SourceHanSans  
Github：https://github.com/adobe-fonts/source-han-sans  
所需字体下载地址：https://github.com/adobe-fonts/source-han-sans/blob/release/SubsetOTF/SourceHanSansCN.zip?raw=true

**[思源宋体 | Source Han Serif ](http://adobe.ly/SourceHanSerif)**  
官方网址：http://adobe.ly/SourceHanSerif  
Github：https://github.com/adobe-fonts/source-han-serif  
所需字体下载地址：https://github.com/adobe-fonts/source-han-serif/blob/release/SubsetOTF/SourceHanSerifCN.zip?raw=true

### 配置
如果您是初次使用，请先进行配置。

#### 配置管理密码
您可以跳过此步。若不配置，无法进行“回到昨日”操作。
1. 打开“管理密码修改器”文件夹。
2. 双击admin-passwd.exe。
3. 里面有适用于普通人类的提示。请按提示操作。
4. 复制生成的passwd文件到/safety 文件夹下，覆盖。

#### 配置邮件服务
您可以跳过此步。若不配置，无法使用“发送邮件”功能。
这一步需要你明白/拥有如下内容：
* 什么是SMTP
* 支持SMTP的邮件账户
* Notepad++编辑器

如果您不知道，也不会进行搜索，我建议您立刻关闭本“给普通人类的用户指南”：电脑很危险，关机保平安。  
请选用我内定、钦点的Notepad++作为编辑器。  
下载地址:https://notepad-plus-plus.org/download
1. 进入 Modules 文件夹。
2. 用 Notepad++ 打开 mailsetting.json 。
您可能看到如下内容：
```
{
    "smtp_host":"smtp.host.com",
    "smtp_user":"service1@email.com",
    "smtp_passwd":"your_smtp_password",
    "smtp_port":465,
    "sender":"service1@email.com",
    "receivers":[
        "email1@email.net",
        "email2@email.com"
    ]
}
```
在此给出Python格式的注释（‘#’）。请按注释修改，请不要直接复制。  
若怕修改有误，请搜索“json校验”，复制修改内容。校验通过后，再粘贴回来。
```
{
    "smtp_host":"smtp.host.com",  # 您的SMTP主机
    "smtp_user":"service1@email.com", # 您的SMTP账户
    "smtp_passwd":"your_smtp_password", # 您的SMTP密码
    "smtp_port":465, # 您的SMTP主机端口
    "sender":"service1@email.com", # 发件人，建议填写发件邮箱
    "receivers":[
        "email1@email.net", # 收件人，支持多人，中间用逗号隔开。
        "email2@email.com" # 如果只要一人，中括号内只需填写那个人的邮箱地址
    ]
}
```

#### 一般设置
运行每日名句获取器.exe。您可以在设置中进行设置。  
您可以跳过此步。默认关闭每日一次功能、使用句子迷模式。

### 输出
我们会整理好txt作为输出。  
您可以在 /output 文件夹中看到它们。

***

## 更新日志

### V1.1（Py-Tkinter 0.2）
* 被人推荐了个应用，叫[作文纸条](https://itunes.apple.com/cn/app/%E4%BD%9C%E6%96%87%E7%BA%B8%E6%9D%A1/id1207254643)，觉得“欸这个不错欸！”
* 于是就在1.0的基础上加了对作文纸条的支持。您现在可以在设置里设置选用的模式：句子迷，或者作文纸条。

### V1.0（Py-Tkinter 0.1）
* 终于，我选择了Python的Tkinter来完成GUI，并用Python彻底重写。
* 了却了多年以来的一点点小小心愿：用纯英文的编程语言写一个GUI程序。
* 了却了V0.3.2的一点点小小心愿
* 可能UI没有易语言版本好看……如果可能的话，教练，我想学Pyqt！！

### ~~V0.5（VB-Py0.1）~~
* ~~喜大普奔！我终于完成了Windows10下 Visual Basic的安装！于是这是Visual Basic与Python结合的第一版！~~
* ~~了却了V0.3.2的一点点小小心愿~~
* ~~上面两行就是废话，这版做了一天就被抛弃了~~

### V0.4.2 
* 一个被搁浅的版本
* 一个被放弃的版本
* 用4个Python组件取代了部分原功能

### V0.4.1
* 添加一个基于Python的组件
* 修复bug 2处

### V0.4
* 懒癌患者又更新啦！
* 删掉了“PPT发布”这个FLAG
* 加了个彩蛋
* 写了一点点发送邮件的部分

### V0.3.2
* 紧急修复在发布界面不小心压到键盘导致的无限存档bug
* **计划在完成基本功能后停止更新，转向其他语言重做**

### V0.3.1
* UI重设计
* 紧急修复V0.2 built3的一大bug

### V0.2.3
* 支持备份（自动）
* 支持“回到昨天”

### V0.2.2
* 支持安全保护，每日仅可运行一次

### V0.2
* 支持一次抓取多句
* 支持选取句子发布
* 支持未被选取的句子加入缓存日志（离线使用）

### V0.1
* 程序成功抓取句子了！！
* 抓到的句子可以读出来了！
* 抓到的句子可以被记录在日志文件了！
* 哎哟学校断网了完全不能用了orz

