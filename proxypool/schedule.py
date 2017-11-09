import asyncio
import logging
import time
from multiprocessing import Process

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


class Schedule(object):
    '''
    调度器模块
    '''

    @staticmethod
    def check_pool_proxy_useable(cycle=setting.PROXY_CHECK_CYCLE):
        '''
        一定周期从代理池取出一半的代理检查有效性
        :param cycle:
        :return:
        '''
        conn = RedisClient()
        checker = ValidityChecker()
        while True:
            logging.info("开始校验代理池代理有效性")
            count = int(0.5 * conn.queueLen)
            if count == 0:
                logging.info("代理池中暂无代理，等待添加代理")
                time.sleep(cycle)
                continue
            raw_proxies = conn.getProxy(count)
            checker.set_raw_proxies(raw_proxies)
            checker.check()
            time.sleep(cycle)

    @staticmethod
    def add_proxy_to_pool(lower_threshold=setting.PROXY_POOL_LOWER_THRESHOLD,
                          upper_threshold=setting.PROXY_POOL_UPPER_THRESHOLD, cycle=setting.PROXU_POOL_LEN_CHECK_CYCLE):
        '''
        一定周期检查代理池中代理数量是否在阈值内，不在则调用添加器添加代理
        :param lower_threshold:
        :param upper_threshold:
        :param cycle:
        :return:
        '''
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queueLen < lower_threshold:
                adder.pool_add_proxy()
            time.sleep(cycle)

    def run(self):
        '''
        创建两个进程，分别用于校验代理池代理有效性和检查代理池中代理数量是否在阈值内
        :return:
        '''
        logging.info('调度器开始运行')
        check_process = Process(target=Schedule.check_pool_proxy_useable)
        threshold_process = Process(target=Schedule.add_proxy_to_pool)
        check_process.start()
        threshold_process.start()
