import logging
import re

from pyquery import PyQuery as pq

from proxypool import setting
from proxypool import utils

logging.basicConfig(level=setting.LOGGING_LEVEL)

'爬虫模块'


class ProxyMetaclass(type):
    '''
    元类
    在ProxyCrawl中添加__CrawlFunc__与__CrawlFuncCount__
    分别表示爬虫函数和爬虫数量
    '''

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxyCrawl(object, metaclass=ProxyMetaclass):
    '''
    爬虫类
    '''

    def get_raw_proxies(self, callback):
        '''
        迭代每个爬虫函数的生成器，循环获取每行代理IP加入到数组并返回
        :param callback: 爬虫函数
        :return: 代理数组
        '''
        proxies = []
        logging.debug('callback', callback)
        for proxy in eval('self.{}()'.format(callback)):
            logging.info('获取代理', proxy, '来源', callback)
            proxies.append(proxy)
        return proxies

    def crawl_ip181(self):
        '''
        爬取ip181 100个精选代理IP
        :return:
        '''
        start_url = 'http://www.ip181.com'
        html = utils.get_page(start_url)
        reobj = re.compile(r"<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>")
        proxy_array = reobj.findall(html)  # [(ip1,port1),(ip2,port2)]形式
        proxy_array.pop(0)  # 去除数组中第一个，第一个内容为(IP地址,端口)
        for addr, port in proxy_array:
            result = addr + ":" + port
            yield result.replace(' ', '')  # 将空格剔除

    def crawl_xicidaili(self):
        '''
        爬取xicidaili 国内HTTP代理
        :return:
        '''
        for pageNo in range(1, 4):  # 爬取前3页代理
            start_url = 'http://www.xicidaili.com/wt/{}'.format(pageNo)
            html = utils.get_page(start_url)
            reobj = re.compile(
                r'<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            proxy_array = reobj.findall(html)
            for addr, port in proxy_array:
                result = addr + ':' + port
                yield result.replace(' ', '')

    def crawl_ip3366(self):
        '''
        爬取ip3366 国内高匿代理
        :return:
        '''
        for pageNo in range(1, 4):  # 爬取前3页代理
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(pageNo)
            html = utils.get_page(start_url)
            reobj = re.compile(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>")
            proxy_array = reobj.findall(html)
            for addr, port in proxy_array:
                result = addr + ':' + port
                yield result.replace(' ', '')

    def crawl_66ip(self):
        '''
        爬取66ip 国内高匿代理
        :return:
        '''
        for pageNo in range(1, 4):  # 爬取前3页代理
            start_url = 'http://www.66ip.cn/{}.html'.format(pageNo)
            html = utils.get_page(start_url)
            reobj = re.compile(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>")
            proxy_array = reobj.findall(html)
            proxy_array.pop(0)  # 去除数组中第一个，第一个内容为(IP地址,端口)
            for addr, port in proxy_array:
                result = addr + ':' + port
                yield result.replace(' ', '')

    def crawl_goubanjia(self):
        '''
        爬取goubanjia 国内高匿代理
        由于网页结构较复杂，使用pyquery更简单快速
        :return:
        '''
        for pageNo in range(1, 4):  # 爬取前3页代理
            start_url = 'http://www.goubanjia.com/free/gngn/index{}.shtml'.format(pageNo)
            html = utils.get_page(start_url)
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')

    def crawl_data5u(self):
        '''
        爬取data5u 国内高匿代理
        :return:
        '''
        for pageNo in range(1, 4):  # 爬取前3页代理
            start_url = 'http://www.data5u.com/free/gngn/index{}.shtml'.format(pageNo)
            html = utils.get_page(start_url)
            reobj = re.compile(
                r'span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class="port .*?">(.*?)</li></span>')
            proxy_array = reobj.findall(html)
            for addr, port in proxy_array:
                result = addr + ':' + port
                yield result.replace(' ', '')

    def crawl_kxdaili(self):
        '''
        爬取kxdaili 国内高匿代理
        :return:
        '''
        for pageNo in range(1, 4):  # 爬取前3页代理
            start_url = 'http://www.kxdaili.com/dailiip/1/{}.html'.format(pageNo)
            html = utils.get_page(start_url)
            reobj = re.compile(r"<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>")
            proxy_array = reobj.findall(html)
            for addr, port in proxy_array:
                result = addr + ':' + port
                yield result.replace(' ', '')
