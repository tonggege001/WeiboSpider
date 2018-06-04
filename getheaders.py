__author__ = 'Administor'

'''
功能：获取网页的Cookie
入口参数：fileName:保存登陆后的网页的信息，其中浏览器是Chrome，检查->Network->登录->F5刷新->Network下的网页地址复制到fileName中
出口参数：headers,里面包含了Cookie和User-Agent
'''
def getHeaders(fileName):
    headers = []
    headerList = ['User-Agent','Cookie']
    with open(fileName,'r') as fp:
        for line in fp.readlines():
            name,value = line.split(':',1)
            if name in headerList:
                headers.append((name.strip(),value.strip()));
    return headers

if __name__=='__main__':
    headers = getHeaders('headersRaw.txt')
    print(headers)