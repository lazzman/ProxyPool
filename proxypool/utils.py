import logging

import requests

from . import setting

logging.basicConfig(level=setting.LOGGING_LEVEL)

'工具模块'


def get_page(url, options={}):
    '''
    爬取指定页面并返回页面内容
    :param url: 网页url
    :param options: 附加的请求头
    :return: 页面内容
    '''
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
    requestHeaders = {
        'User-Agent': ua,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(requestHeaders, **options)
    logging.info('爬取网页内容开始 url：%s ' % (url,))
    try:
        r = requests.get(url, headers=headers)
        logging.info("爬取页面内容完毕 url:%s 响应码:%s" % (url, r.status_code))
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        logging.warning('爬取页面失败 url：%s' % (url,))
        return None
