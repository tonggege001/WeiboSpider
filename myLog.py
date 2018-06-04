__author__ = 'Administor'
'''
自定义模块myLog，将日志信息输出在文件中

'''
import logging
import getpass
import sys

#定义MyLog类
class MyLog(object):
    #这个类用于创建一个自用的log
    def __init__(self):#构造函数
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        logFile = 'Log.log'#日志文件名
        formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')
        '''日志显示在屏幕上并输出在日志上'''
        logHand = logging.FileHandler(logFile)
        logHand.setFormatter(formatter)
        logHand.setLevel(logging.ERROR)#只有错误才会被记录在logFile中
        logHandSt = logging.StreamHandler()
        logHandSt.setFormatter(formatter)

        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandSt)

        '''日志的五个级别对应以下五个函数'''
    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warn(self,msg):
        self.logger.warn(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)

if __name__=='__main__':
    myLog = MyLog()
    myLog.debug("I'm debug")
    myLog.info("I'm info")
    myLog.warn("I'm warn")
    myLog.error("I'm error")
    myLog.critical("I'm critical")