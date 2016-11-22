#\usr\bim\python
#coding=utf-8

import re,os,subprocess  
import datetime

host = "192.168.252.251"
log_ping_path=r'D:\ping_ipc.txt'


def ping_ipc(host):
    fileping=open(log_ping_path,'a')
    p = subprocess.Popen("ping -t %s"%host,
                         stdin = subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         shell=True)  

    while p.poll() == None:  
        now = datetime.datetime.now()
        nowprint=now.strftime('%Y-%m-%d  %H:%M:%S ')

        pingout = p.stdout.readline()
        print nowprint+pingout
        fileping.write(nowprint+pingout)
    #print p.stdout.read()     
    print 'returen code:', p.returncode

    fileping.close()
    
if __name__ =='__main__':
    ping_ipc(host)


#备注：此方法通过判断子进程的是否结束，然后逐行读取。
#subprocess:还有p.wait()用于等待进程结束后再输出结果；通过标准输出读出，stdout.redline
    
