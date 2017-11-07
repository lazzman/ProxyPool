import re

from pyquery import PyQuery as pq

from proxypool import utils

'测试爬虫方法是否正确'


def crawl_ip181():
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

def crawl_xicidaili():
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


def crawl_goubanjia():
    '''
    爬取goubanjia 国内高匿代理
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


def crawl_data5u():
    '''
    爬取data5u 国内高匿代理
    :return:
    '''
    for pageNo in range(1, 3):  # 爬取前3页代理
        start_url = 'http://www.data5u.com/free/gngn/index{}.shtml'.format(pageNo)
        html = utils.get_page(start_url)
        reobj = re.compile(
            r'span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class="port .*?">(.*?)</li></span>')
        proxy_array = reobj.findall(html)
        for addr, port in proxy_array:
            result = addr + ':' + port
            yield result.replace(' ', '')


def crawl_kxdaili():
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


if __name__ == '__main__':
    for proxy in crawl_ip181():
        print(proxy)
