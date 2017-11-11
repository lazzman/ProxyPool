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
    conn = get_conn()
    return conn.popProxy()


if __name__ == '__main__':
    app.run()
