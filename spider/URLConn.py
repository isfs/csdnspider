from urllib.request import Request, urlopen
import urllib.request
import ssl
import gzip
from lxml import etree
# 随机数
import random

# 防止浏览器认出是爬虫，更换头部和ip
class URLConn:
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.headres = [
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"},
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"},
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3538.102 Safari/537.36 Edge/18.18363"},
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.4280.66 Safari/537.36"},
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"},
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"},
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"},
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"},
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"},
            {
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"},
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
     ]
        self.pro = [
            {"https://": "182.34.34.230:9999"},
            {"https://": "60.176.116.214:8888"},
            {"https://": "60.176.116.214:8888"},
            {"https://": "222.217.30.29:8888"},
            {"https://": "218.104.248.36:9999"},
            {"https://": "49.70.99.95:9999"},
            {"https://": "49.87.29.174:8888"},
            {"https://": "163.204.93.34:9999"},
            {"https://": "36.251.147.24:8888"}
        ]
        pass

    def getData(self, path):
        numHeaders = random.randint(0, len(self.headres) - 1)
        myHeaders = self.headres[numHeaders]
        req = Request(url=path, headers=myHeaders)

        numPro = random.randint(0, len(self.pro) - 1)
        myPro = self.pro[numPro]
        # 设置代理
        urllib.request.ProxyHandler(myPro)

        conn = urlopen(req)
        if conn.code == 200:
            data = conn.read()
            iszip = conn.headers.get("content-encoding")
            if iszip == "gzip":
                data = gzip.compress(data)
            data = data.decode(encoding="utf-8")
            return data
            pass
        else:
            return "网络连接异常:%d" % conn.code

    pass
