#coding=utf-8
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from System_Info import ping_ipc,conf_verify
import time,os,re,threading
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read(r'Config.py')
host = cf.get("common","host")
username = cf.get("common","username")
password = cf.get("common","password")
profileDir = cf.get("profiledir","profileDir")
number = cf.get("common","number")
num = int(number)


class action():
    def login(self,username,password):
        time.sleep(1)
        self.driver.find_element_by_id("username").send_keys(username)
        time.sleep(0.5)
        self.driver.find_element_by_id("password").send_keys(password)
        time.sleep(0.5)
        self.driver.find_element_by_id("b_Login").click()
        time.sleep(2)
    def reboot(self):
        time.sleep(0.5)
        self.driver.find_element_by_id("MenuConfig").click()    ##进入“配置”
        time.sleep(0.5)
        self.driver.switch_to_frame('contentframe')
        time.sleep(0.5)
        self.driver.find_element_by_id("SubSyttem").click()      #进入“系统”
        time.sleep(0.5)
        self.driver.find_element_by_id("aSystemMaintenance").click()   ##进入“系统维护”
        time.sleep(0.5)
        self.driver.find_element_by_class_name("localsecondspan").click()
        time.sleep(0.5)
        self.driver.switch_to_alert()      ##切换到弹出框
        time.sleep(0.5)
        self.driver.execute("acceptAlert")    ##   确认弹出框
        #self.driver.execute("dismissAlert")   ## 取消弹出框
        #self. driver.execute("getAlertText")["value"]   ##获取弹出框的文字
        #self.driver.find_element_by_name("laRestart").click()    ##重启
        time.sleep(2)
        self.driver.quit()
        n = 0
        tt = 50
        while ( n< tt):
            time.sleep(1) 
            n = n+1
            m = 50-n
            print  '倒计时',m

class Reboot(unittest.TestCase,action):
    def setUp(self):
        print '重启初始化开始'
    def tearDown(self): 
        #self.driver.quit()
                print '重启环境回收完成'
#设置长拷的次数
    def test_01(self):
        n=0
        while (n<num):
            n=n+1
            print '第 ',n ,' 次重启'
            self.profileDir=profileDir
            self.profile=webdriver.FirefoxProfile(self.profileDir)
            self.driver=webdriver.Firefox(self.profile)      #初始化浏览器，使启动的浏览器可以加载已配置的信息
            self.driver.maximize_window()
            self.driver.implicitly_wait(30)
            self.driver.get('http://'+host)     #输入IP地址???
            self.login(username,password)
            self.reboot()
        
def test_reboot():
    suite=unittest.TestSuite(unittest.makeSuite(Reboot))
    unittest.TextTestRunner(verbosity=2).run(suite)
 
def test05():
    threads = []
    t1 = threading.Thread(target=test_reboot,args=())
    threads.append(t1)
    t2 = threading.Thread(target=ping_ipc,args=(host,))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    

if __name__ == "__main__":
    test05()

