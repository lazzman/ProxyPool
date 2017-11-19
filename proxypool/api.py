import json

from flask import Flask, g

from .db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    '''
    获取redis连接
    :return:
    '''
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client


@app.route('/')
def index():
    return 'ProxyPool Index Page'


@app.route('/getProxy')
def get_proxy():
    '''
    获取1个代理
    :return:
    '''
    conn = get_conn()
    return json.dumps(conn.popProxy())


@app.route('/getMoreProxy/<int:count>')
def get_more_proxy(count):
    '''
    获取指定数量的代理，代理池不足时有多少返回多少
    :return:
    '''
    conn = get_conn()
    raw_proxys = conn.getProxy(count)
    proxys = [proxy.decode('utf-8') for proxy in raw_proxys if isinstance(proxy, bytes)]
    return json.dumps(proxys)


if __name__ == '__main__':
    app.run()
