import asyncio
import logging

import aiohttp
from aiohttp.client_exceptions import *

from proxypool import setting
from proxypool.crawl import ProxyCrawl
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError

logging.basicConfig(level=setting.LOGGING_LEVEL)
'调度器模块'


class ValidityChecker(object):
    '''
    代理校验类
    '''

    def __init__(self):
        self._raw_proxies = None

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies  # 未校验的代理集合
        self._conn = RedisClient()

    async def check_single_proxy(self, proxy):
        '''
        校验单个代理的有效性，有效的存入redis
        :param proxy:
        :return:
        '''
        session = aiohttp.ClientSession()
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
                http_proxy = 'http://' + proxy
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
            async with session.get(setting.CHECK_PROXY_USEFULL_URL, timeout=setting.CHECK_PROXY_USEFULL_TIMEOUT,
                                   headers=headers, proxy=http_proxy) as r:
                if r.status == 200:
                    # 有效代理存入redis
                    self._conn.putProxy(proxy)
                    logging.info('代理[%s]有效' % (proxy,))
        except (TimeoutError, ClientProxyConnectionError) as e:
            logging.warning('代理[%s]无效' % (proxy,))
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError,
                ) as e:
            logging.warning(e)
        finally:
            # 关闭会话
            session.close()

    def check(self):
        '''
        异步校验所有代理
        :return:
        '''
        logging.info("开启异步校验代理")
        loop = asyncio.get_event_loop()
        try:
            tasks = [self.check_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            logging.error("异步校验代理异常")
        finally:
            loop.close()


class PoolAdder(object):
    '''
    代理添加器
    '''

    def __init__(self, upper_threshold):
        self._upper_threshold = upper_threshold  # 阈值上限
        self._conn = RedisClient()
        self._checker = ValidityChecker()
        self._crawler = ProxyCrawl()

    def is_upper_threshold(self):
        '''
        redis中的代理是否超出阈值上限
        :return:
        '''
        if self._conn.queueLen >= self._upper_threshold:
            return True
        else:
            return False

    def pool_add_proxy(self):
        '''
        自动调用爬虫模块爬取代理，校验代理有效性并添加到Redis，到达阈值上限则停止
        :return:
        '''
        logging.info('代理添加器正在运行')
        proxy_count = 0
        while not self.is_upper_threshold():
            for callback in self._crawler.__CrawlFunc__:
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # 校验代理有效
                self._checker.set_raw_proxies(raw_proxies)
                self._checker.check()
                proxy_count += len(raw_proxies)
                if self.is_upper_threshold():
                    logging.info("代理池达到阈值，停止爬虫")
                    break
            if proxy_count == 0:
                raise ResourceDepletionError
