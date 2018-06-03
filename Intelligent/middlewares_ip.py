import random

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import pymysql
import time
'''
class ProxyMiddleware(object):
    def __init__(self):
        self.conn=pymysql.connect(host="localhost", user="root", passwd="26651", db="ip_pool")
    def process_request(self, request, spider):
        # thisip=random.choice(IPPOOL)
        cursor=self.conn.cursor()
        if_get_ip=False
        while not if_get_ip:
            try:
                cursor.execute('select * from ips order by rand() limit 1')
                ips=cursor.fetchall()
                self.conn.commit()
                ip=ips[0][0]
                used_times=int(ips[0][1])+1
                try:
                    if used_times<3:
                        cursor.execute("update ips set used_times=%d where ip='%s';" %(used_times,ip))
                    else:
                        cursor.execute("delete from ips where ip='%s';" %ip)
                    self.conn.commit()
                except Exception as e:
                    print("更新使用次数失败！")
                    print("Error:",e)
                print("当前使用的ip为："+ip)
                if_get_ip=True
                request.meta["proxy"]="http://"+ip
                cursor.close()
            except Exception as e:
                print('代理池为空。请等待填充！(3分钟)')
                print("Error:",e)
                time.sleep(60)    #等待3分钟，代理池每2分钟更新一次

'''
'''
# 阿里布 动态ip代理
import base64
# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H51GH40756H0DA2D"
proxyPass = "EAAAB0952E878D91"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
'''

#讯代理转发
import hashlib
# 代理隧道验证信息
orderno="ZF20181298155C04Cc1"
secret="afa41973b05242ddab6c83e0f1ae65b4"

ip="http://forward.xdaili.cn"
port="80"
# 代理服务器
ip_port=ip+":"+port
timestamp = str(int(time.time()))                # 计算时间戳
string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
string = string.encode()
md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
sign = md5_string.upper()
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = ip_port
        request.headers["Proxy-Authorization"] = auth
