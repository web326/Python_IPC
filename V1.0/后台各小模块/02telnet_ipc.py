#\usr\bim\python
#coding=utf-8


import time,os,re,threading,telnetlib,datetime

host = '10.255.248.76'
username = 'admin'
password = 'zhongshi2016'
finish = 'bin->'
commands = ['ipclog 3','ipclog 5']
#Cgi协议  cgiapplog 3 （255是全部）Vsip协议：vsiplog 3 （255是全部）Onvif协议：onvifapplog 3 （255是全部）
#Gb协议：sipapplog 3 （255是全部）rtsp协议  rtsplog 3 （255是全部）
#其他待补充
log_telnet_path=r'D:\telnet17230.txt'

def telnet_ipc(host,username,password,finish,commands):
    tn = telnetlib.Telnet(host,port=17230,timeout=10)
    tn.open(host,port=17230)
    tn.read_until("Username:",timeout=2)
    tn.write(username+ "\r\n")
    tn.read_until("Password:")
    tn.write(password+ "\r\n")

    for command in commands:  
        tn.write('%s\r\n' % command)  

    filetelnet=open(log_telnet_path,'a')
    j=0
    while j<5:
        time.sleep(2)#2秒取一次，否则一直在刷导致CPU和内存占用较多
        now = datetime.datetime.now()
        nowprint=now.strftime('%Y-%m-%d  %H:%M:%S ')
        telnetout=tn.read_very_eager()
        print nowprint+telnetout 
 
        #写入日志
        filetelnet.write(nowprint+telnetout)
        #filetelnet.flush()
    filetelnet.close()

if __name__ =='__main__':
    telnet_ipc(host,username,password,finish,commands)
