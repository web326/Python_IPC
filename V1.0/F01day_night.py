#coding=utf-8

import unittest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from System_Info import ping_telnet,conf_verify
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
    def Day_night(self):
        time.sleep(0.5)
        self.driver.find_element_by_id("MenuConfig").click()
        time.sleep(0.5)
        self.driver.switch_to_frame('contentframe')
        time.sleep(0.5)
        self.driver.find_element_by_id("aVideoCamera").click()
        time.sleep(0.5)
        self.driver.find_element_by_id("aImagsSettings").click()
        time.sleep(0.5)
        self.driver.find_element_by_id("ircutfilterh5").click()
        time.sleep(0.5)
    def Day_night_change(self):
        ##夜：night  白天：day 自动增益：auto_gain  自动光敏：auto_photot.sleep(0.5)
        list = ['night','day']
        for i in list:
            self.driver.find_element_by_id("IrcutfilterType").click()
            self.select=Select(self.driver.find_element_by_id('IrcutfilterType'))
            self.select.select_by_value(i)
            self.driver.find_element_by_id("IrcutfilterType").click()
            time.sleep(8)
            cmd = ["cat /usr/config/ipccfg.conf|awk -F DayNightMode '{print $5}'|awk -F , '{print $1"" }'|awk -F : '{print $2}'"]
            conf_verify(i,cmd)
            time.sleep(2)

class DnyNightchange(unittest.TestCase,action):
    def setUp(self):
        #self.profileDir="C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\9znyf7zm.default"
        self.profileDir=profileDir
        self.profile=webdriver.FirefoxProfile(self.profileDir)
        self.driver=webdriver.Firefox(self.profile)  #初始化浏览器，使启动的浏览器可以加载已配置的信息
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get('http://'+host)#输入IP地址???
        self.login(username,password)
        self.Day_night()
    def tearDown(self): 
        self.driver.quit()
#设置长拷的次数
    def test_01(self):
        n=0
        while (n<num):
            n=n+1
            print '第 ',n ,' 次日夜切换测试'
            self.Day_night_change()
def day_night():
    suite=unittest.TestSuite(unittest.makeSuite(DnyNightchange))
    unittest.TextTestRunner(verbosity=2).run(suite)
#开始前的检测
def test_test():
#检测主机地址是否通;os.system返回0是通，1是不通
    ping_return=os.system('ping -n 4 -w 1 %s'%host) #每个ip ping2次，等待时间为1s 
    #print return1
    if ping_return: 
        print 'ping %s is fail'%host #需要考虑如何显示在GUI上面
        return
    else: 
        print 'ping %s is ok'%host #需要考虑如何显示在GUI上面
    

def test01():    
    threads = []
    t1 = threading.Thread(target=day_night,args=())
    threads.append(t1)
    t2 = threading.Thread(target=ping_telnet,args=())
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    

if __name__ == "__main__":
    test01()

