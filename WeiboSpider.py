__author__ = 'Administor'
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from myLog import MyLog as MyLog


'''
Class:WBSpider
方法：
'''

class WBSpider(object):
    '''
    属性：
        username:微博的用户名
        password:微博的密码
        driver:浏览器，默认是PhantomJS
    '''

    def __init__(self, username, password):
        self.log = MyLog()#获得打印日志对象
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)#静静等待10s
        self.isLogin = 0
        self.uid = ""

    '''
    析构函数
    在销毁该类的实例的时候将浏览器关闭。
    '''
    def __del__(self):
        self.driver.close()#关闭浏览器

    '''
    登录微博的函数
    登陆成功则属性isLogin为1，否则为0
    '''
    def loginWeibo(self):
        #输入用户名/密码登录
        self.driver.get("http://login.sina.com.cn/")
        self.driver.implicitly_wait(5)
        elem_user = self.driver.find_element_by_name("username")#找到用户名输入框
        elem_user.send_keys(self.username) #传送用户名
        #找到密码输入框
        elem_pwd = self.driver.find_element_by_name("password")
        elem_pwd.send_keys(self.password)  #传送密码
        try:
            time.sleep(5)
            elem_pwd.send_keys(Keys.RETURN)#直接传送回车键
            time.sleep(2)
            self.log.info('登陆成功...')
            self.isLogin = 1#是否登录的标志
        except :
            self.Log.error("Login Error")
            self.isLogin = 0#是否登录的标志

    '''
    设置需要爬虫微博主的Uid
    '''
    def setUid(self,Uid):
        self.uid = Uid

    '''
    获取微博
    PageNum:输入爬取微博的页数
    返回：微博的列表
    '''
    def getWeibo(self,PageNum):
        total = PageNum
        #判断不成立的条件
        if self.isLogin == 0:
            self.log.error("没有登录微博！")
            return
        if self.uid=="":
            self.log.error("待爬取的微博主的uid为空，请设置！")
            return
        if PageNum<0:
            self.log.error("页数设置不合法")
            return
        #开始爬取
        weiboList = []
        url = "http://weibo.com/" + self.uid
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        #爬取名称
        self.log.debug("准备访问个人网站....."+str(url))
        self.log.info('个人详细信息')
        #用户id
        print (u'用户id: ' + self.uid)
        self.driver.implicitly_wait(5)
        #昵称
        str_name = self.driver.find_element_by_xpath("//div[@class='pf_username']/h1")
        name = str_name.text        #str_name.text是unicode编码类型
        self.log.info("昵称:"+str(name))
        self.driver.implicitly_wait(5)
        try:
            while(1):
                #让selenium直接滚动到下一页，用来获取“下一页”按钮
                print("正在爬取第"+str(total-PageNum+1)+"页")
                next_page = None
                try:
                    next_page = self.driver.find_element_by_link_text('下一页')
                except:
                    next_page = None
                Count = 0
                while(next_page is None):
                    try:
                        next_page = self.driver.find_element_by_link_text('下一页')
                    except:
                        next_page = None
                    Count = Count+1
                    print(Count)
                    time.sleep(3)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    if Count==200:
                        break
                #获取微博元素
                weiboelem = self.driver.find_elements_by_xpath("//div[@action-type='feed_list_item']/div[@node-type='feed_content']/div[@class='WB_detail']/div[@node-type='feed_list_content']")
                #将微博元素列表转换成字符串并加入到微博列表中
                for i in range(len(weiboelem)):
                    weiboList.append(weiboelem[i].text)
                #获得下一页按钮并点击,此处可能会出现加载不出来下一页按钮的异常
                if(next_page is None):
                    break
                if(PageNum==0):
                    self.log.info("到达尾页")
                    break
                #下一页按钮被覆盖，不能clickable
                ActionChains(self.driver).move_to_element(next_page).click(next_page).perform()
                next_page.click()
                Pagenum = Pagenum-1
                self.driver.implicitly_wait(5)
        except:
            self.log.error("爬取异常")
        finally:
            return weiboList

#程序的入口地址
if __name__=="__main__":
    WBS = WBSpider("在此输入用户名","在此输入密码")
    WBS.setUid("5985604592")#测试样例使用省钱小管家
    WBS.loginWeibo()#登录微博
    weibolist = WBS.getWeibo(2)
    print(weibolist)