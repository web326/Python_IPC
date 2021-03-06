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
    def video_type(self):
        time.sleep(0.5)
        self.driver.find_element_by_id("MenuConfig").click()
        time.sleep(0.5)
        self.driver.switch_to_frame('contentframe')
        time.sleep(0.5)
        self.driver.find_element_by_id("aVideoCamera").click()
        time.sleep(0.5)
        self.driver.find_element_by_id("aVideo").click()
        time.sleep(0.5)
        self.driver.find_element_by_id("MVideo").click()
        time.sleep(0.5)
    def video_type_change(self):
        ##编码格式H.264、H.265、MJPEG
        list = ['H.264','H.265','MJPEG']
        for i in list:
            self.driver.find_element_by_id("videoCodecType").click()
            self.select=Select(self.driver.find_element_by_id('videoCodecType'))
            time.sleep(0.5)
            self.select.select_by_value(i)
            time.sleep(0.5)
            self.driver.find_element_by_id("videoCodecType").click()
            time.sleep(0.5)
            self.driver.find_element_by_id("ConfigBtn").click()
            time.sleep(8)
            cmd = ["cat /usr/config/ipccfg.conf|awk -F DayNightMode '{print $5}'|awk -F , '{print $1"" }'|awk -F : '{print $2}'"]
            conf_verify(i,cmd)
            time.sleep(2)

class VideotypeChange(unittest.TestCase,action):
    def setUp(self):
        #self.profileDir="C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\9znyf7zm.default"
        self.profileDir=profileDir
        self.profile=webdriver.FirefoxProfile(self.profileDir)
        self.driver=webdriver.Firefox(self.profile)  #初始化浏览器，使启动的浏览器可以加载已配置的信息
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.get('http://'+host)      #输入IP地址
        self.login(username,password)
        self.video_type()
    def tearDown(self): 
        self.driver.quit()
#设置长拷的次数
    def test_01(self):
        n=0
        while (n<num):
            n=n+1
            print '第 ',n ,' 次日编码格式切换'
            self.video_type_change()
def test_video_type():
    suite=unittest.TestSuite(unittest.makeSuite(VideotypeChange))
    unittest.TextTestRunner(verbosity=2).run(suite)

def test01():    
    threads = []
    t1 = threading.Thread(target=test_video_type,args=())
    threads.append(t1)
    t2 = threading.Thread(target=ping_telnet,args=())
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    

if __name__ == "__main__":
    test01()

