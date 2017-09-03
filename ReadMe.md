# 每日名句获取器-EORS-Everyday One Rhesis System

1. 本程序[在Github开源](https://github.com/foldblade/EORS)。
2. 本程序所抓取内容来自[句子迷](http://www.juzimi.com)、[作文纸条](https://itunes.apple.com/cn/app/%E4%BD%9C%E6%96%87%E7%BA%B8%E6%9D%A1/id1207254643)，为满足高中语文学习时每日名句的选择和数字化、日志化而编写，不代表程序编写者的立场。  

To English User：  
This programme was designed for Chinese users only.  
(But if you want to learn Chinese , you may try it ! )  
I won't add the support of any other languages.  
Thank you.  

F.B. 2017-7  

***
## 开发缘由
那天，语文老师说：“隔壁的Ⅸ班每天都在黑板上写一句名句作为积累，我觉得这很好，我们班也要这么做。”  
课代表领旨而去。自然，前几天不会有人去抄在本子上。鄙人作为电教管理员，每日将名句记在班级电脑里，然后周末给全班发送邮件。  
刚过去三天，我就受不了了。和语文课代表夸下海口，说“能写一个程序，省得你不知道找什么 ~~（我每天跟着码字也累的要死）~~ 。”  
“好呀!”  
我就滚去写代码了。熬夜三晚，事毕。这就是v0.1。  
结果，用了两天，学校断网。课代表又写了一周名句。我又熬夜一周。然后就有了v0.2。
日后就进行了一点小修小补。很抱歉，做了一点微小的工作。  

## 功能介绍
* 从互联网上寻找名句供您选择（联网使用一次后即可在一段时间内使用缓存模式离线使用）
* 选择完成后可以用大号字体显示在电脑上发布（请配合投影使用）
* 完成后自动保存到日志文件
* 配置邮件服务器后，鼠标轻轻一点，当月句子即一键发送到邮箱
* 防止有人手贱，支持开启每日仅运行一次的模式，还可自动备份、“回到昨日”

## 更新日志
### V1.2.1
* 修复： 
    * mail_helper.py 和 邮件配置助手.exe ；admin-passwd.py 和 管理密码修改器.exe 因为V1.2.0写了 `.gitignore` 造成了一点影响。 
	* 自动更新部分修正。

### V1.2.0
* 新增：
    * 朗读模式   
    现在已经可以朗读出发布的句子啦！您可以在设置界面中进行设置。
    * 自动更新  
    新增了自动检查release版本更新的功能。
* 更改：
    * /output 目录下的文件层次，X月.txt放在当前年份文件夹下，如： /output/2017/9月.txt。
    * /Modules 改名 /Mypackage，进行一点小修小补。
* 还有其他的一点点小修小补

### V1.1.2
* 新增：在无网络模式下进行“发布句子”的错误提示

### V1.1.1
* 新增：输出目录按钮、邮件配置助手
* 更改：管理密码修改器
* 修复：为了适应exe发布而进行了一些修复

### V1.1
* 被人推荐了个应用，叫[作文纸条](https://itunes.apple.com/cn/app/%E4%BD%9C%E6%96%87%E7%BA%B8%E6%9D%A1/id1207254643)，觉得“欸这个不错欸！”
* 于是就在1.0的基础上加了对作文纸条的支持。您现在可以在设置里设置选用的模式：句子迷，或者作文纸条。

### V1.0
* 终于，我选择了Python的Tkinter来完成GUI，并用Python彻底重写。
* 了却了多年以来的一点点小小心愿：用纯英文的编程语言写一个GUI程序。
* 了却了V0.3.2的一点点小小心愿
* 可能UI没有易语言版本好看……如果可能的话，教练，我想学Pyqt！！

### ~~V0.5~~
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

