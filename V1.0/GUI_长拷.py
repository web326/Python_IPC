#\usr\bim\python
#coding=utf-8

from Tkinter import *
import time,sys,os
from F01day_night import test01
from F02test import test02
from F03test import test03
import ConfigParser
import threading

cf = ConfigParser.ConfigParser()
cf.read(r'Config.py')
host = cf.get("common","host")
username = cf.get("common","username")
password = cf.get("common","password")
profileDir = cf.get("profiledir","profileDir")

def choice_value():
    value=v.get()
    cf = ConfigParser.ConfigParser()
    cf.read(r'Config.py')
    cf.set("gui","choice_value",str(value))
    cf.write(open(r'Config.py', "w"))
    choice_value = cf.get("gui","choice_value")
    #print choice_value.decode('UTF-8').encode('GBK') 
def changkao_item():
    changkao = [test01,test02,test03]
    #调用函数不需要加引号
    cf = ConfigParser.ConfigParser()
    cf.read(r'Config.py')
    value = cf.get("gui","choice_value")
    print value
    print changkao[int(value)-1] 
    changkao[int(value)-1]()

####创建单独线程#######
#t=threading.Thread(target=ping_ipc)
#def ping_func():
#    t.setDaemon(True)
#    t.start()



t=threading.Thread(target=changkao_item)
def changkao_func():
    ping_return=os.system('ping -n 4 -w 1 %s'%host) #每个ip ping2次，等待时间为1s 
    if ping_return: 
        ping_out= str('ping %s is fail'%host) #需要考虑如何显示在GUI上面
        test_out.set(ping_out)
        return
    else: 
        ping_out=str('ping %s is ok'%host) #需要考虑如何显示在GUI上面
        test_out.set(ping_out)

    t.setDaemon(True)
    t.start()

root = Tk()
root.title("KIPC长拷自动化测试")
root.geometry('650x500')
root.resizable(width=False,height=True)

#Label(root,text="欢迎使用KIPC长拷自动化测试",height= "3",width="30",font=("Arial",20)).grid(row=0)
Label(root,text="欢迎使用KIPC长拷自动化测试",height= "1",font=("Arial",18)).grid(row=0,column=0,columnspan=7,rowspan=1,sticky=W+E+N+S)

#设置长拷项
Label(root,text="长拷项选择",height= "1",font=("Arial",14)).grid(row=1,column=0,columnspan=7,rowspan=1,sticky=NW)
v=IntVar()
Label(root,text="",).grid(row=2,column=0,columnspan=1,rowspan=4,ipadx=20)
##通过v.get获取value的值
Radiobutton(root,text = "日夜切换长拷和后台自动化",variable=v,value=1,command=choice_value).grid(row=2,column=1,columnspan=2,sticky=NW)
Radiobutton(root,text = "日夜切换长拷和后台自动化",variable=v,value=2,command=choice_value).grid(row=2,column=3,columnspan=2,sticky=NW)
Radiobutton(root,text = "分辨率切换长拷和后台自动化",variable=v,value=3,command=choice_value).grid(row=2,column=5,columnspan=2,sticky=NW)
Radiobutton(root,text = "后台自动化(批量且且无功能长拷)",variable=v,value=4,command=choice_value).grid(row=3,column=1,columnspan=2,sticky=NW)
Radiobutton(root,text = "简单恢复长拷和后台自动化",variable=v,value=5,command=choice_value).grid(row=3,column=3,columnspan=2,sticky=NW)
Radiobutton(root,text = "日夜切换长拷和后台自动化",variable=v,value=6,command=choice_value).grid(row=3,column=5,columnspan=2,sticky=NW)
Radiobutton(root,text = "分辨率切换长拷和后台自动化",variable=v,value=7,command=choice_value).grid(row=4,column=1,columnspan=2,sticky=NW)
Radiobutton(root,text = "后台自动化(批量且无功能长拷)",variable=v,value=8,command=choice_value).grid(row=4,column=3,columnspan=2,sticky=NW)

'''
#配置信息,目前未搞定如何将输入信息写入到配置文件中，所以暂缓。
Label(root,text="配置信息",height= "1",font=("Arial",14)).grid(row=5,column=0,columnspan=7,rowspan=1,sticky=NW)
Label(root,text="",).grid(row=6,column=0,columnspan=1,rowspan=2,ipadx=20)
Label(root, text="IP地址").grid(row=6,column=1,sticky=NW,)
Label(root, text="账号").grid(row=7,column=1,sticky=NW)
Label(root, text="密码").grid(row=7,column=3,sticky=NW)
Entry(root).grid(row=6,column=2,columnspan=4,sticky=NW,ipadx=97)
Entry(root).grid(row=7,column=2,sticky=NW)
Entry(root).grid(row=7,column=4,sticky=NW)
'''

#执行
Button(root, text="开始",width=8, height=1, font=('Arial', 20),command=changkao_func).grid(row=11,column=2,columnspan=2,sticky=NW)
Button(root, text="停止",width=8, height=1, font=('Arial', 20)).grid(row=11,column=4,columnspan=2,sticky=NW)
#,command=test_main

#打印信息
test_out = StringVar()
Label(root,textvariable=test_out,font=('Arial', 10)).grid(row=12,column=1,columnspan=7,rowspan=1,sticky=NW)

root.mainloop()

