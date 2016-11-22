#\usr\bim\python
#coding=utf-8


import time,os,re,subprocess,telnetlib
import threading
host = '10.255.248.76'
username = 'admin'
password = 'zhongshi2016'
finish = 'bin->'
commandname = 'ipclog 3'
logpath=r'D:\telnet17230.txt'
logpath1=r'D:\ping_ipc.txt'

def ping_ipc(host):
    fileping=open(logpath1,'a')
    i=0
    while i<5:
        p = subprocess.Popen(["ping.exe ", host],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True) 
        p.wait()
        pinglog =p.stdout.read()
        print pinglog
        fileping.write(pinglog)
        fileping.flush()#没有关系
    fileping.close()

def telnet_ipc(host,username,password,finish,commandname):
    tn = telnetlib.Telnet(host,port=17230,timeout=10)
    #tn.set_debuglevel(2)
    time.sleep(1)
    tn.open(host,port=17230)
    tn.read_until("Username:",timeout=2)
    tn.write(username+ "\r\n")
    time.sleep(1)
    tn.read_until("Password:")
    tn.write(password+ "\r\n")
    time.sleep(2)

    tn.write(commandname+"\r\n")

    fileHandle=open(logpath,'a')
    j=0
    while j<5:
        #tn.read_some()
        #time.sleep(2)
        klog=tn.read_very_eager()
        print klog 
 
        #写入日志
        fileHandle.write(klog)
        fileHandle.flush()#没有关系
    fileHandle.close()

def ping_telnet():
    threads = []
    t1 = threading.Thread(target=ping_ipc,args=(host,))
    threads.append(t1)
    t2 = threading.Thread(target=telnet_ipc,args=(host,username,password,finish,commandname,))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print "all is over"
if __name__ =='__main__':
    ping_telnet()
