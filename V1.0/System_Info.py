#\usr\bim\python
#coding=utf-8

from ftplib import FTP
import time,os,re,subprocess,telnetlib,threading,socket
import datetime
import ConfigParser
import paramiko


cf = ConfigParser.ConfigParser()
cf.read(r'Config.py')
host = cf.get("common","host")
username = cf.get("common","username")
password = cf.get("common","password")
strcommands = cf.get("common","commands")
commands = strcommands.split(',')
finish = cf.get("common","finish")

log_ping_path=cf.get("common","log_ping_path")
log_system_path = cf.get("common","log_system_path")
log_telnet_path=cf.get("common","log_telnet_path")
log_run_path = cf.get("common","log_run_path")


if not os.path.exists('D:\\log_ck\\ping\\'):
    os.makedirs('D:\\log_ck\\ping\\')
if not os.path.exists('D:\\log_ck\\telnet17230\\'):
    os.makedirs('D:\\log_ck\\telnet17230\\')
if not os.path.exists('D:\\log_ck\\cpu\\'):
    os.makedirs('D:\\log_ck\\cpu\\')
if not os.path.exists('D:\\log_ck\\mem\\'):
    os.makedirs('D:\\log_ck\\mem\\')
if not os.path.exists('D:\\log_ck\\system\\'):
    os.makedirs('D:\\log_ck\\system\\')
if not os.path.exists('D:\\log_ck\\runlog\\'):
    os.makedirs('D:\\log_ck\\runlog\\')
else:
    pass
    print('目录已存在')

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
        #print nowprint+pingout
        fileping.write(nowprint+pingout)
    #print p.stdout.read()     
    print 'returen code:', p.returncode
    fileping.close()
    
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
        #print nowprint+telnetout 
 
        #写入日志
        filetelnet.write(nowprint+telnetout)
        #filetelnet.flush()
    filetelnet.close()

def ping_telnet():
    threads = []
    t1 = threading.Thread(target=ping_ipc,args=(host,))
    threads.append(t1)
    t2 = threading.Thread(target=telnet_ipc,args=(host,username,password,finish,commands,))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print "all is over"
    
def ssh_ipc(cmd):
    #print host,username,password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,22,username,password,timeout=5)
    for m in cmd:
        stdin, stdout, stderr = ssh.exec_command(m)
        out = stdout.readlines()
        x=type(out)
        #print 'sshout:'
        #print x
        for o in out:
            ver = o.strip('\n')
            #print ver
    return ver
    ssh.close()

def conf_verify(value,cmd):
    filerunlog=open(log_run_path,'a')
    now = datetime.datetime.now()
    nowprint=now.strftime('%Y-%m-%d  %H:%M:%S ')
    adict={'night':'1','day':'0','auto_gain':'3','auto_photo':'5','time':'3','H.264':'0','H.265':'1','MJPEG':'2'}
    i = value
    i=str(i)
    a = adict.get(i)
    x=type(i)
    #print x
    time.sleep(1)
    r=ssh_ipc(cmd)
    s=type(r)
    #print s
    if a ==r:
        print ('当前测试值:'+i+'：测试 OK')
        printout = nowprint+str('当前测试值:'+i+'：测试 OK'+ "\r\n")
        #print printout
        filerunlog.write(printout+ "\r\n")
    else:
        print ('测试值:'+i+'：时测试用例执行失败')
        printout = nowprint+str('测试值:'+i+'：时测试用例执行失败'+ "\r\n")
        filerunlog.write(printout)
    filerunlog.close()
def resolution_verify(value):
    filerunlog=open(log_run_path,'a')
    now = datetime.datetime.now()
    nowprint=now.strftime('%Y-%m-%d  %H:%M:%S ')
    cmd1=["cat /usr/config/ipccfg.conf|awk -F VidWide '{print $2}'|awk -F , '{print $1}'|awk -F : '{print $2}'"]
    r1=str(ssh_ipc(cmd1))
    cmd2=["cat /usr/config/ipccfg.conf|awk -F VidHeight '{print $5}'|awk -F , '{print $1}'|awk -F : '{print $2}'"]
    r2=str(ssh_ipc(cmd2))
    v = value.split('*')
    v1 = v[0]
    v2 = v[1]
    if v1 ==r1 and v2 == r2:
        print ('当前测试值:'+v1+'*'+v2+'：测试 OK')
        printout = nowprint+str('当前测试值:'+v1+'*'+v2+'：测试 OK'+ "\r\n")
        print printout
        filerunlog.write(printout+ "\r\n")
    else:
        print ('测试值:'+v1+'*'+v2+'：时测试用例执行失败')
        printout = nowprint+str('当前测试值:'+v1+'*'+v2+'：时测试用例执行失败'+ "\r\n")
        filerunlog.write(printout)
    
def openssh(host,username,password):
    command = 'openssh'
    tn = telnetlib.Telnet(host,port=17230,timeout=10)
    tn.open(host,port=17230)
    tn.read_until("Username:",timeout=2)
    tn.write(username+ "\r\n")
    tn.read_until("Password:")
    tn.write(password+ "\r\n")
    tn.write('%s\r\n' % command)
    
def ftp_download(ipcpath ='/usr/config/',filename = "ipccfg.conf"):
    ftp=FTP()   
    ftp.set_debuglevel(2)   
    ftp.connect(host,port=21)
    ftp.login(username,password)
    print (ftp.getwelcome())
    
    ftp.cwd(ipcpath)
    bufsize = 1024  
    file_handler = open(log_system_path+filename,'w').write
    file_handler("\n")
    ftp.retrbinary('RETR %s' % os.path.basename(filename),file_handler,bufsize)
    ftp.set_debuglevel(0)   
    print ("ftp down OK")
    ftp.quit()   


if __name__ =='__main__':
    ipcpath = '/var/log/'
    filename = "message"
    ftp_download(ipcpath, filename)
