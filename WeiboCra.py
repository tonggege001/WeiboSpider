# coding=utf-8

"""
Created on 2018-06-03 @author: Tonggege

功能: 爬取新浪微博用户的信息及微博
网址：http://weibo.cn/ 数据量更小 相对http://weibo.com/
"""

import time
import re
import os
import sys
import codecs
import shutil
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
import csv
'''
    func:登录微博
    参数1：driver
    参数2：用户名
    参数3：密码
'''
def LoginWeibo(driver,username, password):
    #输入用户名/密码登录
    print('准备登陆Weibo.cn网站...')
    driver.get("http://login.sina.com.cn/")
    driver.implicitly_wait(10)
    #找到用户名输入框
    elem_user = driver.find_element_by_name("username")
    elem_user.send_keys(username) #传送用户名
    #找到密码输入框
    elem_pwd = driver.find_element_by_name("password")
    elem_pwd.send_keys(password)  #传送密码
    try:
        #elem_rem = driver.find_element_by_name("safe_login")
        #elem_rem.click()             #安全登录
        #重点: 暂停时间输入验证码(http://login.weibo.cn/login/ 手机端需要)
        time.sleep(20)
        #elem_sub = driver.find_element_by_xpath("//input[@class='smb_btn']")
        #elem_sub.click()              #点击登陆 因无name属性
        #直接按回车
        elem_pwd.send_keys(Keys.RETURN)
        time.sleep(2)
        #获取Coockie 推荐资料：http://www.cnblogs.com/fnng/p/3269450.html
        '''打印Cookies
        print(driver.current_url)
        print (driver.get_cookies())  #获得cookie信息 dict存储
        print ('输出Cookie键值对信息:')
        for cookie in driver.get_cookies():
            #print cookie
            for key in cookie:
                print (key, cookie[key])
        '''
        #driver.get_cookies()类型list 仅包含一个元素cookie类型dict
        print('登陆成功...')
    except:
        print("ERROR")
    finally:
        print(u'End LoginWeibo!\n\n')


#********************************************************************************
#                  第二步: 访问个人页面http://weibo.cn/5824697471并获取信息
#                                VisitPersonPage()
#        编码常见错误 UnicodeEncodeError: 'ascii' codec can't encode characters
#********************************************************************************
'''
    func:访问用户主页获取微博语料
    param:浏览器驱动
    param2:待爬取对象的id
    返回值：微博语料列表
'''
def VisitPersonPage(driver,user_id,Pagenum):
    weiboList = []
    name = ""
    url = "http://weibo.com/" + user_id
    driver.get(url)
    driver.implicitly_wait(10)
    #爬取名称
    print(u'准备访问个人网站.....', url)
    print('个人详细信息')
    #用户id
    print (u'用户id: ' + user_id)
    driver.implicitly_wait(10)
    #昵称
    str_name = driver.find_element_by_xpath("//div[@class='pf_username']/h1")
    name = str_name.text        #str_name.text是unicode编码类型
    print (u'昵称: ', name)
    driver.implicitly_wait(20)
  #  try:
    while(1):
        #让selenium直接滚动到下一页，用来获取“下一页”按钮
        print("正在爬取第页")
        time.sleep(5)
        driver.execute_script("document.body.scrollTop=1080")
        time.sleep(5)
        driver.execute_script("document.body.scrollTop=3080")
        time.sleep(5)
        driver.execute_script("document.body.scrollTop=10880")
        time.sleep(5)
        driver.execute_script("document.body.scrollTop=30880")
        time.sleep(3)
        driver.execute_script("document.body.scrollTop=60880")
        time.sleep(3)
        weiboelem = driver.find_elements_by_xpath("//div[@action-type='feed_list_item']/div[@node-type='feed_content']/div[@class='WB_detail']/div[@node-type='feed_list_content']")
        for i in range(len(weiboelem)):
            weiboList.append(weiboelem[i].text)
        next_page = driver.find_element_by_link_text('下一页')
        if(next_page is None):
            print("next page error!")
            break
        if(Pagenum==0):
            break
        next_page.click()
        Pagenum = Pagenum-1
        driver.implicitly_wait(10)
    #except:
        #print("ERROR")
  #  finally:
       # return name,weiboList

if __name__=="__main__":
    driver = webdriver.PhantomJS()
    wait = ui.WebDriverWait(driver,10)
    #定义变量
    username = ''             #输入你的用户名
    password = ''               #输入你的密码

    #操作函数
    LoginWeibo(driver,username, password)       #登陆微博

    #在if __name__ == '__main__':引用全局变量不需要定义 global inforead 省略即可
   # user_id = user_id.rstrip('\r\n')
    #print (user_id)
    name,list = VisitPersonPage(driver,"5985604592",1)         #访问个人页面http://weibo.cn/guangxianliuyan
    print(list)
    data = []
    for i in range(len(list)):
        data.append([name,list[i]])
with open("zhaolei_data.csv","w",newline="",encoding="UTF-8")  as f:
    writer = csv.writer(f)
    for i in range(len(data)):
        e_list = data[i]
        print(e_list)
        writer.writerow(e_list)
    #或者循环writer.writerow(一个列表元素）




