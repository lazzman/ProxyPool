import redis

from proxypool import setting
from proxypool.error import PoolEmptyError

'redisDB操作模块'


class RedisClient(object):
    def __init__(self):
        if setting.REDIS_PASSWORD:
            self._db = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT, password=setting.REDIS_PASSWORD)
        else:
            self._db = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)

    def getProxy(self, count=1):
        '''
        从Redis中的proxies列表中获取指定数量的代理
        :param count: 代理数量
        :return:
        '''

        # Redis Lrange 返回列表中指定区间内的元素，区间以偏移量 START 和 END 指定。
        # 其中 0 表示列表的第一个元素， 1 表示列表的第二个元素，以此类推。
        # 你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
        proxies = self._db.lrange('proxies', 0, count - 1)

        # Redis Ltrim 对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
        # 下标 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
        #  你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
        self._db.ltrim("proxies", count, -1)
        return proxies

    def putProxy(self, proxy):
        '''
        向Redis中的proxies列表添加一个代理
        :param proxy:
        :return:
        '''

        # Redis Rpush 命令用于将一个或多个值插入到列表的尾部(最右边)。
        # 如果列表不存在，一个空列表会被创建并执行 RPUSH 操作。 当列表存在但不是列表类型时，返回一个错误。
        self._db.rpush("proxies", proxy)

    def popProxy(self):
        '''
        从Redis中的proxies列表末尾Pop一个代理
        :return:
        '''

        # Redis Rpop 命令用于移除并返回列表的最后一个元素。
        # 当列表不存在时，返回 nil 。
        try:
            return self._db.rpop("proxies").decode('utf-8')  # 当列表没有元素时会发生异常
        except:
            raise PoolEmptyError

    @property
    def queueLen(self):
        '''
        获取Redis中的proxies列表长度
        :return:
        '''

        # Redis Llen 命令用于返回列表的长度。 如果列表 key 不存在，则 key 被解释为一个空列表，返回 0 。 如果 key 不是列表类型，返回一个错误。
        return self._db.llen("proxies")

    def flushQueue(self):
        '''
        清空Redis中的proxies列表
        :return:
        '''

        # self._db.flushall() # 清空所有key
        self._db.delete("proxies")


if __name__ == '__main__':
    conn = RedisClient()
    # print(conn.queueLen)
    # print(conn.popProxy())
    print(conn.getProxy())
