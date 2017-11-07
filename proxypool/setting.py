# Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379  # 默认端口
REDIS_PASSWORD = ''  # 如果有密码则填写密码，没有则为''

# 代理检测超时时间(单位秒)
PROXY_CHECK_TIMEOUT = 9

# 代理有效性校验周期（单位秒）
PROXY_CHECK_CYCLE = 60
# 代理池长度校验周期
PROXU_POOL_LEN_CHECK_CYCLE = 20

# 代理池代理IP数量（上下限）
PROXY_POOL_LOWER = 20
PROXY_POOL_UPPER = 100

# 测试API
TEST_API = 'http://www.baidu.com'

import logging

# 控制台日志输出级别
LOGGING_LEVEL = logging.INFO
